import logging
import os
from typing import Optional
from typing import Tuple
from urllib.parse import urlparse

from volcengine import Credentials

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.io import tos
from volcengine_ml_platform.innerapi import model_client as inner_model_client
from volcengine_ml_platform.innerapi import sts_token
from volcengine_ml_platform.models import validation
from volcengine_ml_platform.openapi import secure_token_client


class Model:
    """Model类封装了模型仓库相关的一些操作,包括：模型上传、下载、更新、删除，评测任务提交、更新等"""

    def __init__(self, target_account_id=None, target_user_id=None):
        self.inner_model_client = inner_model_client.ModelInnerApiClient()
        self.inner_sts_client = sts_token.STSApiClient()
        self.secure_token_client = secure_token_client.SecureTokenClient()
        self.module_name = constant.MODULE_MODEL_REPO
        self.target_account_id = target_account_id
        self.target_user_id = target_user_id

    def set_target_account_id(self, target_account_id):
        self.target_account_id = target_account_id
    
    def set_target_user_id(self, target_user_id):
        self.target_user_id = target_user_id

    def get_target_account_id(self):
        if self.target_account_id is None:
            self.target_account_id = int(os.getenv(constant.ACCOUNT_ID_ENV_NAME))
        return self.target_account_id

    def get_target_user_id(self):
        if self.target_user_id is None:
            self.target_user_id = int(os.getenv(constant.USER_ID_ENV_NAME))
        return self.target_user_id

    @staticmethod
    def _model_version_id(model_id, model_version):
        return f"{model_id}-{model_version.lower()}"

    def _get_secure_token(self):
        resp = self.secure_token_client.get_secure_token(
            module_name=self.module_name,
            time_to_live=600,
            account_id=self.get_target_account_id(),
            user_id=self.get_target_user_id(),
        )
        return resp["Result"]["Token"]

    def _get_sts_token(self):
        resp = self.inner_sts_client.get_sts_token(self._get_secure_token())
        result = resp["Result"]
        return result['AccessKeyId'], result['SecretAccessKey'], result['SessionToken']

    def get_model_version(
        self,
        model_id: str,
        model_version: str,
    ):
        """获取模型版本

        Args:
            model_id (str): 模型在仓库中的唯一标识
            model_version (str): 模型版本号

        Returns:
            返回json格式的response，包含模型版本信息
            比如: ::
                {
                    "ResponseMetadata": {
                        "RequestId": "2021091410551801022514606301199F07",
                        "Action": "ListModelVersions",
                        "Version": "2021-07-01",
                        "Service": "ml_platform",
                        "Region": "cn-north-4"
                    },
                    "Result": {
                        "ModelVersionID": "m-20210812150750-w54j6-14",
                        "ModelVersion": 14,
                        "ModelFormat": "SavedModel",
                        "ModelType": "TensorFlow:2.4",
                        "Path": "tos://ml-platform-auto-created-required-2100000050-cn-north-4/modelrepo/from-sdk-repo/1631236594036/1/",
                        "Description": "test remark 2",
                        "SourceType": "TOS",
                        "CreateTime": "2021-09-10T09:37:14+08:00",
                        "TensorConfig": {
                            "Inputs": []
                        }
                    }
                }

        Raises:
            Exception: 获取模型版本异常
        """
        if not model_id:
            logging.warning("model_id is empty")
            return None

        return self.inner_model_client.get_model_version(
            model_version_id=self._model_version_id(model_id, model_version),
            token=self._get_secure_token(),
        )

    def _get_tos_client(self):
        ak, sk, session_token = self._get_sts_token()
        region = volcengine_ml_platform.get_credentials().region
        credentials = Credentials.Credentials(ak, sk, constant.SERVICE_NAME, region)
        return tos.TOSClient(credentials, session_token)

    def _download_model(self, remote_path, local_path):
        parse_url = urlparse(remote_path)
        scheme = parse_url.scheme
        if scheme == "tos":
            bucket = parse_url.hostname
            key = parse_url.path.lstrip("/")
            tos_client = self._get_tos_client()
            tos_client.download_dir(bucket, key, key, local_path)
        else:
            logging.warning("unsupported remote_path, %s", remote_path)

    def download(
        self,
        model_id: str,
        model_version: str,
        local_path: str,
    ):
        """下载模型到本地

        Args:
            model_id (str): 模型在仓库中的唯一标识
            model_version (str): 模型版本号
            local_path (str): 标示模型下载到本地时的存储路径

        Raises:
            Exception: 模型下载异常
        """
        if not model_id:
            logging.warning("Model can not be download, model_id is empty")
            raise ValueError

        response = self.get_model_version(model_id, model_version)
        remote_path = response["Result"]["Path"]

        self._download_model(remote_path, local_path)
        logging.info(
            "model %s:%s download finished to %s",
            model_id,
            model_version,
            local_path,
        )

    def update_model_version(
        self,
        model_id: str,
        model_version: str,
        description: Optional[str] = None,
        tensor_config: Optional[dict] = None,
        model_metrics: Optional[list] = None,
    ):
        """更新模型版本

        Args:
            model_id (str): 模型在仓库中的唯一标识
            model_version (str): 模型版本号
            description (str, optional): 模型描述信息。 默认为None
            tensor_config (dict, optional): 模型的Tensor配置。 默认为None
            model_metrics (list, optional): 模型的指标数据。默认为None

        Returns:
            返回json格式的response，包含模型版本ID
            比如: ::
                {
                    "ResponseMetadata": {
                        "RequestId": "202109141641180102250842170249FC70",
                        "Action": "UpdateModelVersion",
                        "Version": "2021-07-01",
                        "Service": "ml_platform",
                        "Region": "cn-north-4"
                    },
                    "Result": {
                        "ModelVersionID": "m-20210805193007-tt2ww-1"
                    }
                }

        Raises:
            Exception: 更新模型版本异常
        """
        try:
            validation.validate_model_tensor_config(tensor_config)
        except Exception as e:
            raise Exception("Invalid tensor config.") from e

        try:
            validation.validate_metrics(model_metrics)
        except Exception as e:
            raise Exception("Invalid models metrics.") from e

        return self.inner_model_client.update_model_version(
            model_version_id=self._model_version_id(model_id, model_version),
            token=self._get_secure_token(),
            description=description,
            tensor_config=tensor_config,
            model_metrics=model_metrics,
        )

    @staticmethod
    def _register_validate_and_preprocess(
        local_path: str,
        model_id: Optional[str] = None,
        model_name: Optional[str] = None,
        model_format: Optional[str] = None,
        model_type: Optional[str] = None,
        tensor_config: Optional[dict] = None,
        model_metrics: Optional[list] = None,
        model_category: Optional[str] = None,
        source_type: Optional[str] = None,
    ):
        if model_id is None and (model_name is None or model_format is None or model_type is None):
            logging.warning(
                "Register new model need parameter model_name,model_format,model_type",
            )
            raise ValueError
        validation.validate_local_path(local_path)
        validation.validate_model_tensor_config(tensor_config)
        validation.validate_metrics(model_metrics)
        validation.validate_model_category(model_category)
        validation.validate_source_type(source_type)

    def _require_model_tos_storage(self) -> Tuple[str, str]:
        response = self.inner_model_client.get_tos_upload_path(
            service_name=constant.MODULE_MODEL_REPO,
            path=["from-sdk-repo"],
            token=self._get_secure_token(),
        )
        return response["Result"]["Bucket"], response["Result"]["KeyPrefix"]

    def register(
        self,
        local_path: str,
        model_id: Optional[str] = None,
        model_name: Optional[str] = None,
        model_format: Optional[str] = None,
        model_type: Optional[str] = None,
        description: Optional[str] = None,
        tensor_config: Optional[dict] = None,
        model_metrics: Optional[list] = None,
        model_category: Optional[str] = None,
        dataset_id: Optional[str] = None,
        source_type: Optional[str] = "TOS",
        base_model_version_id: Optional[str] = None,
    ):
        """注册模型到模型仓库

        将存储在本地的模型包，上传到模型仓库

        Args:
            local_path (str): 模型在本地的存放路径
            model_id (str, optional): 模型在仓库中的唯一标识。默认为None
                指定该参数时，会在`model_id`对应的模型下，注册一个新的模型版本
                不指定该参数时，会在模型仓库中创建一个新的模型
            model_name (str, optional): 模型名字。默认为None
                如果指定了`model_id`，则该参数可忽略，否则需要填写该参数
            model_format (str): 模型格式
                可选值: 'SavedModel', 'GraphDef','TorchScript','PTX', 'CaffeModel',
                'NetDef','MXNetParams','Scikit_Learn','XGBoost','TensorRT','ONNX', 'Custom'
            model_type (str): 模型框架
                格式：<framework_name:framework_version>，比如：'TensorFlow:2.0'
                框架可选值：'TensorFlow', 'PyTorch', 'ONNX', 'Caffe', 'Caffe2', 'MXNet', 'TensorRT',
                'Scikit_Learn', 'XGBoost', 'LightGBM',
            description (str, optional): 模型描述信息。 默认为None
            tensor_config (dict, optional): 模型的Tensor配置。 默认为None
            model_metrics (list, optional): 模型的指标数据。默认为None
            model_category (str, optional): 模型类别
                可选值: 'TextClassification', 'TabularClassification', 'TabularRegression', 'ImageClassification'
            dataset_id (str, optional): 训练模型所使用的数据集唯一标示
            source_type (str, optional): 模型来源, 默认为TOS
                可选值: 'TOS', 'Local', 'AutoML', 'Perf'
            base_model_version_id (str, optional): perf转换任务生成的模型，所基于的模型版本ID

        Returns:
            返回json格式的response，包含模型相关信息。
            比如: ::
                {
                    "ResponseMetadata": {
                        "RequestId": "20210910093712010225084217038CE268",
                        "Action": "CreateModel",
                        "Version": "2021-07-01",
                        "Service": "ml_platform",
                        "Region": "cn-north-4"
                    },
                    "Result": {
                        "ModelID": "m-20210812150750-w54j6",
                        "VersionInfo": {
                            "ModelVersionID": "m-20210812150750-w54j6-14",
                            "ModelVersion": 14
                        }
                    }
                }

        Raises:
            Exception: 模型创建异常
        """
        self._register_validate_and_preprocess(
            local_path,
            model_id,
            model_name,
            model_format,
            model_type,
            tensor_config,
            model_metrics,
            model_category,
            source_type,
        )

        bucket, prefix = self._require_model_tos_storage()
        tos_client = self._get_tos_client()
        tos_path = tos_client.upload(local_path, bucket, prefix)
        return self.inner_model_client.create_model(
            model_name=model_name,
            model_format=model_format,
            model_type=model_type,
            model_id=model_id,
            path=tos_path,
            token=self._get_secure_token(),
            description=description,
            tensor_config=tensor_config,
            model_metrics=None,
            model_category=model_category,
            dataset_id=dataset_id,
            source_type=source_type,
            base_model_version_id=base_model_version_id,
        )
