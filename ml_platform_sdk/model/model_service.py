import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk.config import config


class ModelRepoService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, region='cn-north-1'):
        self.conf = config.Config(region)
        self.service_info = self.get_service_info()
        self.api_info = self.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(ModelRepoService, self).__init__(self.service_info, self.api_info)

    def set_ak(self, ak):
        self.conf.set_ak(ak)
        self.service_info.credentials.set_ak(ak)

    def set_sk(self, sk):
        self.conf.set_sk(sk)
        self.service_info.credentials.set_sk(sk)

    def get_service_info(self):
        return ServiceInfo(
            self.conf.get_service_host(), {'Accept': 'application/json'},
            Credentials('', '', self.conf.get_service_name(),
                        self.conf.get_service_region()), 10, 10, 'https')

    def get_api_info(self):
        api_info = {
            'DeleteModel':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteModel',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListModels':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListModels',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'GetModel':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetModel',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'CreateModel':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'CreateModel',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'DeleteModelVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteModelVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListModelVersions':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListModelVersions',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'UpdateModelVersion':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateModelVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'GetModelVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetModelVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
        }
        return api_info

    def create_model(self,
                     model_name: str,
                     model_format: str,
                     model_type: str,
                     path: str,
                     model_id=None,
                     description=None,
                     source_type='TOS'):
        """create model

        Args:
            model_name (str): model's name
            model_format (str): model's format, can be 'SavedModel', 'GraphDef','TorchScript','PTX',
                    'CaffeModel','NetDef','MXNetParams','Scikit_Learn','XGBoost','TensorRT','ONNX',or 'Custom'
            model_type (str): The type of the ModelVersion, examples: 'TensorFlow:2.0'
            path (str): source storage path
            model_id (str, optional): model_id, a new model will be created if not given. Defaults to None.
            description (str, optional): description to the model. Defaults to None.
            source_type (str, optional): storage type. Defaults to 'TOS'.

        Raises:
            Exception: failed to create model

        Returns:
            json response
        """
        try:
            body = {
                'ModelName': model_name,
                'VersionInfo': {
                    'ModelFormat': model_format,
                    'ModelType': model_type,
                    'Path': path,
                    'SourceType': source_type,
                }
            }
            if description is not None:
                body['VersionInfo'].update({'Description': description})

            if model_id is not None:
                body.update({'ModelID': model_id})

            res = self.json(api='CreateModel',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('create_model failed') from e

    def list_models(self,
                    model_name=None,
                    model_name_contains=None,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend'):
        """list models

        Args:
            model_name (str, optional): model name
            model_name_contains (str, optional): filter option, check if
                                model name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list model exception

        Returns:
            json response
        """
        params = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if model_name:
            params.update({'ModelName': model_name})

        if model_name_contains:
            params.update({'ModelNameContains': model_name_contains})

        try:
            res = self.get(api='ListModels', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('list_models failed') from e

    def delete_model(self, model_id: str):
        """delete model with given model id

        Args:
            model_id (str): model id

        Raises:
            Exception: raise on delete_model failed

        Returns:
            json response
        """
        params = {
            'ModelID': model_id,
        }
        try:
            res = self.get(api='DeleteModel', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('delete_model failed') from e

    def get_model(self, model_id: str):
        """get model with given model id

        Args:
            model_id (str): model id

        Raises:
            Exception: raise on get_model failed

        Returns:
            json response
        """
        params = {
            'ModelID': model_id,
        }
        try:
            res = self.get(api='GetModel', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_model failed') from e

    def list_model_versions(self,
                            model_id,
                            offset=0,
                            page_size=10,
                            sort_by='CreateTime',
                            sort_order='Descend'):
        """list model versions with given model_id

        Args:
            model_id (str): model id
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_model_versions failed

        Returns:
            json response
        """
        params = {
            'ModelID': model_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order
        }

        try:
            res = self.get(api='ListModelVersions', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('list_model_versions failed') from e

    def get_model_version(self, model_id: str, model_version_id: str):
        """get certain version of a model

        Args:
            model_id (str): model id
            model_version_id (str): model version id

        Raises:
            Exception: get_model_version failed

        Returns:
            json response
        """
        params = {'ModelID': model_id, 'ModelVersionID': model_version_id}

        try:
            res = self.get(api='GetModelVersion', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_model_version failed') from e

    def delete_model_version(self, model_id: str, model_version_id: str):
        """delete certain version of a model

        Args:
            model_id (str): model id
            model_version_id (str): model version id

        Raises:
            Exception: delete_model_version failed

        Returns:
            json response
        """
        params = {'ModelID': model_id, 'ModelVersionID': model_version_id}

        try:
            res = self.get(api='DeleteModelVersion', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('delete_model_version failed') from e

    def update_model_version(self, model_version_id, description=None):
        """update model version description

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            description (str, optional): New Description of the ModelVersion. Defaults to None.

        Raises:
            Exception: update_model_version failed

        Returns:
            json response
        """
        body = {
            'ModelVersionID': model_version_id,
        }
        if description is not None:
            body.update({'Description': description})
        try:
            res = self.json(api='UpdateModelVersion',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('update_model_version failed') from e
