# type: ignore
import logging

from volcengine_ml_platform.innerapi.base_client import InnerApiBaseClient
from volcengine_ml_platform.innerapi.base_client import define_inner_api


define_inner_api("GetSTSToken")


class STSApiClient(InnerApiBaseClient):
    def __init__(self):
        super().__init__()
    
    def get_sts_token(self, token, duration=3600):
        body = {"Duration": duration}

        try:
            res_json = self.common_json_handler(
                api="GetSTSToken",
                body=body,
                token=token
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get sts token, token: %s, error: %s",
                token,
                e,
            )
            raise Exception("get_sts_token failed") from e
