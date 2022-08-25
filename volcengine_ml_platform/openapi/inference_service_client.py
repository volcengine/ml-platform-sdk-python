# mypy: ignore-errors
import logging
from typing import Optional

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api("UpdateService")
define_api("CreateService")
define_api("UpdateServiceVersionDescription")
define_api("ListServices")
define_api("StopService")
define_api("ListServiceVersions")
define_api("StartService")
define_api("DeleteService")
define_api("GetService")
define_api("RollbackServiceVersion")
define_api("ListInferenceServiceInstances")
define_api("GetInferenceServiceInstanceStatus")
define_api("ModifyService")


class InferenceServiceClient(BaseClient):

    def __init__(self):
        super().__init__()

    def create_service(
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
    ) -> dict:
        """create inference service for models

        Args:
            service_name (str): 推理服务名字
            replicas (int): 服务实例数量
            flavor_id (str): 服务所使用的计算规格ID。
            envs (list): 服务环境变量列表。
                列表每个元素格式: {"Name": str, "Value": str}
            service_description (str, optional): 服务描述信息。默认为None
            model_id (str, optinal): 服务部署的模型ID。默认为None
            model_version_id (str, optinal): 服务部署的模型版本ID。默认为None
            image_id (str, optional): 服务所使用的镜像ID。 默认为None
            image_version (str, optional): 服务所使用的镜像版本。 默认为None
            image_type (str, optional): 服务所使用的镜像版本。
                可选值: 'Preset', 'Custom', 'VolcEngine', 'Public'
            image_url (str, optional): 服务所使用的镜像URL。默认为None
            registry_username (str, optional): 服务所使用的镜像仓库的用户名。默认为None
            registry_token (str, optional): 服务所使用的镜像仓库的token。默认为None
            command (str, optional): 服务容器的入口命令。默认为None
            ports (list, optional): 服务监听端口列表。默认为None
                列表每个元素格式:
                {
                    "ListenPort": str,
                    "ExposePort": str,
                    "Type": str,
                }
                Type可选值: "HTTP", "RPC", "Metrics", "Other"
            vpc_id (str, optional): 对于需要跨VPC访问的服务, 服务客户端所在的VPC ID。默认为None
            subnet_id (str, optional): 对于需要跨VPC访问的服务, 服务客户端所在的子网ID。默认为None
            enable_eip (bool, optional): 对于需要跨VPC访问的服务, 是否开启公网访问。默认为False
            eip_id (str, optional): 对于需要跨VPC访问并且开启公网访问的服务, EIP ID。默认为None
            readiness_enabled (bool, optional): 是否开启健康检查。默认为False
            readiness_command (str, optional): 自定义健康检查命令。默认为None
            failure_threshold (int, optional): 自定义健康检查失败次数阈值。默认为3
            period_seconds (int, optional): 自定义健康检查间隔时间。默认为10s
            resource_group_id (str, optional): 资源组ID。默认为None
            resource_queue_id (str, optional): 资源组队列ID。默认为None
            

        Raises:
            Exception: create_service failed

        Returns:
            返回json格式的response, 包含模型相关信息。
            比如: ::
                {
                    "ResponseMetadata": {
                        "RequestId": "20220815174947010225145152058E51BE",
                        "Action": "CreateService",
                        "Version": "2021-10-01",
                        "Service": "ml_platform",
                        "Region": "cn-beijing"
                    },
                    "Result": {
                        "ServiceID": "s-20220815174947-n99pk",
                        "CurrentVersionID": 100000743
                    }
                }
        """
        try:
            body = {
                "ServiceName": service_name,
                "ServiceDeployment": {
                    "Replicas": replicas,
                    "FlavorID": flavor_id,
                    "Image": {},
                    "Envs": envs,
                },
            }
            if service_description is not None:
                body["ServiceDeployment"].update({"Description": service_description})
            if model_id:
                body["ServiceDeployment"].update({"Model": {
                    "ModelID": model_id,
                    "ModelVersionID": model_version_id,
                }})
            if image_id:
                body["ServiceDeployment"]["Image"].update({"Id": image_id})
            if image_version:
                body["ServiceDeployment"]["Image"].update({"Version": image_version})
            if image_type:
                body["ServiceDeployment"]["Image"].update({"Type": image_type})
            if image_url:
                body["ServiceDeployment"]["Image"].update({"Url": image_url})
            if registry_username:
                body["ServiceDeployment"]["Image"].update(
                    {"ImageCredential": {
                        "RegistryUsername": registry_username,
                        "RegistryToken": registry_token,
                    }})
            if resource_group_id:
                body["ServiceDeployment"].update({"ResourceGroupID": resource_group_id})
            if resource_queue_id:
                body["ServiceDeployment"].update({"ResourceQueueId": resource_queue_id})
            if command:
                body["ServiceDeployment"].update({"Command": command})
            if ports:
                body["ServiceDeployment"].update({"Ports": ports})
            if vpc_id:
                body["ServiceDeployment"].update(
                    {"Network": {
                        "VpcId": vpc_id,
                        "SubnetId": subnet_id,
                        "EnableEip": enable_eip,
                    }})
                if eip_id:
                    body["ServiceDeployment"]["Network"].update({"EipId": eip_id})
            if readiness_enabled or readiness_command or failure_threshold or period_seconds:
                body["ServiceDeployment"].update({"ReadinessProbe": {}})
                if readiness_enabled:
                    body["ServiceDeployment"]["ReadinessProbe"].update({"Enabled": readiness_enabled})
                if readiness_command:
                    body["ServiceDeployment"]["ServiceDeployment"]["ReadinessProbe"].update(
                        {"Command": readiness_command})
                if failure_threshold:
                    body["ServiceDeployment"]["ReadinessProbe"].update({"FailureThreshold": failure_threshold})
                if period_seconds:
                    body["ServiceDeployment"]["ReadinessProbe"].update({"PeriodSeconds": period_seconds})

            res_json = self.common_json_handler(api="CreateService", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to create service, error: %s", e)
            raise Exception("create_service failed") from e

    def modify_service(self, service_name: str, service_id: str, cluster_id: str):
        """Modify ServiceName with given ServiceID and ClusterID

        Args:
            service_name(str, required): New Name of the Service
            service_id (str, required): The unique ID of the Service
            cluster_id (str, required): The unique ID of the Cluster

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            "ServiceName": service_name,
            "ServiceID": service_id,
            "ClusterID": cluster_id,
        }
        try:
            res_json = self.common_json_handler("ModifyService", body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to modify service, service_id: %s, cluster_id: %s, error: %s",
                service_id,
                cluster_id,
                e,
            )
            raise Exception("modify_service failed") from e

    def delete_service(self, service_id: str) -> dict:
        """delete service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: delete_service failed

        Returns:
            json response
        """
        body = {"ServiceID": service_id}
        try:
            res_json = self.common_json_handler(api="DeleteService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to delete service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("delete_service failed") from e

    def start_service(self, service_id: str) -> dict:
        """start service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: start_service failed

        Returns:
            json response
        """
        body = {"ServiceID": service_id}
        try:
            res_json = self.common_json_handler(api="StartService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to start service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("start_service failed") from e

    def stop_service(self, service_id: str) -> dict:
        """stop service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: stop_service failed

        Returns:
            json response
        """
        body = {"ServiceID": service_id}
        try:
            res_json = self.common_json_handler(api="StopService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to stop service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("stop_service failed") from e

    def scale_service(self, service_id: str, replicas: int) -> dict:
        """scale service by changing the number of replicas

        Args:
            service_id (str): service id
            replicas (int): number of replicas

        Raises:
            Exception: scale_service failed

        Returns:
            json response
        """
        change_type = "ScalingService"

        try:
            body = {
                "ServiceID": service_id,
                "Replicas": replicas,
                "ChangeType": change_type,
            }

            res_json = self.common_json_handler(api="UpdateService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to scale service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("scale_service failed") from e

    def update_service(
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
        """更新推理服务

        Args:
            service_id (str): 推理服务ID
            service_description (str, optional): 服务描述信息。默认为None
            flavor_id (str, optional): 服务所使用的计算规格ID。默认为None
            model_id (str, optional): 服务部署的模型ID。默认为None
            model_version_id (str, optional): 服务部署的模型版本ID。默认为None
            image_id (str, optional): 服务所使用的镜像ID。 默认为None
            image_version (str, optional): 服务所使用的镜像版本。 默认为None
            image_type (str, optional): 服务所使用的镜像版本。
                可选值: 'Preset', 'Custom', 'VolcEngine', 'Public'
            image_url (str, optional): 服务所使用的镜像URL。默认为None
            registry_username (str, optional): 服务所使用的镜像仓库的用户名。默认为None
            registry_token (str, optional): 服务所使用的镜像仓库的token。默认为None
            envs (list): 服务环境变量列表。
                列表每个元素格式: {"Name": str, "Value": str}
            command (str, optional): 服务容器的入口命令。默认为None
            ports (list, optional): 服务监听端口列表。默认为None
                列表每个元素格式:
                {
                    "ListenPort": str,
                    "ExposePort": str,
                    "Type": str,
                }
                Type可选值: "HTTP", "RPC", "Metrics", "Other"
            vpc_id (str, optional): 对于需要跨VPC访问的服务, 服务客户端所在的VPC ID。默认为None
            subnet_id (str, optional): 对于需要跨VPC访问的服务, 服务客户端所在的子网ID。默认为None
            enable_eip (bool, optional): 对于需要跨VPC访问的服务, 是否开启公网访问。默认为False
            eip_id (str, optional): 对于需要跨VPC访问并且开启公网访问的服务, EIP ID。默认为None
            readiness_enabled (bool, optional): 是否开启健康检查。默认为False
            readiness_command (str, optional): 自定义健康检查命令。默认为None
            failure_threshold (int, optional): 自定义健康检查失败次数阈值。默认为3
            period_seconds (int, optional): 自定义健康检查间隔时间。默认为10s

        Raises:
            Exception: 推理服务更新异常

        Returns:
            返回json格式的response, 包含模型相关信息。
            比如: ::
                {
                    "ResponseMetadata": {
                        "RequestId": "2022081517555501022509900802F561E4",
                        "Action": "UpdateService",
                        "Version": "2021-10-01",
                        "Service": "ml_platform",
                        "Region": "cn-beijing"
                    },
                    "Result": {
                        "ServiceID": "s-20220815174947-n99pk",
                        "CurrentVersionID": 100000744,
                        "PreviousVersionID": 100000743
                    }
                }
        """
        body = {
            "ServiceID": service_id,
            "FlavorID": flavor_id,
            "Image": {},
        }
        if service_description:
            body.update({"Description": service_description})
        if flavor_id:
            body.update({"FlavorID": flavor_id})
        if model_id:
            body.update({"Model": {
                "ModelID": model_id,
                "ModelVersionID": model_version_id,
            }})
        if image_id:
            body["Image"].update({"Id": image_id})
        if image_version:
            body["Image"].update({"Version": image_version})
        if image_type:
            body["Image"].update({"Type": image_type})
        if image_url:
            body["Image"].update({"Url": image_url})
        if registry_username:
            body["Image"].update(
                {"ImageCredential": {
                    "RegistryUsername": registry_username,
                    "RegistryToken": registry_token,
                }})
        if envs:
            body.update({"Envs": envs})
        if command:
            body.update({"Command": command})
        if ports:
            body.update({"Ports": ports})
        if vpc_id:
            body.update({"Network": {
                "VpcId": vpc_id,
                "SubnetId": subnet_id,
                "EnableEip": enable_eip,
            }})
            if eip_id:
                body["Network"].update({"EipId": eip_id})
        if readiness_enabled or readiness_command or failure_threshold or period_seconds:
            body.update({"ReadinessProbe": {}})
            if readiness_enabled:
                body["ReadinessProbe"].update({"Enabled": readiness_enabled})
            if readiness_command:
                body["ReadinessProbe"].update({"Command": readiness_command})
            if failure_threshold:
                body["ReadinessProbe"].update({"FailureThreshold": failure_threshold})
            if period_seconds:
                body["ReadinessProbe"].update({"PeriodSeconds": period_seconds})
        try:
            res_json = self.common_json_handler(api="UpdateService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to update service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("update_service failed") from e

    def get_service(self, service_id: str):
        """get service with given service_id

        Args:
            service_id (str): The unique ID of the Service

        Raises:
            Exception: raise on get_service failed

        Returns:
            json response
        """
        body = {"ServiceID": service_id}
        try:
            res_json = self.common_json_handler(api="GetService", body=body)
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get service, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("get_service failed") from e

    def list_services(
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
        """list services

        Args:
            service_name (str, optional): service name
            service_name_contains (str, optional): filter option, check if
                                service name contains given string. Defaults to None.
            resource_group_id (str, optional): id of the resource group
            resource_queue_id (str, optional): id of the resource queue
            status (str, optional): status of the service
            states (list, optional): list of states of the service
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServiceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            "Offset": offset,
            "Limit": page_size,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }
        if service_name:
            body.update({"ServiceName": service_name})
        if service_name_contains:
            body.update({"ServiceNameContains": service_name_contains})
        if resource_group_id:
            body.update({"ResourceGroupId": resource_group_id})
        if resource_queue_id:
            body.update({"ResourceQueueId": resource_queue_id})
        if status:
            body.update({"Status": status})
        if states:
            body.update({"States": states})

        try:
            res_json = self.common_json_handler(api="ListServices", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to list services, error: %s", e)
            raise Exception("list_services failed") from e

    def list_service_versions(
        self,
        service_id: str,
        offset=0,
        page_size=10,
        sort_by="CreateTime",
        sort_order="Descend",
    ):
        """list service versions with given service_id

        Args:
            service_id (str): The unique ID of the Service
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServiceVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_service_versions failed

        Returns:
            json response
        """
        body = {
            "ServiceID": service_id,
            "Offset": offset,
            "Limit": page_size,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }

        try:
            res_json = self.common_json_handler(
                api="ListServiceVersions",
                body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to list service versions, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("list_service_versions failed") from e

    def rollback_service_version(self, service_id: str, service_version_id: str):
        """Rollback a ServiceVersion with ServiceID and ServiceVersionID

        Args:
            service_id (str, required): The unique ID of the Service
            service_version_id(str, required): The unique ID of the ServiceVersion

        Raises:
            Exception: failed to rollback service version

        Returns:
            Dataset: json response
        """
        body = {
            "ServiceID": service_id,
            "ServiceVersionID": service_version_id,
        }
        try:
            res_json = self.common_json_handler(
                api="RollbackServiceVersion",
                body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to rollback service version, service_id: %s, service_version_id: %s, error: %s",
                service_id,
                service_version_id,
                e,
            )
            raise Exception("rollback_service_version failed") from e

    def list_inference_service_instances(
        self,
        service_id: str,
        offset=0,
        page_size=10,
        sort_by="CreateTime",
        sort_order="Descend",
    ):
        """list service instances

        Args:
            service_id (str, optional): The unique ID of Service
            offset (int, optional): offset of service. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'InstanceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            "ServiceID": service_id,
            "Offset": offset,
            "Limit": page_size,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }

        try:
            res_json = self.common_json_handler(
                api="ListInferenceServiceInstances",
                body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to list inference service instances, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("list_inference_service_instances failed") from e

    def get_inference_service_instance_status(
        self,
        service_id: str,
        instance_id_list: list,
    ):
        """get the status of inference service instance

        Args:
            service_id (str, required): The unique ID of Service
            offset (list, required): instance id list

        Raises:
            Exception: get service instance status exception

        Returns:
            json response
        """
        body = {"ServiceID": service_id, "InstanceIDList": instance_id_list}

        try:
            res_json = self.common_json_handler(
                api="GetInferenceServiceInstanceStatus",
                body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get inference service instance status, service_id: %s, error: %s",
                service_id,
                e,
            )
            raise Exception("get_inference_service_instance_status failed",) from e
