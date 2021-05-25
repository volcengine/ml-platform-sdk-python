import json
import threading
import os
import logging
import tempfile

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk.config import config
from ml_platform_sdk.dataset.dataset import Dataset


class DatasetService(Service):
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
        super(DatasetService, self).__init__(self.service_info, self.api_info)

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
            "CreateDataset":
                ApiInfo(
                    "POST", "/", {
                        "Action": "CreateDataset",
                        "Version": self.conf.get_service_version()
                    }, {}, {}),
            "UpdateDataset":
                ApiInfo(
                    "POST", "/", {
                        "Action": "UpdateDataset",
                        "Version": self.conf.get_service_version()
                    }, {}, {}),
            "GetDataset":
                ApiInfo(
                    "GET", "/", {
                        "Action": "GetDataset",
                        "Version": self.conf.get_service_version()
                    }, {}, {}),
            "DeleteDataset":
                ApiInfo(
                    "GET", "/", {
                        "Action": "DeleteDataset",
                        "Version": self.conf.get_service_version()
                    }, {}, {}),
            "ListDatasets":
                ApiInfo(
                    "GET", "/", {
                        "Action": "ListDatasets",
                        "Version": self.conf.get_service_version()
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
            logging.error('Failed to create dataset, error: %s', e)
            raise Exception('create_dataset failed') from e

    def update_dataset(self, body):
        try:
            res_json = self.common_json_handler("UpdateDataset", body)
            return res_json
        except Exception as e:
            logging.error('Failed to update dataset, error: %s', e)
            raise Exception('update_dataset failed') from e

    def get_dataset(self, dataset_id):
        params = {'DatasetID': dataset_id}
        try:
            res = self.get(api='GetDataset', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get dataset info, dataset_id: %s, error: %s',
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

    def download_dataset(self, dataset_id: str, output_dir: str) -> Dataset:
        output_dir = os.path.join(output_dir, dataset_id)
        os.makedirs(output_dir, exist_ok=True)
        try:
            resp = self.get_dataset(dataset_id=dataset_id)
        except Exception as e:
            raise Exception(
                'Failed to get dataset info with dataset_id: {}'.format(
                    dataset_id)) from e
        dataset = Dataset(ak=self.conf.get_access_key_id(),
                          sk=self.conf.get_secret_access_key(),
                          region=self.conf.get_tos_region(),
                          remote_url=resp['Result']['StoragePath'],
                          local_dir=output_dir)
        try:
            dataset.download()
        except Exception as e:
            logging.error(
                'Failed to download dataset, dataset_id: %s, error: %s',
                dataset_id, e)
            raise Exception('download_dataset failed') from e
        return dataset

    def split_dataset(self,
                      training_dir,
                      testing_dir,
                      dataset_id='',
                      dataset=None,
                      ratio=0.8,
                      random_state=0):
        if dataset is None:
            with tempfile.TemporaryDirectory() as tmpdir:
                try:
                    dataset = self.download_dataset(dataset_id, tmpdir)
                    dataset.split(training_dir, testing_dir, ratio,
                                  random_state)
                except Exception as e:
                    logging.error('Failed to split dataset, error: %s', e)
                    raise Exception('split_dataset failed') from e
        else:
            try:
                dataset.split(training_dir, testing_dir, ratio, random_state)
            except Exception as e:
                logging.error('Failed to split dataset, error: %s', e)
                raise Exception('split_dataset failed') from e
