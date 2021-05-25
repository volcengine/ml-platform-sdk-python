import json

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from operator_sdk.base import env


class ModelService(Service):

    def __init__(self, region: str, ak: str, sk: str):
        config = env.Config()
        self.host = config.get_service_host()
        self.region = region
        self.service = config.get_service_name()
        self.version = config.get_service_version()

        self.service_info = self.get_service_info()
        self.api_info = self.get_api_info()
        super(ModelService, self).__init__(self.service_info, self.api_info)
        self.set_ak(ak)
        self.set_sk(sk)

    def get_service_info(self):
        return ServiceInfo(self.host, {'Accept': 'application/json'},
                           Credentials('', '', self.service, self.region), 10,
                           10, "https")

    def get_api_info(self):
        api_info = {
            "CreateModel":
                ApiInfo("POST", "/api/v1/model_versions/create", {
                    "Action": "CreateModel",
                    "Version": self.version
                }, {}, {}),
            "ListModels":
                ApiInfo("GET", "/api/v1/models/list", {
                    "Action": "ListModels",
                    "Version": self.version
                }, {}, {}),
            "DeleteModel":
                ApiInfo("GET", "/api/v1/models/delete", {
                    "Action": "DeleteModel",
                    "Version": self.version
                }, {}, {}),
            "ListModelVersions":
                ApiInfo("GET", "/api/v1/model_versions/list", {
                    "Action": "ListModelVersions",
                    "Version": self.version
                }, {}, {}),
            "GetModelVersion":
                ApiInfo("GET", "/api/v1/model_versions/describe", {
                    "Action": "GetModelVersion",
                    "Version": self.version
                }, {}, {}),
            "DeleteModelVersion":
                ApiInfo("GET", "/api/v1/model_versions/delete", {
                    "Action": "DeleteModelVersion",
                    "Version": self.version
                }, {}, {}),
            "UpdateModelVersion":
                ApiInfo("POST", "/api/v1/model_versions/update", {
                    "Action": "UpdateModelVersion",
                    "Version": self.version
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
