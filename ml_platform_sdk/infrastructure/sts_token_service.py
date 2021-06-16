import json
import logging
import threading
import time

from ml_platform_sdk.base.direct_apiinfo import DirectApiInfo
from ml_platform_sdk.base.direct_service import DirectService, DirectServiceInfo
from ml_platform_sdk.config import config


class STSTokenService(DirectService):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, duration, region='cn-north-1'):
        self.conf = config.Config(region)
        self.duration = duration
        self.api_info = self.get_api_info()
        self.service_info = self.get_service_info()
        super().__init__(self.service_info, self.api_info)

    def get_sts_token(self):
        encrypted_key = self.conf.get_encrypted_key()
        if encrypted_key is None:
            raise Exception('no encrypted key in environment variable')

        params = {'EncryptCode': encrypted_key, 'Duration': self.duration}

        try:
            resp = self.get(api='GetSTSToken', params=params)
            res_json = json.loads(resp)
            return res_json
        except Exception as e:
            logging.error('Failed to get sts token, error: %s', e)
            raise Exception('get_sts_token failed') from e

    def get_service_info(self):
        headers = {
            'Accept': 'application/json',
            'X-Top-Request-Id': '%d' % time.time(),
            'X-Top-Service': self.conf.get_service_name(),
            'X-Top-Region': self.conf.region
        }
        return DirectServiceInfo(self.conf.get_service_direct_host(), headers,
                                 10, 10, "http")

    @staticmethod
    def get_api_info():
        api_info = {
            'GetSTSToken': DirectApiInfo('GET', '/GetSTSToken', {}, {}, {}),
        }
        return api_info
