import json
import time
from typing import Optional
import logging

from volcengine_ml_platform import initializer
from volcengine_ml_platform.config import credential as auth_credential
from volcengine_ml_platform.openapi import client, handle_res


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
        self.service_id = None
        self.service_status = None
        self.service_version_id = None
        self.endpoint_url = None
        self.replicas = None
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
            self.service_id = self.api_client.create_service(
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
                replica=self.replica)['Result']['ServiceID']
        except Exception as e:
            logging.warning('Inference failed to create')
            raise Exception('Inference is invalid') from e

    def _sync(self):
        result = self.api_client.get_service(
            service_id=self.service_id)['Result']
        self.service_id = result['ServiceID']
        self.model_id = result['ServiceDeployment']['Model']['ModelID']
        self.model_version_id = result['ServiceDeployment']['Model'][
            'ModelVersionID']
        self.model_version = result['ServiceDeployment']['Model']['Version']
        self.model_type = result['ServiceDeployment']['Model']['Type']
        self.model_path = result['ServiceDeployment']['Model']['Path']
        self.model_name = result['ServiceDeployment']['Model']['Name']
        self.service_status = result['ServiceDeployment']['Status']
        self.endpoint_url = result['ServiceDeployment']['EndpointURL']
        self.replicas = result['ServiceDeployment']['Replicas']
        self.service_version_id = result['ServiceDeployment'][
            'ServiceVersionID']

    def print(self):
        self._sync()

        json_output = dict()
        json_output['service_id'] = self.service_id
        json_output['endpoint_url'] = self.endpoint_url
        json_output['replicas'] = self.replicas
        json_output['service_status'] = self.service_status
        json_output['model'] = dict()
        json_output['model']['name'] = self.model_name
        json_output['model']['version'] = self.model_version
        json_output['model']['type'] = self.model_type
        json_output['model']['path'] = self.model_path
        print(json.dumps(json_output, indent='\t'))

    def delete(self):
        if self.service_id is None:
            logging.warning('service not exists')
            raise ValueError
        try:
            self.api_client.delete_service(service_id=self.service_id)
        except Exception as e:
            logging.warning('Inference failed to undeploy')
            raise Exception('Inference is invalid') from e

    def stop(self):
        if self.service_id is None:
            logging.warning('service not exists')
            raise ValueError
        try:
            self.api_client.stop_service(service_id=self.service_id)
            self._sync()
        except Exception as e:
            logging.warning('Inference failed to stop')
            raise Exception('Inference is invalid') from e

    def start(self):
        if self.service_id is None:
            logging.warning('service not exists')
            raise ValueError
        try:
            self.api_client.start_service(service_id=self.service_id)
            self._sync()
        except Exception as e:
            logging.warning('Inference failed to start')
            raise Exception('Inference is invalid') from e

    def scale(self,
              replicas: Optional[int] = None,
              flavor: Optional[str] = None):
        flavor_id = None
        if flavor:
            flavor_id = handle_res.get_unique_flavor(
                self.api_client.list_resource(name=flavor))
        try:
            self.api_client.scale_service(service_id=self.service_id,
                                          replicas=replicas,
                                          flavor_id=flavor_id)
            self._sync()
        except Exception as e:
            logging.warning('Inference failed to scale')
            raise Exception('Inference is invalid') from e

    # TODO
    def predict(self, data: Optional[dict] = None):
        self._sync()
        # do not support predict now
