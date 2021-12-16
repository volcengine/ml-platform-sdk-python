# volcengine_ml_platform.models package

## Submodules

## volcengine_ml_platform.models.inner_model module


### class volcengine_ml_platform.models.inner_model.Model(target_account_id=None, target_user_id=None)
Bases: `object`

Model类封装了模型仓库相关的一些操作,包括：模型上传、下载、更新、删除，评测任务提交、更新等


#### download(model_id: str, model_version: str, local_path: str)
下载模型到本地


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **local_path** (*str*) – 标示模型下载到本地时的存储路径



* **Raises**

    **Exception** – 模型下载异常



#### get_model_version(model_id: str, model_version: str)
获取模型版本


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号



* **Returns**

    返回json格式的response，包含模型版本信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "2021091410551801022514606301199F07",
            "Action": "ListModelVersions",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelVersionID": "m-20210812150750-w54j6-14",
            "ModelVersion": 14,
            "ModelFormat": "SavedModel",
            "ModelType": "TensorFlow:2.4",
            "Path": "tos://ml-platform-auto-created-required-2100000050-cn-north-4/modelrepo/from-sdk-repo/1631236594036/1/",
            "Description": "test remark 2",
            "SourceType": "TOS",
            "CreateTime": "2021-09-10T09:37:14+08:00",
            "TensorConfig": {
                "Inputs": []
            }
        }
    }
    ```




* **Raises**

    **Exception** – 获取模型版本异常



#### get_target_account_id()

#### get_target_user_id()

#### register(local_path: str, model_id: Optional[str] = None, model_name: Optional[str] = None, model_format: Optional[str] = None, model_type: Optional[str] = None, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None, model_category: Optional[str] = None, dataset_id: Optional[str] = None, source_type: Optional[str] = 'TOS', base_model_version_id: Optional[str] = None, source_id: Optional[str] = None, model_tags: Optional[list] = None)
注册模型到模型仓库

将存储在本地的模型包，上传到模型仓库


* **Parameters**

    
    * **local_path** (*str*) – 模型在本地的存放路径


    * **model_id** (*str**, **optional*) – 模型在仓库中的唯一标识。默认为None
    指定该参数时，会在\`model_id\`对应的模型下，注册一个新的模型版本
    不指定该参数时，会在模型仓库中创建一个新的模型


    * **model_name** (*str**, **optional*) – 模型名字。默认为None
    如果指定了\`model_id\`，则该参数可忽略，否则需要填写该参数


    * **model_format** (*str*) – 模型格式
    可选值: ‘SavedModel’, ‘GraphDef’,’TorchScript’,’PTX’, ‘CaffeModel’,
    ‘NetDef’,’MXNetParams’,’Scikit_Learn’,’XGBoost’,’TensorRT’,’ONNX’, ‘Custom’


    * **model_type** (*str*) – 模型框架
    格式：<framework_name:framework_version>，比如：’TensorFlow:2.0’
    框架可选值：’TensorFlow’, ‘PyTorch’, ‘ONNX’, ‘Caffe’, ‘Caffe2’, ‘MXNet’, ‘TensorRT’,
    ‘Scikit_Learn’, ‘XGBoost’, ‘LightGBM’,


    * **description** (*str**, **optional*) – 模型描述信息。 默认为None


    * **tensor_config** (*dict**, **optional*) – 模型的Tensor配置。 默认为None


    * **model_metrics** (*list**, **optional*) – 模型的指标数据。默认为None


    * **model_category** (*str**, **optional*) – 模型类别
    可选值: ‘TextClassification’, ‘TabularClassification’, ‘TabularRegression’, ‘ImageClassification’


    * **dataset_id** (*str**, **optional*) – 训练模型所使用的数据集唯一标示


    * **source_type** (*str**, **optional*) – 模型来源, 默认为TOS
    可选值: ‘TOS’, ‘Local’, ‘AutoML’, ‘Perf’


    * **base_model_version_id** (*str**, **optional*) – perf转换任务生成的模型，所基于的模型版本ID


    * **source_id** (*str**, **optional*) – 对于perf转换任务生成的模型，产生这个模型的perf task id


    * **model_tags** – (list, optional): 模型标签。默认为None。 e.g. [{“Key”: “tag_key”, “Value”: “tag_key_value”}]



* **Returns**

    返回json格式的response，包含模型相关信息。
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210910093712010225084217038CE268",
            "Action": "CreateModel",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelID": "m-20210812150750-w54j6",
            "VersionInfo": {
                "ModelVersionID": "m-20210812150750-w54j6-14",
                "ModelVersion": 14
            }
        }
    }
    ```




