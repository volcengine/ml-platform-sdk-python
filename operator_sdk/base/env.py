import json
import logging
import os

SERVICE_NAME = 'ml_platform'
SERVICE_VERSION = '2021-10-01'
SERVICE_HOST = 'open.volcengineapi.com'
SERVICE_REGION = 'cn-north-1'
# TOS_ENDPOINT_URL = 'http://tos-s3-cn-qingdao-inner.ivolces.com'
TOS_ENDPOINT_URL = 'http://tos-s3-cn-qingdao.volces.com'


class Config:

    def __init__(self):
        if 'NODE_CONFIG' in os.environ:
            config_str = os.environ['NODE_CONFIG']
            self.config = json.loads(config_str)
        else:
            logging.error('NODE_CONFIG not found')

    def get_node_id(self):
        return self.config['id']

    def get_input_slots(self):
        return self.config['inputs']

    def get_output_slots(self):
        return self.config['outputs']

    def get_params(self):
        return self.config['config']['parameters']

    @staticmethod
    def get_access_key_id():
        return os.environ['ACCESS_KEY_ID']

    @staticmethod
    def get_secret_access_key():
        return os.environ['SECRET_ACCESS_KEY']

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
    def get_service_region():
        if 'SERVICE_REGION' in os.environ:
            return os.environ['SERVICE_REGION']
        return SERVICE_REGION

    @staticmethod
    def get_tos_region():
        if 'TOS_REGION' in os.environ:
            return os.environ['TOS_REGION']
        return SERVICE_REGION

    @staticmethod
    def get_tos_endpoint_url():
        if 'TOS_ENDPOINT_URL' in os.environ:
            return os.environ['TOS_ENDPOINT_URL']
        return TOS_ENDPOINT_URL
