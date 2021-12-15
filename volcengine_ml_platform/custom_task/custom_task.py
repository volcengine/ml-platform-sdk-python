import logging

from volcengine_ml_platform.openapi import custom_task_client


class CustomTask:

    client = custom_task_client.CustomTaskClient()

    def __init__(
        self,
        custom_task_id: str = None,
        name: str = None,
        image_id: str = None,
        entrypoint_path: str = None,
        framework: str = None,
        resource_group_id: str = None,
        task_role_specs: list = None,
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
        cache_type: str = "Cloudfs",
        sidecar_image: str = None,
        sidecar_resource_cpu: float = None,
        sidecar_resource_memory: float = None,
    ):
        """自定义任务客户端

        Args:
            custom_task_id: 任务 ID，get、stop 和 delete 方法必填。
            name: 任务名称，create 方法必填。
            image_id: 镜像 ID，比如 "ml_platform/pytorch:1.7"，create 方法必填。
            entrypoint_path: 入口命令，create 方法必填。
            framework: 框架，可选值：'TensorFlowPS','PyTorchDDP','BytePS','Horovod','MPI','Custom'，create 方法必填。
            resource_group_id: 资源组 ID，create 方法必填。
            task_role_specs: 实例配置，示例：[{"RoleName": "worker", "RoleReplicas": 1, "ResourceSpecId": ml.g1e.large}]，
                create 方法必填。
            active_deadline_seconds: 最长运行时间（可选），默认值 432000s（120h）。
            tags: 标签（可选），示例：["tag1", "tag2"]。
            enable_tensorboard: 是否启用 tensorboard（可选），默认值 False。
            code_source: 代码来源（可选），可选值：'', 'WebIDE', 'Local'。
            code_ori_path: 代码路径（可选），如果 code_source 非空，code_ori_path 也必须非空。
            tos_code_path: TOS 代码路径（可选）。
            local_code_path: 本地代码路径（可选）。
            envs: 环境变量（可选），示例：[{"Name": "ENV_DEMO_NAME", "Value": "ENV_DEMO_VALUE"}]。
            args: 参数（可选），示例："--verbose -c conf.ini"。
            storages: 待挂载的数据盘列表（可选），当挂载数据盘时为必填，示例：
                [{"Type": "Tos", "MountPath": "/root/code/mount", "Bucket": "mybucket", "Prefix": "myprefix"}]
                - Type 表示存储类型，可填值：Tos / Nas；
                - MountPath 表示挂载点；
                - Bucket 表示 TOS 存储桶名称，仅当 Type == Tos 时必填；
                - Prefix 表示 TOS 挂载 Prefix，仅当 Type == Tos 时有效。
            tensor_board_path: tensorboard 路径（可选）。
            description: 任务描述（可选）。
            ak: 用户的 AccessKey ID（可选），可在用户的密钥管理页面下查看。
            sk: 用户的 AccessKey Secret（可选），可在用户的密钥管理页面下查看。
            sidecar_memory_ratio: 分配给 sidecar container memory 的比例（可选），允许的值(0,1), 例如 0.5 代表 50%分配给 sidecar 容器。
            cache_type: 数据缓存类型（可选），默认值 'Cloudfs'，可选值：'Cloudfs', 'Gpfs'。
            sidecar_image: sidecar 容器镜像（可选）。
            sidecar_resource_cpu: sidercar CPU 资源（可选）。
            sidecar_resource_memory: sidercar Memory 资源，仅支持 "Gi" 单位（可选）。
        """
        self.custom_task_id = custom_task_id
        self.order_number = None

        self.order_id = None
        self.name = name
        self.image_id = image_id
        self.entrypoint_path = entrypoint_path
        self.framework = framework
        self.resource_group_id = resource_group_id
        self.task_role_specs = task_role_specs

        self.active_deadline_seconds = active_deadline_seconds
        self.tags = tags
        self.enable_tensorboard = enable_tensorboard
        self.code_source = code_source
        self.code_ori_path = code_ori_path
        self.tos_code_path = tos_code_path
        self.local_code_path = local_code_path
        self.envs = envs
        self.args = args
        self.storages = storages
        self.tensor_board_path = tensor_board_path
        self.description = description
        self.ak = ak
        self.sk = sk
        self.sidecar_memory_ratio = sidecar_memory_ratio
        self.cache_type = cache_type
        self.sidecar_image = sidecar_image
        self.sidecar_resource_cpu = sidecar_resource_cpu
        self.sidecar_resource_memory = sidecar_resource_memory

    def submit(self):
        """提交自定义任务

        Returns:
            返回 json 格式的 response，包含任务 ID 和订单号。
            示例: ::
                {
                    "Id": "t-xxx-xxx",
                    // 使用专有资源组时订单号为空
                    "OrderNumber": "yyyy"
                }

        Raises:
            Exception: 提交自定义任务异常
        """

        try:
            res_json = self.client.create_custom_task(
                self.name,
                self.image_id,
                self.entrypoint_path,
                self.framework,
                self.resource_group_id,
                self.task_role_specs,
                self.active_deadline_seconds,
                self.tags,
                self.enable_tensorboard,
                self.code_source,
                self.code_ori_path,
                self.tos_code_path,
                self.local_code_path,
                self.envs,
                self.args,
                self.storages,
                self.tensor_board_path,
                self.description,
                self.ak,
                self.sk,
                self.sidecar_memory_ratio,
                self.cache_type,
                self.sidecar_image,
                self.sidecar_resource_cpu,
                self.sidecar_resource_memory,
            )
            self.custom_task_id = res_json["Result"]["Id"]
            if self.resource_group_id == "default":
                self.order_number = res_json["Result"]["OrderNumber"]
            return res_json["Result"]
        except Exception as e:
            logging.error("Failed to submit custom task, error: %s", e)
            raise Exception("submit custom task failed") from e

    def cancel(self):
        """取消自定义任务

        Raises:
            Exception: 取消自定义任务异常
        """
        if self.custom_task_id is None or self.custom_task_id == "":
            logging.error("Failed to cancel custom task due to an empty custom task id")
            raise Exception("cancel custom task failed")

        try:
            self.client.stop_custom_task(self.custom_task_id)
            return
        except Exception as e:
            logging.error(
                "Failed to cancel custom task, task_id: %s, error: %s",
                self.custom_task_id,
                e,
            )
            raise Exception("cancel custom task failed") from e

    def get(self):
        """获取自定义任务

        Returns:
            返回 json 格式的 response。
            示例: ::
                {
                    "Id": "t-xx-xxx",
                    "Name": "task_demo",
                    "CreateTime": "2021-11-18T12:33:21+08:00",
                    "LaunchTime": "2021-11-18T12:33:31+08:00",
                    "FinishTime": "2021-11-18T12:35:35+08:00",
                    "CreatorUserId": 0,
                    "EnableTensorBoard": false,
                    "State": "Cancelled",
                    "CodeSource": "",
                    "CodeOriPath": "",
                    "ImageSpec": {
                      "Id": "machinelearning/python:2.7_3.7"
                    },
                    "TOSCodePath": "",
                    "LocalCodePath": "",
                    "EntrypointPath": "sleep 3600",
                    "Args": "",
                    "Framework": "Horovod",
                    "ActiveDeadlineSeconds": 432000,
                    "ResourceGroupId": "default",
                    "TaskRoleSpecs": [
                      {
                        "RoleName": "worker",
                        "RoleReplicas": 1,
                        "ResourceSpecId": "ml.g1e.large"
                      }
                    ],
                    "TensorBoardPath": "mlplatform/tensorboard/20000/t-20211118123318-76qwq",
                    "ExitCode": 0,
                    "DiagInfo": "DeletionTimeSet: all pods are terminated",
                    "Description": "This is a demo.",
                    "ServerTime": "2021-11-18T12:41:11.377828+08:00",
                    "UpdateTime": "2021-11-18T12:35:31+08:00",
                    "IsTrial": true
                }

        Raises:
            Exception: 获取自定义任务异常
        """
        if self.custom_task_id is None or self.custom_task_id == "":
            logging.error("Failed to get custom task due to an empty custom task id")
            raise Exception("get custom task failed")

        try:
            res_json = self.client.get_custom_task(self.custom_task_id)
            return res_json["Result"]
        except Exception as e:
            logging.error(
                "Failed to get custom task, task_id: %s, error: %s",
                self.custom_task_id,
                e,
            )
            raise Exception("get custom task failed") from e

    def delete(self):
        """删除自定义任务

        Raises:
            Exception: 删除自定义任务异常
        """
        if self.custom_task_id is None or self.custom_task_id == "":
            logging.error("Failed to delete custom task due to an empty custom task id")
            raise Exception("delete custom task failed")

        try:
            self.client.delete_custom_task(self.custom_task_id)
        except Exception as e:
            logging.error(
                "Failed to delete custom task, task_id: %s, error: %s",
                self.custom_task_id,
                e,
            )
            raise Exception("delete custom task failed") from e

    def list_instances(self, offset=0, limit=10, sort_by="Id", sort_order="Descend"):
        """列出自定义任务实例

        Args:
            offset: 偏移，默认值 0。
            limit: 限制长度，默认值 10，-1 表示无限制。
            sort_by: 排序，默认值 'Id'，可选值：'Id', 'LaunchTime','FinishTime'。
            sort_order: 排序方式，可选值：'Ascend','Descend'

        Returns:
            返回 json 格式的 response。
            实例: ::
                {
                    // 一共有多少个实例
                    "Total": 1,
                    // 实例列表
                    "List": [
                        {
                            "RoleName": "worker",
                            "RoleIndex": "0",
                            "ResourceSpecId": "ml.g1e.large",
                            "LaunchTime": "2021-10-27T15:33:54+08:00",
                            "FinishTime": "2021-10-27T15:34:34+08:00",
                            "State": "Success",
                            "LogURL": "",
                            "WebShellURL": "",
                            "MonitorURL": "",
                            "ExitCode": 0,
                            "DiagInfo": "Completed",
                            "PodName": "t-xx-xxx-worker-0",
                            "ContainerName": "mljob"
                        }
                    ]
                }

        Raises:
            Exception: 列出自定义任务实例异常
        """
        if self.custom_task_id is None or self.custom_task_id == "":
            logging.error(
                "Failed to list custom task instances due to an empty custom task id"
            )
            raise Exception("list custom task instances failed")

        try:
            res_json = self.client.get_custom_task_instances(
                self.custom_task_id, offset, limit, sort_by, sort_order
            )
            return res_json["Result"]
        except Exception as e:
            logging.error(
                "Failed to list custom task instances, task_id: %s, error: %s",
                self.custom_task_id,
                e,
            )
            raise Exception("list custom task instances failed") from e

    @classmethod
    def list(
        cls,
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
    ):
        """列出自定义任务

        Args:
            task_name: 任务名称（精确筛选）。
            task_filter: 模糊搜索，允许的值：'Name'（模糊搜索任务名称）, 'Id'（模糊搜索自定义任务 Id）。
            task_id: 自定义任务 Id（精确筛选）。
            resource_group_id: 资源组 Id（精确筛选）。
            creator_user_ids: 用户 Ids（精确筛选，允许一次筛选多个用户 Id），示例：[0, 1, 2]。
            states: 自定义任务状态（精确筛选，允许一次筛选多个自定义任务状态），示例：["Running", "Stopping"]，
                可用的状态包括：
                - Queue: 排队中
                - Staging: 部署中
                - Running: 运行中
                - Killing: 停止中
                - Success: 成功
                - Failed: 失败
                - Cancelled: 取消
                - Exception: 异常
                - Initialized: 创建中
            tags: 标签（精确筛选，允许一次筛选多个标签），示例：["tag1", "tag2"]。
            offset: 偏移，默认值 0。
            limit: 限制长度，默认值 10，-1 表示无限制。
            sort_by: 排序，默认值 'Id'，可选值：'Name','Id','CreateTime','UpdateTime'。
            sort_order: 排序方式，可选值：'Ascend','Descend'

        Returns:
            返回 json 格式的 response。
            实例: ::
                {
                    "Total": 5084,
                    "List": [
                        {
                            "Id": "t-xx-xxx",
                            "Name": "task_demo",
                            "CreateTime": "2021-11-24T20:11:45+08:00",
                            "LaunchTime": "2021-11-24T20:11:54+08:00",
                            "FinishTime": "",
                            "CreatorUserId": 0,
                            "Tags": ["jhy"],
                            "EnableTensorBoard": false,
                            "State": "Running",
                            "CodeSource": "",
                            "CodeOriPath": "",
                            "ImageSpec": {
                                "Id": "machinelearning/python:2.7_3.7",
                                "Version": "2021-10-01"
                            },
                            "TOSCodePath": "",
                            "LocalCodePath": "",
                            "EntrypointPath": "sleep 1h",
                            "Args": "",
                            "Framework": "Horovod",
                            "ActiveDeadlineSeconds": 432000,
                            "ResourceGroupId": "r-zz-zzz",
                            "TaskRoleSpecs": [
                                {
                                    "RoleName": "worker",
                                    "RoleReplicas": 1,
                                    "ResourceSpecId": "ml.g1e.large"
                                }
                            ],
                            "TensorBoardPath": "mlplatform/tensorboard/20000/t-xx-xxx",
                            "ExitCode": 0,
                            "DiagInfo": "all pods are running",
                            "Description": "",
                            "ServerTime": "2021-11-24T20:36:19.192439602+08:00",
                            "UpdateTime": "2021-11-24T20:34:13+08:00",
                            "IsTrial": false
                        },
                    ]
                }
        """
        try:
            res_json = cls.client.list_custom_tasks(
                task_name,
                task_filter,
                task_id,
                resource_group_id,
                creator_user_ids,
                states,
                tags,
                offset,
                limit,
                sort_by,
                sort_order,
            )
            return res_json["Result"]
        except Exception as e:
            logging.error("Failed to list custom tasks　, error: %s", e)
            raise Exception("list custom tasks failed") from e
