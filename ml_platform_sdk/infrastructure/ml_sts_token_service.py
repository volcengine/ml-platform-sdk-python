import json
import logging
import threading
import time

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk.config import config


class MLSTSTokenService(Service):
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
        super(MLSTSTokenService, self).__init__(self.service_info,
                                                self.api_info)

    def get_sts_token(self):
        encrypted_key = self.conf.get_encrypted_key()
        if encrypted_key is None:
            raise Exception('no encrypted key in environment variable')

        params = {'EncryptCode': encrypted_key, 'Duration': self.duration}

        try:
            self.service_info.header = self.get_latest_header()
            resp = self.get(api='GetSTSToken', params=params)
            resp_json = json.loads(resp)
            resp_ret = {
                'ResponseMetadata': {
                    'RequestId': resp_json['ResponseMetadata']['RequestId'],
                    'Action': resp_json['ResponseMetadata']['Action'],
                    'Version': resp_json['ResponseMetadata']['Version'],
                    'Service': resp_json['ResponseMetadata']['Service'],
                    'Region': resp_json['ResponseMetadata']['Region']
                },
                'Result': {
                    'ExpiredTime': resp_json['Result']['ExpiredTime'],
                    'CurrentTime': resp_json['Result']['CurrentTime'],
                    'AccessKeyId': resp_json['Result']['AccessKeyId'],
                    'SecretAccessKey': resp_json['Result']['SecretAccessKey'],
                    'SessionToken': resp_json['Result']['SessionToken']
                }
            }
            return resp_ret
        except Exception as e:
            logging.error('Failed to get sts token, error: %s', e)
            raise Exception('get_sts_token failed') from e

    def get_service_info(self):
        return ServiceInfo(
            self.conf.get_service_direct_host(), self.get_latest_header(),
            Credentials('', '', self.conf.get_service_name(),
                        self.conf.get_service_region()), 10, 10, "http")

    def get_latest_header(self):
        headers = {
            'Accept': 'application/json',
            'X-Top-Request-Id': '%d' % time.time(),
            'X-Top-Service': self.conf.get_service_name(),
            'X-Top-Region': self.conf.region
        }
        return headers

    @staticmethod
    def get_api_info():
        api_info = {
            'GetSTSToken': ApiInfo('GET', '/GetSTSToken', {}, {}, {}),
        }
        return api_info
