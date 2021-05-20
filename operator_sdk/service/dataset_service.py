import json

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from operator_sdk.base import env


class DatasetService(Service):

    def __init__(self, region: str, ak: str, sk: str):
        config = env.Config()
        self.host = config.get_service_host()
        self.region = region
        self.service = config.get_service_name()
        self.version = config.get_service_version()

        self.service_info = self.get_service_info()
        self.api_info = self.get_api_info()
        super(DatasetService, self).__init__(self.service_info, self.api_info)
        self.set_ak(ak)
        self.set_sk(sk)

    def get_service_info(self):
        return ServiceInfo(self.host, {'Accept': 'application/json'},
                           Credentials('', '', self.service, self.region), 10,
                           10, "https")

    def get_api_info(self):
        api_info = {
            "CreateDataset":
                ApiInfo("POST", "/", {
                    "Action": "CreateDataset",
                    "Version": self.version
                }, {}, {}),
            "UpdateDataset":
                ApiInfo("POST", "/", {
                    "Action": "UpdateDataset",
                    "Version": self.version
                }, {}, {}),
            "GetDataset":
                ApiInfo("GET", "/", {
                    "Action": "GetDataset",
                    "Version": self.version
                }, {}, {}),
            "DeleteDataset":
                ApiInfo("GET", "/", {
                    "Action": "DeleteDataset",
                    "Version": self.version
                }, {}, {}),
            "ListDatasets":
                ApiInfo("GET", "/", {
                    "Action": "ListDatasets",
                    "Version": self.version
                }, {}, {}),
        }
        return api_info

    def common_json_handler(self, api, body):
        params = dict()
        try:
            body = json.dumps(body)
            res = self.json(api, params, body)
            res_json = json.loads(res)
            return res_json
        # pylint: disable=W0703
        except Exception as e:
            res = str(e)
            res_json = json.loads(res)
            return res_json

    def create_dataset(self, body):
        try:
            res_json = self.common_json_handler("CreateDataset", body)
            return res_json
        except Exception as e:
            raise Exception('create_dataset failed') from e

    def update_dataset(self, body):
        try:
            res_json = self.common_json_handler("UpdateDataset", body)
            return res_json
        except Exception as e:
            raise Exception('update_dataset failed') from e

    def get_dataset(self, dataset_id):
        params = {'DatasetID': dataset_id}
        try:
            res = self.get(api='GetDataset', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('get_dataset failed') from e

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'

client = DatasetService(region, ak, sk)
print(client.get_dataset('d-20210511152528-j6mwv'))