* **Raises**

    **Exception** – 模型创建异常



#### set_target_account_id(target_account_id)

#### set_target_user_id(target_user_id)

#### update_model_version(model_id: str, model_version: str, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None)
更新模型版本


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **description** (*str**, **optional*) – 模型描述信息。 默认为None


    * **tensor_config** (*dict**, **optional*) – 模型的Tensor配置。 默认为None


    * **model_metrics** (*list**, **optional*) – 模型的指标数据。默认为None



* **Returns**

    返回json格式的response，包含模型版本ID
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "202109141641180102250842170249FC70",
            "Action": "UpdateModelVersion",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelVersionID": "m-20210805193007-tt2ww-1"
        }
    }
    ```




* **Raises**

    **Exception** – 更新模型版本异常



#### upload_tos(local_path: str)
上传数据到TOS


* **Parameters**

    **local_path** (*str*) – 数据在本地的存放路径



* **Returns**

    返回tos路径。
    比如: “tos://ml-platform-auto-created-required-2100000050-cn-north-4/modelrepo/from-sdk-repo/1631236594036/1/”



* **Raises**

    **Exception** – 数据上传异常


## volcengine_ml_platform.models.model module


### class volcengine_ml_platform.models.model.Model()
Bases: `object`

Model类封装了模型仓库相关的一些操作,包括：模型上传、下载、更新、删除，评测任务提交、更新等


#### calcel_perf_task(task_id: str)
取消评测/转换Task


* **Parameters**

    **task_id** (*str*) – 评测/转换Task唯一标识



* **Returns**

    返回json格式的response，包含评测/转换Job的信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914181913010225146063005A6098",
            "Action": "CancelPerfTask",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "TaskID": "pf-20210908105428-qz4t7"
        }
    }
    ```




* **Raises**

    **Exception** – 取消评测/转换Task异常



#### cancel_perf_job(job_id: str)
取消评测/转换Job，同时会取消Job包含的所有Task


* **Parameters**

    **job_id** (*str*) – 评测/转换Job唯一标识



* **Returns**

    返回json格式的response，包含评测/转换Job的信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914165956010225243081056D3BD9",
            "Action": "CancelPerfJob",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "JobID": "pj-20210914105554-nvh45"
        }
    }
    ```




* **Raises**

    **Exception** – 取消评测/转换Job异常



#### create_perf_job(model_id: str, model_version: str, tensor_config: dict, job_type: str, job_params: list)
创建模型评测/转换Job


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **tensor_config** (*dict*) – 评测/转换任务所使用的模型Tensor配置


    * **job_type** (*str*) – Job类型。可选值：’PERF_ONLY’, ‘CONVERT_PERF’


    * **job_params** (*list*) – Job参数。
    FlavorIDList: 指定Job使用的计算规格列表
    ConvertType: 模型转换的类型
    ConvertPrecisionList: 模型转换的精度列表



* **Returns**

    返回json格式的response，包含评测/转换Job相关信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914105554010225243081032071F7",
            "Action": "CreatePerfJob",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "JobID": "pj-20210914105554-nvh45",
            "ModelVersionID": "m-20210812150750-w54j6-1",
            "TensorConfig": {
                "Inputs": [
                    {
                        "TensorName": "serving_default_Conv1_input:0",
                        "DType": "FP32",
                        "Shape": {
                            "MaxShape": [
                                8,
                                28,
                                28,
                                1
                            ],
                            "MinShape": [
                                1,
                                28,
                                28,
                                1
                            ]
                        }
                    }
                ]
            },
            "TensorConfigID": "t-20210815151138-7fmmp",
            "JobParamsList": [
                {
                    "FlavorIDList": [
                        "ml.g1e.large"
                    ]
                }
            ],
            "JobType": "PERF_ONLY",
            "JobStatus": "Submitted",
            "CreateTime": "2021-09-14T10:55:54.495+08:00"
        }
    }
    ```




* **Raises**

    **Exception** – 创建评测/转换Job异常



