from ctypes import Union
import os
import logging
import datetime
from typing import Dict, List, Union
from volcengine_ml_platform import get_inner_api_token
from volcengine_ml_platform.util.retry import retry
from volcengine_ml_platform.innerapi.base_client import InnerApiBaseClient, define_inner_api
from volcengine_ml_platform.openapi.secure_token_client import SecureTokenClient


define_inner_api("CreateTkExperiment")
define_inner_api("CreateTkTrial")
define_inner_api("SetTkTrialConfig")
define_inner_api("SetTkTrialSummary")
define_inner_api("CreateTkTrialEntities")
define_inner_api("CreateTkTrialEntitySteps")


class Client(InnerApiBaseClient):

    def __init__(self):
        self.token = get_inner_api_token()
        super().__init__()

    @staticmethod
    def _get_endpoint():
        return os.environ['MLP_TRACKING_ENDPOINT']

    @staticmethod
    def _get_url(api, token):
        endpoint = Client._get_endpoint()
        token = get_inner_api_token()
        return f"http://{endpoint}/{api}?Token={token}"

    @retry(5, 1)
    def create_experiment(
        self,
        name: str,
        description: str = ""
    ) -> Dict:
        try:
            res_json = self.common_json_handler(
                "CreateTkExperiment",
                {
                    "Name": name,
                    "Description": description,
                },
                self.token,
            )
            result = res_json['Result']
            return result
        except Exception as e:
            logging.error("Failed to create tracking experiment, error: %s", e)
            raise Exception("create_experiment failed") from e

    @retry(5, 1)
    def create_trial(
        self,
        experiment_id: str,
        name: str,
        description: str = "",
        config: Dict[str, str] = {},
    ) -> Dict:
        # flatten config
        config = self._flatten_config(config)
        try:
            res_json = self.common_json_handler(
                "CreateTkTrial",
                {
                    "ExperimentId": experiment_id,
                    "Name": name,
                    "Description": description,
                    "Config": config,
                },
                self.token,
            )
            result = res_json['Result']
            return result
        except Exception as e:
            logging.error("Failed to create tracking trial, error: %s", e)
            raise Exception("create_trial failed") from e

    @retry(5, 1)
    def set_trial_config(
        self,
        experiment_id: str,
        trial_id: str,
        config: Dict[str, str] = {},
    ) -> None:
        # flatten config
        config = self._flatten_config(config)
        try:
            res_json = self.common_json_handler(
                "SetTkTrialConfig",
                {
                    "ExperimentId": experiment_id,
                    "TrialId": trial_id,
                    "Config": config,
                },
                self.token,
            )
            return res_json
        except Exception as e:
            logging.error("Failed to set tracking trial config, error: %s", e)
            raise Exception("set_trial_config failed") from e

    def _flatten_config(self, config, prefix=[], sep="."):
        _config = {}
        if not isinstance(config, dict):
            _config[sep.join(prefix)] = config
        else:
            for k, v in config.items():
                prefix.append(k)
                _config.update(self._flatten_config(v, prefix=prefix))
                del prefix[-1]
        return _config

    @retry(5, 1)
    def set_trial_summary(
        self,
        experiment_id: str,
        trial_id: str,
        summary: Dict[str, str] = {},
    ) -> None:
        try:
            res_json = self.common_json_handler(
                "SetTkTrialSummary",
                {
                    "ExperimentId": experiment_id,
                    "TrialId": trial_id,
                    "Summary": summary,
                },
                self.token,
            )
            return res_json
        except Exception as e:
            logging.error("Failed to set tracking trial summary, error: %s", e)
            raise Exception("set_trial_summary failed") from e

    @retry(5, 1)
    def create_trial_entities(
        self,
        experiment_id: str,
        trial_id: str,
        entities: List[Dict],
    ) -> None:
        '''
        entities:
            [
                {
                    "Name": "loss",
                    "Type": "scalar",
                    "CustomStep": "epoch"
                }
            ]
        '''
        try:
            res_json = self.common_json_handler(
                "CreateTkTrialEntities",
                {
                    "ExperimentId": experiment_id,
                    "TrialId": trial_id,
                    "Entities": entities,
                },
                self.token,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to create tracking trial entities, error: %s", e)
            raise Exception("create_trial_entities failed") from e

    @retry(5, 1)
    def create_trial_entity_steps(
        self,
        trial_id: str,
        steps: List[Dict],
    ) -> None:
        '''
        step:
            {
                "Step": 1,
                "Items: {
                    "loss": {
                        "Type": "scalar",
                        "Scalar": {
                            "Value": "0.1"
                        }
                    }
                }
            }
        '''
        try:
            res_json = self.common_json_handler(
                "CreateTkTrialEntitySteps",
                {
                    "TrialId": trial_id,
                    "Steps": steps,
                },
                self.token,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to create tracking trial entity steps, error: %s", e)
            raise Exception("create_trial_entity_items failed") from e

    @retry(5, 1)
    def get_tos_upload_path(self, path=[]) -> Union[str, str]:
        resp = super().get_tos_upload_path("tracking", self.token, path)
        result = resp['Result']
        return result['Bucket'], result['KeyPrefix']


if __name__ == "__main__":
    cli = Client()
    # print(cli._get_secure_token())
    # print(cli._flatten_config({
    #     'a1': {
    #         'b1': {
    #             'c1': 1,
    #             'c2': 2,
    #         },
    #         'b2': {
    #             'c3': 1,
    #             'c4': 2,
    #         },
    #     }
    # }))
    print(cli._flatten_config({'j': {'k': {'l': 1}}}))
