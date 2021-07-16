import time
from typing import Optional
import logging

from ml_platform_sdk import initializer
from ml_platform_sdk.config import credential as auth_credential
from ml_platform_sdk.openapi import client


class _Inference:

    def __init__(self,
                 service_name: str,
                 image_url: str,
                 flavor_id: str,
                 model_name: str,
                 model_id: str,
                 model_version_id: str,
                 model_version: int,
                 model_path: str,
                 model_type: str,
                 envs=None,
                 replica: Optional[int] = 1,
                 description: Optional[str] = None,
                 credential: Optional[auth_credential.Credential] = None):
        self.service_name = service_name
        self.image_url = image_url
        self.flavor_id = flavor_id
        self.model_name = model_name
        self.model_id = model_id
        self.model_version_id = model_version_id
        self.model_version = model_version
        self.model_path = model_path
        self.model_type = model_type
        self.envs = envs
        self.replica = replica
        self.description = description
        self.credential = credential or initializer.global_config.get_credential(
        )
        self.api_client = client.APIClient(credential)

    def create(self):
        if self.model_id is None or self.model_version_id is None:
            logging.warning('inference model is invalid')
            raise ValueError
        if self.envs is None:
            self.envs = list()

        try:
            self.api_client.create_service(
                service_name='sdk-create-{}'.format(int(time.time())),
                image_url=self.image_url,
                flavor_id=self.flavor_id,
                envs=self.envs,
                model_name=self.model_name,
                model_version=self.model_version,
                model_version_id=self.model_version_id,
                model_id=self.model_id,
                model_type=self.model_type,
                model_path=self.model_path,
                description=self.description,
                replica=self.replica)
        except Exception as e:
            logging.warning('Inference failed to create')
            raise Exception('Inference is invalid') from e
