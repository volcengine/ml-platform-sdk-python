import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk.config import config


class ModelService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
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
        super(ModelService, self).__init__(self.service_info, self.api_info)

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
                        self.conf.get_service_region()), 10, 10, "https")

    def get_api_info(self):
        api_info = {
            "CreateModel":
                ApiInfo("POST", "/api/v1/model_versions/create", {
                    "Action": "CreateModel",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "ListModels":
                ApiInfo("GET", "/api/v1/models/list", {
                    "Action": "ListModels",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "DeleteModel":
                ApiInfo("GET", "/api/v1/models/delete", {
                    "Action": "DeleteModel",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "ListModelVersions":
                ApiInfo("GET", "/api/v1/model_versions/list", {
                    "Action": "ListModelVersions",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "GetModelVersion":
                ApiInfo("GET", "/api/v1/model_versions/describe", {
                    "Action": "GetModelVersion",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "DeleteModelVersion":
                ApiInfo("GET", "/api/v1/model_versions/delete", {
                    "Action": "DeleteModelVersion",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
            "UpdateModelVersion":
                ApiInfo("POST", "/api/v1/model_versions/update", {
                    "Action": "UpdateModelVersion",
                    "Version": self.conf.get_service_version()
                }, {}, {}),
        }
        return api_info

    def create_model(self, model_name, model_format, model_type, path,
                     create_new_model=False,
                     description=None,
                     source_type="TOS"):
        try:
            body = {
                "ModelName": model_name,
                "NewModelFlag": create_new_model,
                "ModelFormat": model_format,
                "ModelType": model_type,
                "Path": path,
                "SourceType": source_type,
            }
            if description is not None:
                body.update({"Description": description})

            res = self.json(api="CreateModel", params=dict(), body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('create_model failed') from e

    def list_models(self,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend',
                    model_name_contains=None):
        params = {
            "Offset": offset,
            "Limit": page_size,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }
        if model_name_contains:
            params.update({"ModelNameContains": model_name_contains})

        try:
            res = self.get(api="ListModels", params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('list_models failed') from e

    def delete_model(self, model_id):
        params = {
            "ModelId": model_id,
        }
        try:
            res = self.get(api="DeleteModel", params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('delete_model failed') from e

    def list_model_versions(self, model_name=None, model_id=None):
        params = dict()
        if model_name is not None:
            params['ModelName'] = model_name
        if model_id is not None:
            params['ModelId'] = model_id

        try:
            res = self.get(api='ListModelVersions', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('list_model_versions failed') from e

    def get_model_version(self, model_name=None, model_version=None, model_version_id=None):
        params = dict()
        if model_name is not None:
            params['ModelName'] = model_name
        if model_version is not None:
            params['ModelVersion'] = model_version
        if model_version_id is not None:
            params['ModelVersionId'] = model_version_id

        try:
            res = self.get(api='GetModelVersion', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_model_version failed') from e

    def delete_model_version(self, model_name=None, model_version=None, model_version_id=None):
        params = dict()
        if model_name is not None:
            params['ModelName'] = model_name
        if model_version is not None:
            params['ModelVersion'] = model_version
        if model_version_id is not None:
            params['ModelVersionId'] = model_version_id

        try:
            res = self.get(api="DeleteModelVersion", params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('delete_model_version failed') from e

    def update_model_version(self, model_version_id, description=None):
        body = {
            "ModelVersionId": model_version_id,
        }
        if description is not None:
            body.update({"Description": description})
        try:
            res = self.json(api="UpdateModelVersion", params=dict(), body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('update_model_version failed') from e
