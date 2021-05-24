# coding:utf-8

import os

DATASET_LOCAL_METADATA_FILENAME = 'local_metadata.manifest'

SERVICE_NAME = 'ml_platform'
SERVICE_VERSION = '2021-10-01'
SERVICE_HOST = 'open.volcengineapi.com'
SERVICE_REGION = 'cn-north-1'

TOS_REGION_ENDPOINT_URL = {'cn-north-1': 'http://tos-s3-cn-qingdao.volces.com'}


class Config:

    def __init__(self, region):
        self.ak = ''
        self.sk = ''
        self.region = region

    def set_ak(self, ak):
        self.ak = ak

    def set_sk(self, sk):
        self.sk = sk

    def get_access_key_id(self):
        if self.ak != '':
            return self.ak
        return os.environ['ACCESS_KEY_ID']

    def get_secret_access_key(self):
        if self.sk != '':
            return self.sk
        return os.environ['SECRET_ACCESS_KEY']

    def get_service_region(self):
        if self.region != '':
            return self.region
        if 'SERVICE_REGION' in os.environ:
            return os.environ['SERVICE_REGION']
        return SERVICE_REGION

    @staticmethod
    def get_session_token():
        return os.environ['SESSION_TOKEN']

    @staticmethod
    def get_service_name():
        if 'SERVICE_NAME' in os.environ:
            return os.environ['SERVICE_NAME']
        return SERVICE_NAME

    @staticmethod
    def get_service_version():
        if 'SERVICE_VERSION' in os.environ:
            return os.environ['SERVICE_VERSION']
        return SERVICE_VERSION

    @staticmethod
    def get_service_host():
        if 'SERVICE_HOST' in os.environ:
            return os.environ['SERVICE_HOST']
        return SERVICE_HOST

    @staticmethod
    def get_tos_region():
        if 'TOS_REGION' in os.environ:
            return os.environ['TOS_REGION']
        return SERVICE_REGION

    @staticmethod
    def get_tos_endpoint_url():
        if 'TOS_ENDPOINT_URL' in os.environ:
            return os.environ['TOS_ENDPOINT_URL']
        return TOS_REGION_ENDPOINT_URL[Config.get_tos_region()]
