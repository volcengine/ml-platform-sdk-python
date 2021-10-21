import json
import logging
import requests
import threading

from typing import Dict
from typing import Union

from volcengine.ApiInfo import ApiInfo

import volcengine_ml_platform
from volcengine_ml_platform import constant
from volcengine_ml_platform.util import metric


INNER_API_INFOS = {}


BodyDict = Dict[str, Union[str, int]]


def define_inner_api(name, method="POST"):
    header = {"Content-Type": "application/json"}
    stress_flag = volcengine_ml_platform.get_stress_flag()
    if stress_flag is not None and len(stress_flag.strip()) > 0:
        header.update({"X-Tt-Stress": stress_flag.strip()})

    api_info = ApiInfo(
        method,
        "/",
        {
            "Action": name,
            "Version": constant.SERVICE_VERSION,
        },
        {},
        header,
    )
    
    INNER_API_INFOS[name] = api_info


define_inner_api("InnerGetTOSUploadPath")


class InnerApiBaseClient:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.inner_api_info = INNER_API_INFOS
        self.connection_timeout = 10
        self.socket_timeout = 10
        self.session = requests.session()

    @staticmethod
    def _get_url(api, token):
        region = volcengine_ml_platform.get_credentials().region
        host = volcengine_ml_platform.get_inner_api_service_host()
        return f"https://{host}/ml-platform/{region}/api/{api}?Token={token}"

    def common_json_handler(self, api, body, token):
        start_time = metric.current_ts()
        
        if api not in self.inner_api_info:
            raise Exception("no such inner api")

        res_json = {}

        try:
            url = self._get_url(api, token)
            headers = self.inner_api_info[api].header
            body = json.dumps(body)
            resp = self.session.post(
                url,
                headers=headers,
                data=body,
                timeout=(
                    self.connection_timeout,
                    self.socket_timeout,
                ),
            )

            if resp.status_code != 200:
                raise Exception(resp.text)
        
            res_json = resp.json()   
        except Exception as e:
            msg = "time-cost(ms)={}, The server returns an error: api={}, error={}".format(
                metric.cost_time(start_time),
                api,
                json.dumps(res_json),
            )
            logging.error(msg)
            raise e

        err = res_json["ResponseMetadata"].get("Error", None)
        if err is not None:
            msg = "time-cost(ms)={}, The server returns an error: api={}, error={}".format(
                metric.cost_time(start_time),
                api,
                json.dumps(err),
            )
            logging.error(msg)
            raise Exception(msg) from err
        return res_json

    def get_tos_upload_path(self, service_name: str, token: str, path=None):
        """
        Args:
            service_name (str): server name
            token (str): The secure token
            path:

        Returns:

        """
        body: BodyDict = {"ServiceName": service_name}
        if path:
            body.update({"Path": path})

        try:
            res_json = self.common_json_handler(
                api="InnerGetTOSUploadPath",
                body=body,
                token=token,
            )
            return res_json
        except Exception as e:
            logging.error("Failed to InnerGetTOSUploadPath, error: %s", e)
            raise Exception("InnerGetTOSUploadPath failed") from e