#### deploy(model_id: str, model_version: str, service_name: str, flavor: str = 'ml.g1e.large', image_id: str = 'machinelearning/tfserving:tf-cuda10.1', envs=None, replica: Optional[int] = 1, description: Optional[str] = None)
将模型部署为在线推理服务


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **service_name** (*str*) – 推理服务名称


    * **flavor** (*str**, **optional*) – 推理服务使用的套餐。默认为\`ml.g1e.large\`


    * **image_id** (*str**, **optional*) – 推理服务使用的镜像。默认为\`machinelearning/tfserving:tf-cuda10.1\`


    * **envs** (*dict**, **optional*) – 推理服务需要注入的环境变量。默认为None


    * **replica** (*int**, **optional*) – 推理服务实例数量。默认为1


    * **description** (*str**, **optional*) – 推理服务描述信息。默认为None



* **Returns**

    返回InferenceService对象，包含推理服务相关信息



* **Raises**

    **Exception** – 模型部署异常



#### download(model_id: str, model_version: str, local_path: str)
下载模型到本地


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **local_path** (*str*) – 标示模型下载到本地时的存储路径



* **Raises**

    **Exception** – 模型下载异常



#### get_model_versions(model_id: str, model_version: Optional[str] = None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
获取模型版本


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str**, **optional*) – 模型版本号。默认为None


    * **offset** (*int**, **optional*) – 标识检索模型版本时，起始偏移量位置。默认为0


    * **page_size** (*int**, **optional*) – 标识每个分页的大小。默认为10


    * **sort_by** (*str**, **optional*) – 标识按照哪个字段进行排序。默认为”CreateTime”


    * **sort_order** (*str**, **optional*) – 标识按照升序或降序进行排序。默认为”Descend”



* **Returns**

    返回json格式的response，包含模型版本信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "2021091410551801022514606301199F07",
            "Action": "ListModelVersions",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "Total": 14,
            "List": [
                {
                    "ModelVersionID": "m-20210812150750-w54j6-14",
                    "ModelVersion": 14,
                    "ModelFormat": "SavedModel",
                    "ModelType": "TensorFlow:2.4",
                    "Path": "tos://ml-platform-auto-created-required-2100000050-cn-north-4/modelrepo/from-sdk-repo/1631236594036/1/",
                    "Description": "test remark 2",
                    "SourceType": "TOS",
                    "CreateTime": "2021-09-10T09:37:14+08:00",
                    "TensorConfig": {
                        "Inputs": []
                    }
                }
            ]
        }
    }
    ```




* **Raises**

    **Exception** – 获取模型版本异常



#### list_models(model_name_contains=None, id_contains=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
获取模型列表


* **Parameters**

    
    * **model_name_contains** (*str**, **optional*) – 模型名字包含的字符串。默认为None
    获取模型列表时，可以按照模型名是否包含该字段指定的字符串，对模型进行检索查询


    * **id_contains** (*str**, **optional*) – 模型ID包含的字符串。默认为None
    获取模型列表时，可以按照模型ID是否包含该字段指定的字符串，对模型进行检索查询


    * **offset** (*int**, **optional*) – 标识检索模型时，起始偏移量位置。默认为0


    * **page_size** (*int**, **optional*) – 标识每个分页的大小。默认为10


    * **sort_by** (*str**, **optional*) – 标识按照哪个字段进行排序。默认为”CreateTime”


    * **sort_order** (*str**, **optional*) – 标识按照升序或降序进行排序。默认为”Descend”



* **Returns**

    返回json格式的response，包含模型列表数据
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914105459010225084217071AB67E",
            "Action": "ListModels",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "Total": 78,
            "List": [
                {
                    "ModelID": "m-20210812150750-w54j6",
                    "ModelName": "test_perf",
                    "CreateTime": "2021-08-12T15:07:50+08:00",
                    "ModelVersionsCount": 14,
                    "LatestVersion": "14"
                },
                {
                    "ModelID": "m-20210805193007-tt2ww",
                    "ModelName": "swinTransformerTestModel",
                    "CreateTime": "2021-08-05T19:30:07+08:00",
                    "ModelVersionsCount": 1,
                    "LatestVersion": "1"
                }
            ]
        }
    }
    ```




* **Raises**

    **Exception** – 获取模型列表异常



#### list_perf_jobs(model_id=None, model_version=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
获取评测/转换任务Job列表


* **Parameters**

    
    * **model_id** (*str**, **optional*) – 模型在仓库中的唯一标识。默认为None


    * **model_version** (*str**, **optional*) – 模型版本号。默认为None


    * **job_id** (*str**, **optional*) – 评测/转换Job唯一标识。默认为None


    * **offset** (*int**, **optional*) – 标识检索时，起始偏移量位置。默认为0


    * **page_size** (*int**, **optional*) – 标识每个分页的大小。默认为10


    * **sort_by** (*str**, **optional*) – 标识按照哪个字段进行排序。默认为”CreateTime”


    * **sort_order** (*str**, **optional*) – 标识按照升序或降序进行排序。默认为”Descend”



* **Returns**

    返回json格式的response，包含评测/转换Job的信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "202109141657200102250842170054BAB5",
            "Action": "ListPerfJobs",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "Total": 11,
            "List": [
                {
                    "JobID": "pj-20210914105554-nvh45",
                    "ModelVersionID": "m-20210812150750-w54j6-1",
                    "TensorConfigID": "t-20210815151138-7fmmp",
                    "JobParamsList": [
                        {
                            "FlavorIDList": [
                                "ml.g1e.large"
                            ]
                        }
                    ],
                    "JobType": "PERF_ONLY",
                    "JobStatus": "Submitted",
                    "CreateTime": "2021-09-14T10:55:54+08:00",
                    "TaskCount": 1,
                    "EndedTaskCount": 0
                }
            ]
        }
    }
    ```




