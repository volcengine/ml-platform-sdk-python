# -*- coding: utf-8 -*-

import json
import logging
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from volcengine.auth.SignerV4 import SignerV4

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.util import metric

API_INFOS = {}


def define_api(name, method="POST"):
    header = {}
    stress_flag = volcengine_ml_platform.get_stress_flag()
    if stress_flag is not None and len(stress_flag.strip()) > 0:
        header.update("X-Tt-Stress", stress_flag.strip())

    API_INFOS[name] = ApiInfo(method, "/", {
        "Action": name,
        "Version": constant.SERVICE_VERSION
    }, {}, header)


define_api("GetTOSUploadPath")
define_api("GetSTSToken")


class BaseClient(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.service_info = ServiceInfo(
            volcengine_ml_platform.get_service_host(),
            {'Accept': 'application/json'},
            volcengine_ml_platform.get_credentials(), 10, 10, "http")
        self.api_info = API_INFOS
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(BaseClient, self).__init__(self.service_info, self.api_info)

    def common_json_handler(self, api, body):
        start_time = metric.current_ts()
        params = {}
        res_json = {}
        try:
            body = json.dumps(body)
            res_json = self.json2(api, params, body)
        except Exception as e:
            msg = "time-cost(ms)={}, The server returns an error: api={}, error={}".format(
                metric.cost_time(start_time), api, json.dumps(res_json))
            logging.error(msg)
            raise e

        err = res_json['ResponseMetadata'].get('Error', None)
        if err is not None:
            msg = "time-cost(ms)={}, The server returns an error: api={}, error={}".format(
                metric.cost_time(start_time), api, json.dumps(err))
            logging.error(msg)
            raise Exception(msg) from err
        return res_json

    def json2(self, api, params, body):
        if api not in self.api_info:
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        resp = self.session.post(url,
                                 headers=r.headers,
                                 data=r.body,
                                 timeout=(self.service_info.connection_timeout,
                                          self.service_info.socket_timeout))
        if resp.status_code == 200:
            return resp.json()
        raise Exception(resp.text)

    def get_tos_upload_path(self, service_name: str, path=None):
        """
        Args:
            service_name:
            path:

        Returns:

        """
        body = {'ServiceName': service_name}
        if path:
            body.update({'Path': path})

        try:
            res_json = self.common_json_handler(api='GetTOSUploadPath',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to GetTOSUploadPath, error: %s', e)
            raise Exception('GetTOSUploadPath failed') from e

    def get_sts_token(self, encrypt_code: str, duration: int = None):
        body = {'EncryptCode': encrypt_code}

        if duration:
            body.update({'Duration': duration})

        try:
            res_json = self.common_json_handler(api='GetSTSToken', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get sts token, encrypt_code: %s, error: %s',
                encrypt_code, e)
            raise Exception('get_sts_token failed') from e

    def get_unique_flavor(self, list_flavor_result):
        flavor_map = list_flavor_result['Result']['List']
        for _, v in flavor_map.items():
            if v and len(v):
                return v[0]['FlavorID']
        return ''
