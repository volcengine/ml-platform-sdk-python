import os

from volcengine_ml_platform.config import constants


class Env:

    @staticmethod
    def get_tos_endpoint_url(region):
        return constants.TOS_REGION_ENDPOINT_URL[region]

    @staticmethod
    def get_encrypted_key():
        return os.getenv(constants.ENCRYPTED_KEY_ENV_NAME)

    @staticmethod
    def get_service_direct_host():
        return constants.SERVICE_DIRECT_HOST

    @staticmethod
    def get_session_token():
        return os.environ['SESSION_TOKEN']

    @staticmethod
    def get_service_name():
        if 'SERVICE_NAME' in os.environ:
            return os.environ['SERVICE_NAME']
        return constants.SERVICE_NAME

    @staticmethod
    def get_service_version():
        if 'SERVICE_VERSION' in os.environ:
            return os.environ['SERVICE_VERSION']
        return constants.SERVICE_VERSION

    @staticmethod
    def get_service_host():
        if 'SERVICE_HOST' in os.environ:
            return os.environ['SERVICE_HOST']
        return constants.SERVICE_HOST