* **Raises**

    **Exception** – 获取评测/转换Job异常



#### list_perf_tasks(task_id=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
获取评测/转换任务Task列表


* **Parameters**

    
    * **task_id** (*str**, **optional*) – 评测/转换Task唯一标识。默认为None


    * **job_id** (*str**, **optional*) – 评测/转换Job唯一标识。默认为None


    * **offset** (*int**, **optional*) – 标识检索时，起始偏移量位置。默认为0


    * **page_size** (*int**, **optional*) – 标识每个分页的大小。默认为10


    * **sort_by** (*str**, **optional*) – 标识按照哪个字段进行排序。默认为”CreateTime”


    * **sort_order** (*str**, **optional*) – 标识按照升序或降序进行排序。默认为”Descend”



* **Returns**

    返回json格式的response，包含评测/转换Task的信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914170325010225243147054486D2",
            "Action": "ListPerfTasks",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "Total": 1,
            "List": [
                {
                    "TaskID": "pf-20210914105554-fb564",
                    "JobID": "pj-20210914105554-nvh45",
                    "ModelVersionID": "m-20210812150750-w54j6-1",
                    "TaskArgs": {
                        "TaskType": "PERF_ONLY",
                        "FlavorID": "ml.g1e.large",
                        "ConvertType": "base",
                        "ConvertPrecision": "base"
                    },
                    "TaskStatus": "Stopping",
                    "CreateTime": "2021-09-14T10:55:55+08:00"
                }
            ]
        }
    }
    ```




* **Raises**

    **Exception** – 获取评测/转换Task异常



#### register(local_path: str, model_id: Optional[str] = None, model_name: Optional[str] = None, model_format: Optional[str] = None, model_type: Optional[str] = None, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None, model_category: Optional[str] = None, dataset_id: Optional[str] = None, source_type: Optional[str] = 'TOS', model_tags: Optional[list] = None)
注册模型到模型仓库

将存储在本地的模型包，上传到模型仓库


* **Parameters**

    
    * **local_path** (*str*) – 模型在本地的存放路径


    * **model_id** (*str**, **optional*) – 模型在仓库中的唯一标识。默认为None
    指定该参数时，会在\`model_id\`对应的模型下，注册一个新的模型版本
    不指定该参数时，会在模型仓库中创建一个新的模型


    * **model_name** (*str**, **optional*) – 模型名字。默认为None
    如果指定了\`model_id\`，则该参数可忽略，否则需要填写该参数


    * **model_format** (*str*) – 模型格式
    可选值: ‘SavedModel’, ‘GraphDef’,’TorchScript’,’PTX’, ‘CaffeModel’,
    ‘NetDef’,’MXNetParams’,’Scikit_Learn’,’XGBoost’,’TensorRT’,’ONNX’, ‘Custom’


    * **model_type** (*str*) – 模型框架
    格式：<framework_name:framework_version>，比如：’TensorFlow:2.0’
    框架可选值：’TensorFlow’, ‘PyTorch’, ‘ONNX’, ‘Caffe’, ‘Caffe2’, ‘MXNet’, ‘TensorRT’,
    ‘Scikit_Learn’, ‘XGBoost’, ‘LightGBM’,


    * **description** (*str**, **optional*) – 模型描述信息。 默认为None


    * **tensor_config** (*dict**, **optional*) – 模型的Tensor配置。 默认为None


    * **model_metrics** (*list**, **optional*) – 模型的指标数据。默认为None


    * **model_category** (*str**, **optional*) – 模型类别
    可选值: ‘TextClassification’, ‘TabularClassification’, ‘TabularRegression’, ‘ImageClassification’


    * **dataset_id** (*str**, **optional*) – 训练模型所使用的数据集唯一标示


    * **source_type** (*str**, **optional*) – 模型来源, 默认为TOS
    可选值: ‘TOS’, ‘Local’, ‘AutoML’, ‘Perf’


    * **model_tags** – (list, optional): 模型标签。默认为None。 e.g. [{“Key”: “tag_key”, “Value”: “tag_key_value”}]



* **Returns**

    返回json格式的response，包含模型相关信息。
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210910093712010225084217038CE268",
            "Action": "CreateModel",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelID": "m-20210812150750-w54j6",
            "VersionInfo": {
                "ModelVersionID": "m-20210812150750-w54j6-14",
                "ModelVersion": 14
            }
        }
    }
    ```




