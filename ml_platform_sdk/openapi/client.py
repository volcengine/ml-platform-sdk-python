import json
import threading
import logging
from typing import Optional

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk import initializer
from ml_platform_sdk.config import credential as auth_credential, env


class APIClient(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, credential: Optional[auth_credential.Credential] = None):
        self.credential = credential or initializer.global_config.get_credential(
        )
        self.service_info = self.get_service_info()
        self.api_info = self.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(APIClient, self).__init__(self.service_info, self.api_info)

    def get_service_info(self):
        return ServiceInfo(
            env.Env.get_service_host(), {'Accept': 'application/json'},
            Credentials(self.credential.get_access_key_id(),
                        self.credential.get_secret_access_key(),
                        env.Env.get_service_name(),
                        self.credential.get_region()), 10, 10, "https")

    def get_api_info(self):
        api_info = {
            "CreateDataset":
                ApiInfo(
                    "POST", "/", {
                        "Action": "CreateDataset",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            "UpdateDataset":
                ApiInfo(
                    "POST", "/", {
                        "Action": "UpdateDataset",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            "GetDataset":
                ApiInfo(
                    "GET", "/", {
                        "Action": "GetDataset",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            "DeleteDataset":
                ApiInfo(
                    "GET", "/", {
                        "Action": "DeleteDataset",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            "ListDatasets":
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListDatasets",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'DeleteModel':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteModel',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListModels':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListModels',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetModel':
                ApiInfo('GET', '/', {
                    'Action': 'GetModel',
                    'Version': env.Env.get_service_version()
                }, {}, {}),
            'CreateModel':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'CreateModel',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetModelNextVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetModelNextVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'DeleteModelVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteModelVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListModelVersions':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListModelVersions',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'UpdateModelVersion':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateModelVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetModelVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetModelVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'UpdateService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'CreateService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'CreateService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'UpdateServiceVersionDescription':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateServiceVersionDescription',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListServiceImages':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServiceImages',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListServices':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServices',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'StopService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'StopService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListServiceVersions':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServiceVersions',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'StartService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'StartService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'DeleteService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'RollbackServiceVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListModelServiceInstances':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetModelServiceInstanceStatus':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetTOSUploadPath':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetTOSUploadPath',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ListResource':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListResource',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
        }
        return api_info

    def list_resource(self,
                      name: Optional[str] = None,
                      name_contains: Optional[str] = None):
        params = {}
        if name:
            params.update({'Name': name})
        if name_contains:
            params.update({'NameContains': name_contains})
        try:
            res = self.get(api='ListResource', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('list_resource failed') from e

    def get_tos_upload_path(self, service_name: str, path=None):
        """

        Args:
            service_name:
            path:

        Returns:

        """
        params = {'ServiceName': service_name}
        if path:
            params.update({'Path': path})

        try:
            res = self.get(api='GetTOSUploadPath', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_model_next_version failed') from e

    def create_dataset(self, body):
        try:
            res_json = self.common_json_handler("CreateDataset", body)
            return res_json
        except Exception as e:
            logging.error('Failed to create datasets, error: %s', e)
            raise Exception('create_dataset failed') from e

    def update_dataset(self, body):
        try:
            res_json = self.common_json_handler("UpdateDataset", body)
            return res_json
        except Exception as e:
            logging.error('Failed to update datasets, error: %s', e)
            raise Exception('update_dataset failed') from e

    def get_dataset(self, dataset_id):
        params = {'DatasetID': dataset_id}
        try:
            res = self.get(api='GetDataset', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get datasets info, dataset_id: %s, error: %s',
                dataset_id, e)
            raise Exception('get_dataset failed') from e

    def list_datasets(self):
        params = {}
        try:
            res = self.get(api='ListDatasets', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            logging.error('Failed to list datasets, error: %s', e)
            raise Exception('list_datasets failed') from e

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

    def get_model_next_version(self, model_id=None):
        """

        Args:
            model_id:

        Returns:

        """
        params = {}
        if model_id:
            params.update({'ModelID': model_id})

        try:
            res = self.get(api='GetModelNextVersion', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_model_next_version failed') from e

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
                            model_id: str,
                            model_version: int = None,
                            offset=0,
                            page_size=10,
                            sort_by='CreateTime',
                            sort_order='Descend'):
        """list model versions with given model_id

        Args:
            model_id (str): model id
            model_version:
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
        if model_version:
            params.update({'ModelVersion': model_version})

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

    def create_service(self,
                       service_name: str,
                       model_name: str,
                       model_id: str,
                       model_version_id: str,
                       image_url: str,
                       flavor_id: str,
                       envs: list,
                       model_version: Optional[int] = None,
                       model_path: Optional[str] = None,
                       model_type: Optional[str] = None,
                       replica: Optional[int] = 1,
                       cluster_id: Optional[str] = 'cc3gpncvqtofppg3tqam0',
                       description: Optional[str] = None) -> dict:
        """create inference service for model

        Args:
            service_name (str): service name
            model (Model): Model object
            image_url (str): container image url
            flavor_id (str): hardward standard id
            envs (list): environment variables
            replica (int, optional): replica number. Defaults to 1.
            description (str, optional): description of service. Defaults to None.

        Raises:
            Exception: create_service failed

        Returns:
            json response
        """
        try:
            body = {
                'ServiceName': service_name,
                'ClusterID': cluster_id,
                'ServiceDeployment': {
                    'Replicas': replica,
                    'FlavorID': flavor_id,
                    'Model': {
                        'ModelID': model_id,
                        'ModelVersionID': model_version_id,
                        'Name': model_name,
                        'Version': model_version,
                        'Path': model_path,
                        'Type': model_type,
                    },
                    'Image': {
                        'URL': image_url,
                    },
                    'Envs': envs
                }
            }
            if description is not None:
                body['ServiceDeployment'].update({'Description': description})
            res = self.json(api='CreateService',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('create_service failed') from e

    def delete_service(self, service_id: str) -> dict:
        """delete service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: delete_service failed

        Returns:
            json response
        """
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='DeleteService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('delete_service failed') from e

    def start_service(self, service_id: str) -> dict:
        """start service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: start_service failed

        Returns:
            json response
        """
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='StartService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('start_service failed') from e

    def stop_service(self, service_id: str) -> dict:
        """stop service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: stop_service failed

        Returns:
            json response
        """
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='StopService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('start_service failed') from e

    def scale_service(self, service_id: str, replicas: int,
                      flavor_id: str) -> dict:
        """scale service by changing the number of replicas

        Args:
            service_id (str): service id
            replicas (int): number of replicas
            flavor_id (str): hardware standard

        Raises:
            Exception: scale_service failed

        Returns:
            json response
        """
        change_type = 'ScalingService'

        try:
            body = {
                'ServiceID': service_id,
                'Replicas': replicas,
                'FlavorID': flavor_id,
                'ChangeType': change_type
            }

            res = self.json(api='UpdateService',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('scale_service failed') from e

    # TODO
    def update_service(self):
        pass

    def update_service_version_description(self):
        pass
