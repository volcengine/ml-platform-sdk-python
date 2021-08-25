# -*- coding: utf-8 -*-

import json
import logging
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.util import id_gen


class MLSTSTokenResponse:

    class ResponseMetadata:

        def __init__(self, resp_json_meta):
            self.RequestId = resp_json_meta['RequestId']
            self.Action = resp_json_meta['Action']
            self.Version = resp_json_meta['Version']
            self.Service = resp_json_meta['Service']
            self.Region = resp_json_meta['Region']

    class Result:

        def __init__(self, resp_json_result):
            self.ExpiredTime = resp_json_result['ExpiredTime']
            self.CurrentTime = resp_json_result['CurrentTime']
            self.AccessKeyId = resp_json_result['AccessKeyId']
            self.SecretAccessKey = resp_json_result['SecretAccessKey']
            self.SessionToken = resp_json_result['SessionToken']

    def __init__(self, resp_json):
        self.resp_json = resp_json
        self.ResponseMetadata = self.ResponseMetadata(
            resp_json['ResponseMetadata'])
        self.Result = self.Result(resp_json['Result'])

    def get_raw_json(self):
        return self.resp_json


class MLSTSTokenService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, duration, region=constant.DEFAULT_REGION):
        self.region = region
        self.duration = duration
        self.api_info = self.get_api_info()
        self.service_info = self.get_service_info()
        super(MLSTSTokenService, self).__init__(self.service_info,
                                                self.api_info)

    def get_sts_token(self):
        encrypted_key = volcengine_ml_platform.get_encrypted_key()
        if encrypted_key is None:
            raise Exception('no encrypted key in environment variable')

        params = {'EncryptCode': encrypted_key, 'Duration': self.duration}

        try:
            self.service_info.header = self.get_latest_header()
            resp = self.get(api='GetSTSToken', params=params)
            resp_json = json.loads(resp)
            resp_ret = MLSTSTokenResponse(resp_json)
            return resp_ret
        except Exception as e:
            logging.error('Failed to get sts token, error: %s', e)
            raise Exception('get_sts_token failed') from e

    def get_service_info(self):
        return ServiceInfo(volcengine_ml_platform.get_service_direct_host(),
                           self.get_latest_header(),
                           volcengine_ml_platform.get_credentials(), 10, 10,
                           'http')

    def get_latest_header(self):
        headers = {
            'Accept': 'application/json',
            'X-Top-Request-Id': id_gen.gen_req_id(),
            'X-Top-Service': volcengine_ml_platform.get_service_name(),
            'X-Top-Region': self.region,
            'X-Top-Account-Id': '0',  # Not used in sts service
        }
        return headers

    @staticmethod
    def get_api_info():
        api_info = {
            'GetSTSToken': ApiInfo('GET', '/GetSTSToken', {}, {}, {}),
        }
        return api_info


if __name__ == '__main__':
    s = MLSTSTokenService(duration=1600)
    print(s.get_sts_token().Result.SessionToken)
