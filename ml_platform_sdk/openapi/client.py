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
from ml_platform_sdk.openapi.handle_res import handle_res


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
            'UpdateModel':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateModel',
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
                    'GET', '/', {
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
                        'Action': 'ListModelServiceInstances',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetModelServiceInstanceStatus':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetModelServiceInstanceStatus',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'ModifyService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ModifyService',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetTOSUploadPath':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetTOSUploadPath',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'CreateResource':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'CreateResource',
                        'Version': env.Env.get_service_version()
                    }, {}, {}),
            'GetResource':
                ApiInfo(
                    "GET", "/", {
                        "Action": "GetResource",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'DeleteResource':
                ApiInfo(
                    "GET", "/", {
                        "Action": "DeleteResource",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'ListResource':
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListResource",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'GetSTSToken':
                ApiInfo(
                    "GET", "/", {
                        "Action": "GetSTSToken",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'ListAnnotationSets':
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListAnnotationSets",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'UpdateAnnotationLabel':
                ApiInfo(
                    "POST", "/", {
                        "Action": "UpdateAnnotationLabel",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'GetAnnotationSet':
                ApiInfo(
                    "GET", "/", {
                        "Action": "GetAnnotationSet",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'DeleteAnnotationSet':
                ApiInfo(
                    "GET", "/", {
                        "Action": "DeleteAnnotationSet",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'CreateAnnotaionSet':
                ApiInfo(
                    "POST", "/", {
                        "Action": "CreateAnnotaionSet",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'UpdateAnnotationData':
                ApiInfo(
                    "POST", "/", {
                        "Action": "UpdateAnnotationData",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'ListAnnotationDatas':
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListAnnotationDatas",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'TryDeleteAnnotationLabel':
                ApiInfo(
                    "POST", "/", {
                        "Action": "TryDeleteAnnotationLabel",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
            'ListAnnotationLabel':
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListAnnotationLabel",
                        "Version": env.Env.get_service_version()
                    }, {}, {}),
        }
        return api_info

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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to get model next version, error: %s', e)
            raise Exception('get_model_next_version failed') from e

    def create_dataset(self, body):
        try:
            res_json = self.common_json_handler("CreateDataset", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to create datasets, error: %s', e)
            raise Exception('create_dataset failed') from e

    def update_dataset(self, body):
        try:
            res_json = self.common_json_handler("UpdateDataset", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to update datasets, error: %s', e)
            raise Exception('update_dataset failed') from e

    def get_dataset(self, dataset_id):
        """Get a Dataset.

        Args:
            dataset_id (str, required): The unique ID of the Dataset
        Raises:
            Exception: failed to get dataset
        Returns:
            Dataset: json response

        """
        params = {'DatasetID': dataset_id}
        try:
            res = self.get(api='GetDataset', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get datasets info, dataset_id: %s, error: %s',
                dataset_id, e)
            raise Exception('get_dataset failed') from e

    def delete_dataset(self, dataset_id: str):
        """Delete a Dataset.

        Args:
            dataset_id (str, required): The unique ID of the Dataset
        Raises:
            Exception: failed to delete dataset
        Returns:
            Dataset: json response

        """
        params = {'DatasetID': dataset_id}
        try:
            res = self.get(api='DeleteDataset', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to delete dataset, dataset_id: %s, error: %s',
                          dataset_id, e)
            raise Exception('delete_dataset failed') from e

    def list_datasets(self,
                      name=None,
                      name_contains=None,
                      status=None,
                      offset=0,
                      page_size=10,
                      sort_by='CreateTime',
                      sort_order='Descend'):
        """list datasets

        Args:
            name (str, optional): dataset name
            name_contains (str, optional): filter option, check if
                                dataset name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'DatasetlName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        params = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if name:
            params.update({'Name': name})
        if name_contains:
            params.update({'NameContains': name_contains})
        if status:
            params.update({'Status': status})

        try:
            res = self.get(api='ListDatasets', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to create model, error: %s', e)
            raise Exception('create_model failed') from e

    def get_model_next_version(self, model_id=None):
        """get next model version with given model_id

        Args:
            model_id (str, required): The unique ID of the Model. 1 will return if not given

        Returns:
            next_version(int): The next version of the Model
        """

        params = {}
        if model_id:
            params.update({'ModelID': model_id})

        try:
            res = self.get(api='GetModelNextVersion', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get model next version, model_id: %s, error: %s',
                model_id, e)
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
            model_name (str, optional): certern model with return if given model name. Defaults to None.
            model_name_contains (str, optional): filter option, check if
                                model name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to None.
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list models, error: %s', e)
            raise Exception('list_models failed') from e

    def delete_model(self, model_id: str):
        """delete model with given model id

        Args:
            model_id (str): The unique ID of the Model

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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to delete model, model_id: %s, error: %s',
                          model_id, e)
            raise Exception('delete_model failed') from e

    def get_model(self, model_id: str):
        """get model with given model id

        Args:
            model_id (str): The unique ID of the Model

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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to get model, model_id: %s, error: %s',
                          model_id, e)
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
            model_id (str): The unique ID of the Model
            model_version: filter option, the certain ModelVersion of Model. Defaults to None.
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to list model versions, model_id: %s, error: %s',
                model_id, e)
            raise Exception('list_model_versions failed') from e

    def get_model_version(self, model_version_id: str):
        """get certain version of a model

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: get_model_version failed

        Returns:
            json response
        """
        params = {'ModelVersionID': model_version_id}

        try:
            res = self.get(api='GetModelVersion', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get model version, model_version_id: %s, error: %s',
                model_version_id, e)
            raise Exception('get_model_version failed') from e

    def delete_model_version(self, model_version_id: str):
        """delete certain version of a model

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: delete_model_version failed

        Returns:
            json response
        """
        params = {'ModelVersionID': model_version_id}

        try:
            res = self.get(api='DeleteModelVersion', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to delete model version, model_version_id: %s, error: %s',
                model_version_id, e)
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to update model version, model_version_id: %s, error: %s',
                model_version_id, e)
            raise Exception('update_model_version failed') from e

    def update_model(self, model_id, model_name=None):
        """update model_name with given model_id

        Args:
            model_id (str, required): The unique ID of the Model
            model_name(str, optional): New ModelName of the Model. Defaults to None.

        Raises:
            Exception: failed to update model

        Returns:
            Dataset: json response
        """
        body = {
            'ModelID': model_id,
        }
        if model_name is not None:
            body.update({'ModelName': model_name})
        try:
            res = self.json(api='UpdateModel',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to update model, model_id: %s, error: %s',
                          model_id, e)
            raise Exception('update_model failed') from e

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
            logging.error('Failed to create service, error: %s', e)
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to delete service, service_id: %s, error: %s',
                          service_id, e)
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to start service, service_id: %s, error: %s',
                          service_id, e)
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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to stop service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('stop_service failed') from e

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
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to scale service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('scale_service failed') from e

    def update_service(
        self,
        service_id: str,
        replicas: int,
        flavor_id: str,
        model_id: str,
        model_version_id: str,
        img_url: str,
        envs: list,
        change_type: str,
        img_description: str = None,
        img_version: str = None,
        img_type: str = None,
        service_description: str = None,
        model_name: str = None,
        model_version: int = None,
        model_type: str = None,
        model_path: str = None,
    ):
        body = {
            'ServiceID': service_id,
            'Replicas': replicas,
            'FlavorID': flavor_id,
            'Model': {
                'ModelID': model_id,
                'ModelVersionID': model_version_id,
            },
            'Image': {
                'URL': img_url,
            },
            'Envs': envs,
            'ChangeType': change_type
        }
        if service_description:
            body.update({'Description': service_description})
        if model_name:
            body['Model'].update({'Name': model_name})
        if model_version:
            body['Model'].update({'Version': model_version})
        if model_type:
            body['Model'].update({'Type': model_type})
        if model_path:
            body['Model'].update({'Path': model_path})

        if img_description:
            body['Image'].update({'Description': img_description})
        if img_version:
            body['Image'].update({'Version': img_version})
        if img_type:
            body['Image'].update({'Type': img_type})
        try:
            res = self.json(api='UpdateService',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to update service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('update_service failed') from e

    # TODO
    def update_service_version_description(self):
        pass

    def get_service(self, service_id: str):
        """get service with given service_id

        Args:
            service_id (str): The unique ID of the Service

        Raises:
            Exception: raise on get_service failed

        Returns:
            json response
        """
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='GetService', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to get service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('get_service failed') from e

    def list_service_images(self,
                            model_id: str,
                            model_version_id: str,
                            name: str = None,
                            version: int = None,
                            service_type: str = None,
                            path: str = None):
        params = {'ModelID': model_id, 'ModelVersionID': model_version_id}
        if name:
            params.update({'Name': name})
        if version:
            params.update({'Version': version})
        if service_type:
            params.update({'Type': service_type})
        if path:
            params.update({'Path': path})

        try:
            res = self.get(api='ListServiceImages', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list service images, error: %s', e)
            raise Exception('list_service_images failed') from e

    def list_services(self,
                      service_name: str = None,
                      service_name_contains: str = None,
                      offset=0,
                      page_size=10,
                      sort_by='CreateTime',
                      sort_order='Descend'):
        """list services

        Args:
            service_name (str, optional): service name
            service_name_contains (str, optional): filter option, check if
                                service name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServicelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        params = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if service_name:
            params.update({'ServiceName': service_name})
        if service_name_contains:
            params.update({'ServiceNameContains': service_name_contains})

        try:
            res = self.get(api='ListServices', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list services, error: %s', e)
            raise Exception('list_services failed') from e

    def list_service_versions(self,
                              service_id: str,
                              offset=0,
                              page_size=10,
                              sort_by='CreateTime',
                              sort_order='Descend'):
        """list service versions with given service_id

        Args:
            service_id (str): The unique ID of the Service
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServiceVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_service_versions failed

        Returns:
            json response
        """
        params = {
            'ServiceID': service_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }

        try:
            res = self.get(api='ListServiceVersions', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to list service versions, service_id: %s, error: %s',
                service_id, e)
            raise Exception('list_service_versions failed') from e

    def rollback_service_version(self, service_id: str,
                                 service_version_id: str):
        """Rollback a ServiceVersion with ServiceID and ServiceVersionID

        Args:
            service_id (str, required): The unique ID of the Service
            service_version_id(str, required): The unique ID of the ServiceVersion

        Raises:
            Exception: failed to rollback service version

        Returns:
            Dataset: json response
        """
        params = {
            'ServiceID': service_id,
            'ServiceVersionID': service_version_id
        }
        try:
            res = self.get(api='RollbackServiceVersion', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to rollback service version, service_id: %s, service_version_id: %s, error: %s',
                service_id, service_version_id, e)
            raise Exception('rollback_service_version failed') from e

    def list_model_service_instances(self,
                                     service_id: str,
                                     offset=0,
                                     page_size=10,
                                     sort_by='CreateTime',
                                     sort_order='Descend'):
        """list model service instances

        Args:
            service_id (str, optional): The unique ID of Service
            offset (int, optional): offset of service. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelServiceInstanceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        params = {
            'ServiceID': service_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }

        try:
            res = self.get(api='ListModelServiceInstances', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to list model service instances, service_id: %s, error: %s',
                service_id, e)
            raise Exception('list_model_service_instances failed') from e

    def get_model_service_instance_status(self, service_id: str,
                                          instance_id_list: list):
        """get the status of model service instance

        Args:
            service_id (str, required): The unique ID of Service
            offset (list, required): instance id list

        Raises:
            Exception: get model service instance status exception

        Returns:
            json response
        """
        params = {'ServiceID': service_id, 'InstanceIDList': instance_id_list}

        try:
            res = self.get(api='GetModelServiceInstanceStatus', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get model service instance status, service_id: %s, error: %s',
                service_id, e)
            raise Exception('get_model_service_instance_status failed') from e

    def create_resource(
        self,
        name: str,
        resource_type: str,
        v_cpu: float,
        memory: str,
        gpu_type: str,
        gpu_num: float,
        price: float,
        region: str,
    ):
        """create resource

        Args:
            name (str): resource name
            resource_type : The type of resource
            v_cpu (str): The cpu num of resource
            memory (str): resource memory
            gpu_type (str): The gpu type of resource
            gpu_num (float): The gpu num of resource
            price (float): resource price
            region (str): The region of resource

        Raises:
            Exception: create_resource failed

        Returns:
            json response
        """
        body = {
            'Name': name,
            'Type': resource_type,
            'vCPU': v_cpu,
            'Memory': memory,
            'GPUType': gpu_type,
            'GPUNum': gpu_num,
            'Price': price,
            'Region': region
        }

        try:
            res_json = self.common_json_handler("CreateResource", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to create resource, error: %s', e)
            raise Exception('create_resource failed') from e

    def get_resource(self, flavor_id: str):
        """get resource with given flavor_id

        Args:
            flavor_id (str): The unique ID of the Resource

        Raises:
            Exception: raise on get_resource failed

        Returns:
            json response
        """
        params = {'FlavorID': flavor_id}

        try:
            res = self.get(api='GetResource', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get resource info, flavor_id: %s, error: %s',
                flavor_id, e)
            raise Exception('get_resource failed') from e

    def delete_resource(self, flavor_id: str):
        """delete resource with given flavor id

        Args:
            flavor_id (str): The unique ID of the Resource

        Raises:
            Exception: raise on delete_resource failed

        Returns:
            json response
        """
        params = {'FlavorID': flavor_id}

        try:
            res = self.get(api='DeleteResource', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to delete resource, flavor_id: %s, error: %s',
                          flavor_id, e)
            raise Exception('delete_resource failed') from e

    def list_resource(self,
                      name=None,
                      name_contains=None,
                      resource_type=None,
                      tag: list = None,
                      offset=0,
                      page_size=10,
                      sort_by='CreateTime',
                      sort_order='Descend'):
        """list resource with given service_id

        Args:
            name (str, optional): resource name
            name_contains (str, optional): filter option, check if
                                resource name contains given string. Defaults to None.
            resource_type (str, optional): filter option, check if
                                resource type equals to given string. Defaults to None.
            tag (list, optional): filter option, check if
                                resource tag in given list. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ResourceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_resource failed

        Returns:
            json response
        """
        params = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }

        if name:
            params.update({'Name': name})
        if name_contains:
            params.update({'NameContains': name_contains})
        if resource_type:
            params.update({'Type': resource_type})
        if tag:
            params.update({'Tag': tag})

        try:
            res = self.get(api='ListResource', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list resource, error: %s', e)
            raise Exception('list_resource failed') from e

    def get_sts_token(self, encrypt_code: str, duration: int = None):
        params = {'EncryptCode': encrypt_code}

        if duration:
            params.update({'Duration': duration})

        try:
            res = self.get(api='GetSTSToken', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get sts token, encrypt_code: %s, error: %s',
                encrypt_code, e)
            raise Exception('get_sts_token failed') from e

    def list_annotation_sets(self, dataset_id: str):
        """list annotation set with given dataset_id

        Args:
            dataset_id (str): The unique ID of Dataset

        Raises:
            Exception: list annotation sets exception

        Returns:
            json response
        """
        params = {'DatasetID': dataset_id}

        try:
            res = self.get(api='ListAnnotationSets', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to list annotation sets, dataset_id: %s, error: %s',
                dataset_id, e)
            raise Exception('list_annotation_sets failed') from e

    def update_annotation_label(self,
                                annotation_id: str,
                                labels: list,
                                default_label=None):
        body = {
            'AnnotationID': annotation_id,
            'Labels': labels,
        }
        if default_label:
            body.update({'DefaultLabel': default_label})

        try:
            res_json = self.common_json_handler("UpdateAnnotationLabel", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to update annotation label, annotation_id: %s, error: %s',
                annotation_id, e)
            raise Exception('update_annotation_label failed') from e

    def get_annotation_set(self, dataset_id: str, annotation_id: str):
        """get annotation with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: failed to get annotation

        Returns:
            json response
        """
        params = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res = self.get(api='GetAnnotationSet', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to get annotation set, dataset_id: %s, annotation_id: %s, error: %s',
                dataset_id, annotation_id, e)
            raise Exception('get_annotation_set failed') from e

    def delete_annotation_set(self, dataset_id: str, annotation_id: str):
        """delete annotation set with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: delete_annotation_set failed

        Returns:
            json response
        """
        params = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res = self.get(api='DeleteAnnotationSet', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to delete annotation set, dataset_id: %s, annotation_id: %s, error: %s',
                dataset_id, annotation_id, e)
            raise Exception('delete_annotation_set failed') from e

    def create_annotation_set(
        self,
        dataset_id: str,
        annotation_type: str,
        annotation_name: str,
        default_label: str = None,
        labels: list = None,
    ):
        """create annotation for dataset

        Args:
            dataset_id (str): The unique ID of Dataset
            annotation_type (Model): annotation type
            annotation_name (str): annotation name
            default_label (str, optional): default label of annotataion. Defaults fo None
            labels (list): labels of annotataion. Defaults fo None

        Raises:
            Exception: create_annotation_set failed

        Returns:
            json response
        """
        body = {
            'DatasetID': dataset_id,
            'AnnotationType': annotation_type,
            'AnnotationName': annotation_name
        }
        if default_label:
            body.update({'DefaultLabel': default_label})
        if labels:
            body.update({'Labels': labels})

        try:
            res_json = self.common_json_handler("CreateAnnotataionSet", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to create annotation set, error: %s', e)
            raise Exception('create_annotation_set failed') from e

    def update_annotation_data(self, annotation_id: str, datas: list):
        """update annotation_data with given annotation_id

        Args:
            annotation_id (str, required): The unique ID of the Annotation
            datas(str, required): New datas of the Annotation.

        Raises:
            Exception: failed to update annotataion_data

        Returns:
            Dataset: json response

        """
        body = {'AnnotationID': annotation_id, 'Datas': datas}

        try:
            res_json = self.common_json_handler("UpdateAnnotationData", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to update annotation data, annotation_id: %s, error: %s',
                annotation_id, e)
            raise Exception('update_annotation_data failed') from e

    def list_annotation_datas(self,
                              annotation_id: str,
                              label_names: list = None,
                              status: int = None,
                              offset=0,
                              page_size=10):
        """list annotation datas with given annotation_id

        Args:
            annotation_id (str): The unique ID of annotation
            label_names (list, optional): filter option, label_names. Defaults to None.
            status (str, optional): filter option, status.Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.

        Raises:
            Exception: list_annotation_datas failed

        Returns:
            json response
        """
        params = {
            'AnnotationID': annotation_id,
            'Offset': offset,
            'Limit': page_size,
        }
        if status:
            params.update({'Status': status})
        if label_names:
            params.update({'LabelNames': label_names})

        try:
            res = self.get(api='ListAnnotationDatas', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list annotation datas, error: %s', e)
            raise Exception('list_annotation_datas failed') from e

    def try_delete_annotation_label(self, annotation_id: str, label: object):
        body = {'AnnotationID': annotation_id, 'Label': label}

        try:
            res_json = self.common_json_handler("TryDeleteAnnotationLabel",
                                                body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to try delete annotation label, annotation_id: %s, error: %s',
                annotation_id, e)
            raise Exception('try_delete_annotation_label failed') from e

    def list_annotation_label(self, dataset_id: str, annotation_id: str):
        """list annotation label set with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: list_annotation_label failed

        Returns:
            json response

        """
        params = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res = self.get(api='ListAnnotationLabel', params=params)
            res_json = json.loads(res)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error('Failed to list annotation label, error: %s', e)
            raise Exception('list_annotation_label failed') from e

    def modify_service(self, service_name: str, service_id: str,
                       cluster_id: str):
        """Modify ServiceName with given ServiceID and ClusterID

        Args:
            service_name(str, required): New Name of the Service
            service_id (str, required): The unique ID of the Service
            cluster_id (str, required): The unique ID of the Cluster

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            'ServiceName': service_name,
            'ServiceID': service_id,
            'ClusterID': cluster_id
        }
        try:
            res_json = self.common_json_handler("ModifyService", body)
            return handle_res.handle_res(res_json)
        except Exception as e:
            logging.error(
                'Failed to modify service, service_id: %s, cluster_id: %s, error: %s',
                service_id, cluster_id, e)
            raise Exception('modify_service failed') from e
            return res_json
        except Exception as e:
            raise Exception('get_service failed') from e
