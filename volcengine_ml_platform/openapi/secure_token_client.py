import logging

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api("GetSecureToken")
define_api("AdminGetSecureToken")


class SecureTokenClient(BaseClient):
    def __init__(self):
        super().__init__()

    def get_secure_token(
        self,
        module_name,
        time_to_live=30,
    ) -> dict:
        """get secure token to perform some operation

        Args:
            module_name (str): module name, eg: inference, customtask
            time_to_live (int): ttl of token, equals to 30 by default
        Raises:
            Exception: get_secure_token failed

        Returns:
            json response
        """
        try:
            body = {
                "ModuleName": module_name,
                "TimeToLive": time_to_live,
            }

            res_json = self.common_json_handler(api="GetSecureToken", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to get secure token, error: %s", e)
            raise Exception("get_secure_token failed") from e
