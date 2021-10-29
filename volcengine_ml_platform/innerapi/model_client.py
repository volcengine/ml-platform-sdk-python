# type: ignore
import logging

from volcengine_ml_platform.innerapi.base_client import define_inner_api
from volcengine_ml_platform.innerapi.base_client import InnerApiBaseClient


define_inner_api("InnerCreateModel")
define_inner_api("InnerGetModelVersion")
define_inner_api("InnerUpdateModelVersion")


class ModelInnerApiClient(InnerApiBaseClient):
    def __init__(self):
        super().__init__()

    def create_model(
        self,
        model_name: str,
        model_format: str,
        model_type: str,
        path: str,
        token: str,
        model_id=None,
        description=None,
        tensor_config=None,
        model_metrics=None,
        model_category=None,
        dataset_id=None,
        source_type="TOS",
        base_model_version_id=None,
    ):
        """create models

        Args:
            model_name (str): models's name
            model_format (str): models's format, can be 'SavedModel', 'GraphDef','TorchScript','PTX',
                    'CaffeModel','NetDef','MXNetParams','Scikit_Learn','XGBoost','TensorRT','ONNX',or 'Custom'
            model_type (str): The type of the ModelVersion, examples: 'TensorFlow:2.0'
            path (str): source storage path
            model_id (str, optional): model_id, a new models will be created if not given. Defaults to None.
            description (str, optional): description to the models. Defaults to None.
            tensor_config (dict, optional): tensor config of the models.
            model_metrics (list, optional): list of models metrics.
            model_category (str, optional): category of the model.
                values can be 'TextClassification', 'TabularClassification', 'TabularRegression', 'ImageClassification'
            dataset_id (str, optional): id of the dataset based on which the model is trained
            source_type (str, optional): storage type. Defaults to 'TOS'.
            token (str): The secure token
            base_model_version_id (str, optional): perf转换任务生成的模型，所基于的模型版本ID

        Raises:
            Exception: failed to create models

        Returns:
            json response
        """
        try:
            body = {
                "ModelName": model_name,
                "VersionInfo": {
                    "ModelFormat": model_format,
                    "ModelType": model_type,
                    "Path": path,
                    "SourceType": source_type,
                },
            }
            if description is not None:
                body["VersionInfo"].update({"Description": description})

            if model_id is not None:
                body.update({"ModelID": model_id})

            if tensor_config is not None:
                body["VersionInfo"].update({"TensorConfig": tensor_config})

            if model_metrics is not None:
                body["VersionInfo"].update({"MetricsList": model_metrics})

            if model_category is not None:
                body.update({"ModelCategory": model_category})

            if dataset_id is not None:
                body.update({"DatasetID": dataset_id})

            if base_model_version_id is not None:
                body["VersionInfo"].update(
                    {"BaseModelVersionID": base_model_version_id}
                )

            res_json = self.common_json_handler(
                api="InnerCreateModel", body=body, token=token
            )
            return res_json
        except Exception as e:
            logging.error("Failed to create models, error: %s", e)
            raise Exception("create_model failed") from e

    def get_model_version(self, model_version_id: str, token: str):
        """get certain version of a models

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            token (str): The secure token

        Raises:
            Exception: raise on get model version failed

        Returns:
            json response
        """
        body = {"ModelVersionID": model_version_id}

        try:
            res_json = self.common_json_handler(
                api="InnerGetModelVersion", body=body, token=token
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get model version, model_version_id: %s, error: %s",
                model_version_id,
                e,
            )
            raise Exception("Get model version failed") from e

    def update_model_version(
        self,
        model_version_id: str,
        token: str,
        description=None,
        tensor_config=None,
        model_metrics=None,
    ):
        """update models version

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            token (str): The secure token
            description (str, optional): New Description of the ModelVersion. Defaults to None.
            tensor_config (dict, optional): tensor config of the model.
            model_metrics (list, optional): list of models metrics.

        Raises:
            Exception: raise on update model version failed

        Returns:
            json response
        """
        body = {
            "ModelVersionID": model_version_id,
        }
        if description is not None:
            body.update({"Description": description})

        if tensor_config is not None:
            body.update({"TensorConfig": tensor_config})

        if model_metrics is not None:
            body.update({"MetricsList": model_metrics})
        try:
            res_json = self.common_json_handler(
                api="InnerUpdateModelVersion",
                body=body,
                token=token,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to update model version, model_version_id: %s, error: %s",
                model_version_id,
                e,
            )
            raise Exception("Update model version failed") from e
