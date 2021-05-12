import os
import json


class Config:

    def __init__(self):
        config_str = os.environ['NODE_CONFIG']
        self.config = json.loads(config_str)

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
        return os.environ['SERVICE_NAME']

    @staticmethod
    def get_service_version():
        return os.environ['SERVICE_VERSION']

    @staticmethod
    def get_service_host():
        return os.environ['SERVICE_HOST']

    @staticmethod
    def get_service_region():
        return os.environ['SERVICE_REGION']

    @staticmethod
    def get_tos_region():
        return os.environ['TOS_REGION']

    @staticmethod
    def get_tos_endpoint_url():
        return os.environ['TOS_ENDPOINT_URL']