* **Raises**

    **Exception** – 模型创建异常



#### unregister(model_id: str, model_version: str)
删除模型版本


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号



* **Returns**

    返回json格式的response，包含模型版本信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "2021090515061201022514606305039116",
            "Action": "DeleteModelVersion",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-1"
        },
        "Result": {
            "ModelVersionID": "m-20210805193930-lb8xf-1"
        }
    }
    ```




* **Raises**

    **Exception** – 删除模型版本异常



#### unregister_all_versions(model_id: str)
删除模型及其所有模型版本


* **Parameters**

    **model_id** (*str*) – 模型在仓库中的唯一标识



* **Returns**

    返回json格式的response，包含模型信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "202109141615290102252430810758D951",
            "Action": "DeleteModel",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelID": "m-20210914161504-pbhh7"
        }
    }
    ```




* **Raises**

    **Exception** – 删除模型异常



#### update_model(model_id: str, model_name: Optional[str] = None)
更新模型


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_name** (*str**, **optional*) – 修改之后的模型名字。默认为None



* **Returns**

    返回json格式的response，包含模型ID
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914163725010225243081025917BF",
            "Action": "UpdateModel",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelID": "m-20210805193007-tt2ww"
        }
    }
    ```




* **Raises**

    **Exception** – 更新模型异常



#### update_model_version(model_id: str, model_version: str, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None)
更新模型版本


* **Parameters**

    
    * **model_id** (*str*) – 模型在仓库中的唯一标识


    * **model_version** (*str*) – 模型版本号


    * **description** (*str**, **optional*) – 模型描述信息。 默认为None


    * **tensor_config** (*dict**, **optional*) – 模型的Tensor配置。 默认为None


    * **model_metrics** (*list**, **optional*) – 模型的指标数据。默认为None



* **Returns**

    返回json格式的response，包含模型版本ID
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "202109141641180102250842170249FC70",
            "Action": "UpdateModelVersion",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "ModelVersionID": "m-20210805193007-tt2ww-1"
        }
    }
    ```




* **Raises**

    **Exception** – 更新模型版本异常



#### update_perf_task(task_id: str, task_status=None)
更新评测/转换Task


* **Parameters**

    
    * **task_id** (*str*) – 评测/转换Task唯一标识


    * **task_status** (*str*) – 更新后的Task状态



* **Returns**

    返回json格式的response，包含评测/转换Task的信息
    比如:

    ```
    {
        "ResponseMetadata": {
            "RequestId": "20210914170527010225146063074AD2C8",
            "Action": "UpdatePerfTask",
            "Version": "2021-07-01",
            "Service": "ml_platform",
            "Region": "cn-north-4"
        },
        "Result": {
            "TaskID": "t-20210817143422-xr4dh"
        }
    }
    ```




* **Raises**

    **Exception** – 更新评测/转换Task异常


## volcengine_ml_platform.models.validation module


### volcengine_ml_platform.models.validation.valid_json(serialized_data)

### volcengine_ml_platform.models.validation.validate_local_path(local_path)

### volcengine_ml_platform.models.validation.validate_metrics(model_metrics)

### volcengine_ml_platform.models.validation.validate_model_category(model_category)

### volcengine_ml_platform.models.validation.validate_model_tensor_config(tensor_config)

### volcengine_ml_platform.models.validation.validate_perf_job_tensor_config(tensor_config)

### volcengine_ml_platform.models.validation.validate_source_type(source_type)
## Module contents
