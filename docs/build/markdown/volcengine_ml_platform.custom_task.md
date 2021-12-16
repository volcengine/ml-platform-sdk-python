# volcengine_ml_platform.custom_task package

## Submodules

## volcengine_ml_platform.custom_task.custom_task module


### class volcengine_ml_platform.custom_task.custom_task.CustomTask(custom_task_id: Optional[str] = None, name: Optional[str] = None, image_id: Optional[str] = None, entrypoint_path: Optional[str] = None, framework: Optional[str] = None, resource_group_id: Optional[str] = None, task_role_specs: Optional[list] = None, active_deadline_seconds: int = 432000, tags: Optional[list] = None, enable_tensorboard: bool = False, code_source: Optional[str] = None, code_ori_path: Optional[str] = None, tos_code_path: Optional[str] = None, local_code_path: Optional[str] = None, envs: Optional[list] = None, args: Optional[str] = None, storages: Optional[list] = None, tensor_board_path: Optional[str] = None, description: Optional[str] = None, ak: Optional[str] = None, sk: Optional[str] = None, sidecar_memory_ratio: Optional[float] = None, cache_type: str = 'Cloudfs', sidecar_image: Optional[str] = None, sidecar_resource_cpu: Optional[float] = None, sidecar_resource_memory: Optional[float] = None)
Bases: `object`


#### cancel()
取消自定义任务


* **Raises**

    **Exception** – 取消自定义任务异常



#### client( = <volcengine_ml_platform.openapi.custom_task_client.CustomTaskClient object>)

#### delete()
删除自定义任务


* **Raises**

    **Exception** – 删除自定义任务异常



#### get()
获取自定义任务


* **Returns**

    返回 json 格式的 response。
    示例:

    ```
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
    ```




* **Raises**

    **Exception** – 获取自定义任务异常



#### classmethod list(task_name: Optional[str] = None, task_filter: Optional[str] = None, task_id: Optional[str] = None, resource_group_id: Optional[str] = None, creator_user_ids: Optional[list] = None, states: Optional[list] = None, tags: Optional[list] = None, offset=0, limit=10, sort_by='Id', sort_order='Descend')
列出自定义任务


* **Parameters**

    
    * **task_name** – 任务名称（精确筛选）。


    * **task_filter** – 模糊搜索，允许的值：’Name’（模糊搜索任务名称）, ‘Id’（模糊搜索自定义任务 Id）。


    * **task_id** – 自定义任务 Id（精确筛选）。


    * **resource_group_id** – 资源组 Id（精确筛选）。


    * **creator_user_ids** – 用户 Ids（精确筛选，允许一次筛选多个用户 Id），示例：[0, 1, 2]。


    * **states** – 自定义任务状态（精确筛选，允许一次筛选多个自定义任务状态），示例：[“Running”, “Stopping”]，
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


    * **tags** – 标签（精确筛选，允许一次筛选多个标签），示例：[“tag1”, “tag2”]。


    * **offset** – 偏移，默认值 0。


    * **limit** – 限制长度，默认值 10，-1 表示无限制。


    * **sort_by** – 排序，默认值 ‘Id’，可选值：’Name’,’Id’,’CreateTime’,’UpdateTime’。


    * **sort_order** – 排序方式，可选值：’Ascend’,’Descend’



* **Returns**

    返回 json 格式的 response。
    实例:

    ```
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
    ```




#### list_instances(offset=0, limit=10, sort_by='Id', sort_order='Descend')
列出自定义任务实例


* **Parameters**

    
    * **offset** – 偏移，默认值 0。


    * **limit** – 限制长度，默认值 10，-1 表示无限制。


    * **sort_by** – 排序，默认值 ‘Id’，可选值：’Id’, ‘LaunchTime’,’FinishTime’。


    * **sort_order** – 排序方式，可选值：’Ascend’,’Descend’



* **Returns**

    返回 json 格式的 response。
    实例:

    ```
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
    ```




* **Raises**

    **Exception** – 列出自定义任务实例异常



#### submit()
提交自定义任务


* **Returns**

    返回 json 格式的 response，包含任务 ID 和订单号。
    示例:

    ```
    {
        "Id": "t-xxx-xxx",
        // 使用专有资源组时订单号为空
        "OrderNumber": "yyyy"
    }
    ```




* **Raises**

    **Exception** – 提交自定义任务异常


## Module contents
