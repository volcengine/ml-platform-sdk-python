import logging

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api("CreateCustomTask")
define_api("GetCustomTask")
define_api("ListCustomTasks")
define_api("StopCustomTask")
define_api("DeleteCustomTask")
define_api("ListCustomTaskTimelines")
define_api("GetCustomTaskInstances")


class CustomTaskClient(BaseClient):
    def __init__(self):
        super().__init__()

    def list_custom_task_timelines(self, custom_task_id: str):
        body = {"CustomTaskId": custom_task_id}
        try:
            res_json = self.common_json_handler("ListCustomTaskTimelines", body)
            return res_json
        except Exception as e:
            logging.error("Failed to list custom task timelines, error: %s", e)
            raise Exception("list custom task timelines failed") from e

    def list_custom_tasks(
        self,
        task_name: str = None,
        task_filter: str = None,
        task_id: str = None,
        resource_group_id: str = None,
        creator_user_ids: list = None,
        states: list = None,
        tags: list = None,
        offset=0,
        limit=10,
        sort_by="Id",
        sort_order="Descend",
    ) -> dict:

        body = {
            "Offset": offset,
            "Limit": limit,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }
        CustomTaskClient.set_if_not_none(body, "Name", task_name)
        CustomTaskClient.set_if_not_none(body, "Filter", task_filter)
        CustomTaskClient.set_if_not_none(body, "Id", task_id)
        CustomTaskClient.set_if_not_none(body, "ResourceGroupId", resource_group_id)
        CustomTaskClient.set_if_not_none(body, "CreatorUserIds", creator_user_ids)
        CustomTaskClient.set_if_not_none(body, "States", states)
        CustomTaskClient.set_if_not_none(body, "Tags", tags)

        try:
            res_json = self.common_json_handler(api="ListCustomTasks", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to list custom tasks, error: %s", e)
            raise Exception("list custom task failed") from e

    def update_custom_task(
        self,
        task_id: str,
        task_name: str = None,
        description: str = None,
        tags: list = None,
    ) -> dict:
        body = {
            "Id": task_id,
        }
        CustomTaskClient.set_if_not_none(body, "Name", task_name)
        CustomTaskClient.set_if_not_none(body, "Description", description)
        CustomTaskClient.set_if_not_none(body, "Tags", tags)

        try:
            res_json = self.common_json_handler("UpdateCustomTask", body)
            return res_json
        except Exception as e:
            logging.error("Failed to update custom task, error: %s", e)
            raise Exception("update custom task failed") from e

    def stop_custom_task(self, task_id: str):
        body = {"Id": task_id}
        try:
            res_json = self.common_json_handler("StopCustomTask", body)
            return res_json
        except Exception as e:
            logging.error("Failed to stop custom task, error: %s", e)
            raise Exception("stop custom task failed") from e

    def get_custom_task(self, task_id: str) -> dict:
        try:
            body = {
                "Id": task_id,
            }
            res_json = self.common_json_handler(api="GetCustomTask", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to get custom task %s, error: %s", task_id, e)
            raise Exception("get custom task failed") from e

    def create_custom_task(
        self,
        # required
        name: str,
        image_id: str,
        entrypoint_path: str,
        framework: str,
        resource_group_id: str,
        task_role_specs: list,
        # optional
        active_deadline_seconds: int = 432000,
        tags: list = None,
        enable_tensorboard: bool = False,
        code_source: str = None,
        code_ori_path: str = None,
        tos_code_path: str = None,
        local_code_path: str = None,
        envs: list = None,
        args: str = None,
        storages: list = None,
        tensor_board_path: str = None,
        description: str = None,
        ak: str = None,
        sk: str = None,
        sidecar_memory_ratio: float = None,
        cache_type: str = None,
        sidecar_image: str = None,
        sidecar_resource_cpu: float = None,
        sidecar_resource_memory: float = None,
    ) -> dict:

        if active_deadline_seconds < 0:
            raise Exception("active_deadline_seconds should greater than 0")

        body = {
            # required
            "Name": name,
            "ImageSpec": {
                "Id": image_id,
            },
            "EntrypointPath": entrypoint_path,
            "Framework": framework,
            "ResourceGroupId": resource_group_id,
            "TaskRoleSpecs": task_role_specs,
            # optional
            "ActiveDeadlineSeconds": active_deadline_seconds,
            "EnableTensorBoard": enable_tensorboard,
        }

        CustomTaskClient.set_if_not_none(body, "Tags", tags)
        CustomTaskClient.set_if_not_none(body, "CodeSource", code_source)
        CustomTaskClient.set_if_not_none(body, "CodeOriPath", code_ori_path)
        CustomTaskClient.set_if_not_none(body, "TOSCodePath", tos_code_path)
        CustomTaskClient.set_if_not_none(body, "LocalCodePath", local_code_path)
        CustomTaskClient.set_if_not_none(body, "Args", args)
        CustomTaskClient.set_if_not_none(body, "Envs", envs)
        CustomTaskClient.set_if_not_none(body, "Storages", storages)
        CustomTaskClient.set_if_not_none(body, "TensorBoardPath", tensor_board_path)
        CustomTaskClient.set_if_not_none(body, "Description", description)
        CustomTaskClient.set_if_not_none(
            body, "SidecarMemoryRatio", sidecar_memory_ratio
        )
        CustomTaskClient.set_if_not_none(body, "CacheType", cache_type)
        CustomTaskClient.set_if_not_none(body, "SidecarImage", sidecar_image)
        CustomTaskClient.set_if_not_none(
            body, "SidecarResourceCPU", sidecar_resource_cpu
        )
        CustomTaskClient.set_if_not_none(
            body, "SidecarResourceMemory", sidecar_resource_memory
        )

        if ak is not None and sk is not None:
            body["Credential"] = {"AccessKeyId": ak, "SecretAccessKey": sk}

        try:
            res_json = self.common_json_handler(api="CreateCustomTask", body=body)
            return res_json
        except Exception as e:
            logging.error("Failed to create custom task, error: %s", e)
            raise Exception("create custom task failed") from e

    def delete_custom_task(self, task_id: str) -> dict:
        try:
            body = {
                "Id": task_id,
            }
            res_json = self.common_json_handler("DeleteCustomTask", body)
            return res_json
        except Exception as e:
            logging.error("Failed to delete custom task %s, error: %s", task_id, e)
            raise Exception("delete custom task failed") from e

    def get_custom_task_instances(
        self,
        custom_task_id: str,
        offset=0,
        limit=10,
        sort_by="Id",
        sort_order="Descend",
    ) -> dict:
        body = {
            "CustomTaskId": custom_task_id,
            "Offset": offset,
            "Limit": limit,
            "SortBy": sort_by,
            "SortOrder": sort_order,
        }

        try:
            res_json = self.common_json_handler("GetCustomTaskInstances", body)
            return res_json
        except Exception as e:
            logging.error("Failed to get custom task instances, error: %s", e)
            raise Exception("get custom task instances failed") from e

    @staticmethod
    def set_if_not_none(body, name, value):
        if value is not None:
            body[name] = value
