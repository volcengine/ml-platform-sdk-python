import json
import logging
from typing import Optional

from volcengine_ml_platform.openapi import inference_service_client


# TODO 去掉model_version_id
class InferenceService:
    """提供推理服务"""

    def __init__(
        self,
        service_name: str,
        image_id: str,
        flavor_id: str,
        model_id: str,
        model_version_id: str,
        envs=None,
        replica: Optional[int] = 1,
        description: Optional[str] = None,
    ):
        self.service_name = service_name
        self.service_id = None
        self.service_status = None
        self.service_version_id = None
        self.endpoint_url = None
        self.replicas = None
        self.image_id = image_id
        self.flavor_id = flavor_id
        self.model_id = model_id
        self.model_version_id = model_version_id
        self.model_version = None
        self.model_type = None
        self.model_path = None
        self.model_name = None
        self.envs = envs or {}
        self.replica = replica
        self.description = description
        self.inference_service_client = (
            inference_service_client.InferenceServiceClient()
        )

    def create(self):
        if self.model_id is None or self.model_version_id is None:
            logging.warning("inference models is invalid")
            raise ValueError

        envs = self._envs_dict_to_list(self.envs)
        try:
            self.service_id = self.inference_service_client.create_service(
                service_name=self.service_name,
                image_id=self.image_id,
                flavor_id=self.flavor_id,
                envs=envs,
                model_version_id=self.model_version_id,
                model_id=self.model_id,
                description=self.description,
                replica=self.replica,
            )["Result"]["ServiceID"]
        except Exception as e:
            logging.warning("Inference failed to create")
            raise Exception("Inference is invalid") from e

    def _sync(self):
        result = self.inference_service_client.get_service(service_id=self.service_id)[
            "Result"
        ]
        self.service_id = result["ServiceID"]
        self.model_id = result["ServiceDeployment"]["Model"]["ModelID"]
        self.model_version_id = result["ServiceDeployment"]["Model"]["ModelVersionID"]
        self.model_version = result["ServiceDeployment"]["Model"]["Version"]
        self.model_type = result["ServiceDeployment"]["Model"]["Type"]
        self.model_path = result["ServiceDeployment"]["Model"]["Path"]
        self.model_name = result["ServiceDeployment"]["Model"]["Name"]
        self.service_status = result["ServiceDeployment"]["Status"]
        self.endpoint_url = result["ServiceDeployment"]["EndpointURL"]
        self.replicas = result["ServiceDeployment"]["Replicas"]
        self.service_version_id = result["ServiceDeployment"]["ServiceVersionID"]
        self.envs = self._envs_list_to_dict(
            result["ServiceDeployment"].get("Envs", []),
        )

    def print(self):
        self._sync()

        json_output = {}
        json_output["service_id"] = self.service_id
        json_output["endpoint_url"] = self.endpoint_url
        json_output["replicas"] = self.replicas
        json_output["service_status"] = self.service_status
        json_output["models"] = {}
        json_output["models"]["name"] = self.model_name
        json_output["models"]["version"] = self.model_version
        json_output["models"]["type"] = self.model_type
        json_output["models"]["path"] = self.model_path
        json_output["envs"] = self.envs
        print(json.dumps(json_output, indent="\t"))

    def delete(self):
        if self.service_id is None:
            logging.warning("service not exists")
            raise ValueError
        try:
            self.inference_service_client.delete_service(
                service_id=self.service_id,
            )
        except Exception as e:
            logging.warning("Inference failed to undeploy")
            raise Exception("Inference is invalid") from e

    def stop(self):
        if self.service_id is None:
            logging.warning("service not exists")
            raise ValueError
        try:
            self.inference_service_client.stop_service(
                service_id=self.service_id,
            )
            self._sync()
        except Exception as e:
            logging.warning("Inference failed to stop")
            raise Exception("Inference is invalid") from e

    def start(self):
        if self.service_id is None:
            logging.warning("service not exists")
            raise ValueError
        try:
            self.inference_service_client.start_service(
                service_id=self.service_id,
            )
            self._sync()
        except Exception as e:
            logging.warning("Inference failed to start")
            raise Exception("Inference is invalid") from e

    def scale(self, replicas: int):
        try:
            if not self.service_id or not self.replicas:
                raise ValueError("Empty value(service_id or replicas)")
            self.inference_service_client.scale_service(
                service_id=self.service_id,
                replicas=replicas,
            )
            self._sync()
        except Exception as e:
            logging.warning("Inference failed to scale")
            raise Exception("Inference is invalid") from e

    # TODO
    def predict(self, data: Optional[dict] = None):
        self._sync()
        # do not support predict now

    def _envs_dict_to_list(self, envs):
        if isinstance(envs, list):
            return envs
        rvs = []
        for key in envs:
            rvs.append({"Name": key, "Value": str(envs[key])})
        return rvs

    def _envs_list_to_dict(self, envs):
        if isinstance(envs, dict):
            return envs
        rvs = {}
        for item in envs:
            rvs[item["Name"]] = item["Value"]
        return rvs
