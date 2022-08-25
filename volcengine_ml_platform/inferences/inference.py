import logging
from typing import Optional
from volcengine_ml_platform.openapi import inference_service_client


# TODO 去掉model_version_id
class InferenceService:
    """提供推理服务"""

    def __init__(self):
        self.inference_service_client = (inference_service_client.InferenceServiceClient())

    def create(
        self,
        service_name: str,
        replicas: int,
        flavor_id: str,
        envs: list,
        service_description: Optional[str] = None,
        model_id: Optional[str] = None,
        model_version_id: Optional[str] = None,
        image_id: Optional[str] = None,
        image_version: Optional[str] = None,
        image_type: Optional[str] = None,
        image_url: Optional[str] = None,
        registry_username: Optional[str] = None,
        registry_token: Optional[str] = None,
        command: Optional[str] = None,
        ports: Optional[list] = None,
        vpc_id: Optional[str] = None,
        subnet_id: Optional[str] = None,
        enable_eip: Optional[bool] = False,
        eip_id: Optional[str] = None,
        readiness_enabled: Optional[bool] = False,
        readiness_command: Optional[str] = None,
        failure_threshold: Optional[int] = 3,
        period_seconds: Optional[int] = 10,
        resource_group_id: Optional[str] = None,
        resource_queue_id: Optional[str] = None,
    ):

        try:
            result = self.inference_service_client.create_service(
                service_name,
                replicas,
                flavor_id,
                envs,
                service_description,
                model_id,
                model_version_id,
                image_id,
                image_version,
                image_type,
                image_url,
                registry_username,
                registry_token,
                command,
                ports,
                vpc_id,
                subnet_id,
                enable_eip,
                eip_id,
                readiness_enabled,
                readiness_command,
                failure_threshold,
                period_seconds,
                resource_group_id,
                resource_queue_id,
            )["Result"]
            return result
        except Exception as e:
            logging.warning("Inference failed to create")
            raise Exception("Inference is invalid") from e

    def update(
        self,
        service_id: str,
        service_description: Optional[str] = None,
        flavor_id: Optional[str] = None,
        model_id: Optional[str] = None,
        model_version_id: Optional[str] = None,
        image_id: Optional[str] = None,
        image_version: Optional[str] = None,
        image_type: Optional[str] = None,
        image_url: Optional[str] = None,
        registry_username: Optional[str] = None,
        registry_token: Optional[str] = None,
        envs: Optional[list] = None,
        command: Optional[str] = None,
        ports: Optional[list] = None,
        vpc_id: Optional[str] = None,
        subnet_id: Optional[str] = None,
        enable_eip: Optional[bool] = False,
        eip_id: Optional[str] = None,
        readiness_enabled: Optional[bool] = False,
        readiness_command: Optional[str] = None,
        failure_threshold: Optional[int] = 3,
        period_seconds: Optional[int] = 10,
    ):
        try:
            self.inference_service_client.update_service(service_id, service_description, flavor_id, model_id,
                                                         model_version_id, image_id, image_version, image_type,
                                                         image_url, registry_username, registry_token, envs, command,
                                                         ports, vpc_id, subnet_id, enable_eip, eip_id,
                                                         readiness_enabled, readiness_command, failure_threshold,
                                                         period_seconds)
        except Exception as e:
            logging.warning("Inference failed to update")
            raise Exception("Inference is invalid") from e

    def delete(self, service_id: str):
        try:
            self.inference_service_client.delete_service(service_id=service_id)
        except Exception as e:
            logging.warning("Inference failed to undeploy")
            raise Exception("Inference is invalid") from e

    def stop(self, service_id: str):
        try:
            self.inference_service_client.stop_service(service_id=service_id)
        except Exception as e:
            logging.warning("Inference failed to stop")
            raise Exception("Inference is invalid") from e

    def start(self, service_id: str):
        try:
            self.inference_service_client.start_service(service_id=service_id)
        except Exception as e:
            logging.warning("Inference failed to start")
            raise Exception("Inference is invalid") from e

    def scale(self, service_id: str, replicas: int):
        try:
            self.inference_service_client.scale_service(
                service_id=service_id,
                replicas=replicas,
            )
        except Exception as e:
            logging.warning("Inference failed to scale")
            raise Exception("Inference is invalid") from e

    def get(self, service_id: str):
        return self.inference_service_client.get_service(service_id=service_id)["Result"]

    def list(
            self,
            service_name: str = None,
            service_name_contains: str = None,
            resource_group_id: str = None,
            resource_queue_id: str = None,
            status: str = None,
            states: list = None,
            offset=0,
            page_size=10,
            sort_by="CreateTime",
            sort_order="Descend",
    ):
        return self.inference_service_client.list_services(
            service_name,
            service_name_contains,
            resource_group_id,
            resource_queue_id,
            status,
            states,
            offset,
            page_size,
            sort_by,
            sort_order,
        )["Result"]

