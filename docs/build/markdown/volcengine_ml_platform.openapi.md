# volcengine_ml_platform.openapi package

## Submodules

## volcengine_ml_platform.openapi.base_client module


### class volcengine_ml_platform.openapi.base_client.BaseClient(\*args, \*\*kwargs)
Bases: `volcengine.base.Service.Service`


#### common_json_handler(api, body)

#### get_sts_token(encrypt_code: str, duration: Optional[int] = None)

#### get_tos_upload_path(service_name: str, path=None)

* **Parameters**

    
    * **service_name** – 


    * **path** – 


Returns:


#### get_unique_flavor(list_flavor_result)

#### json2(api, params, body)

### volcengine_ml_platform.openapi.base_client.define_api(name, method='POST')
## volcengine_ml_platform.openapi.dataset_client module


### class volcengine_ml_platform.openapi.dataset_client.DataSetClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.openapi.base_client.BaseClient`


#### create_annotation_set(dataset_id: str, annotation_type: str, annotation_name: str, default_label: Optional[str] = None, labels: Optional[list] = None)
create annotation for dataset


* **Parameters**

    
    * **dataset_id** (*str*) – The unique ID of Dataset


    * **annotation_type** (*Model*) – annotation type


    * **annotation_name** (*str*) – annotation name


    * **default_label** (*str**, **optional*) – default label of annotataion. Defaults fo None


    * **labels** (*list*) – labels of annotataion. Defaults fo None



* **Raises**

    **Exception** – create_annotation_set failed



* **Returns**

    json response



#### create_dataset(body)

#### delete_annotation_set(dataset_id: str, annotation_id: str)
delete annotation set with given dataset_id and annotation_id


* **Parameters**

    
    * **dataset_id** (*str**, **required*) – The unique ID of the Dataset.


    * **annotation_id** (*str**, **required*) – The unique ID of the Annotation.



* **Raises**

    **Exception** – delete_annotation_set failed



* **Returns**

    json response



#### delete_dataset(dataset_id: str)
Delete a Dataset.


* **Parameters**

    **dataset_id** (*str**, **required*) – The unique ID of the Dataset



* **Raises**

    **Exception** – failed to delete dataset



* **Returns**

    json response



* **Return type**

    Dataset



#### get_annotation_set(dataset_id: str, annotation_id: str)
get annotation with given dataset_id and annotation_id


* **Parameters**

    
    * **dataset_id** (*str**, **required*) – The unique ID of the Dataset.


    * **annotation_id** (*str**, **required*) – The unique ID of the Annotation.



* **Raises**

    **Exception** – failed to get annotation



* **Returns**

    json response



#### get_dataset(dataset_id)
Get a Dataset.


* **Parameters**

    **dataset_id** (*str**, **required*) – The unique ID of the Dataset



* **Raises**

    **Exception** – failed to get dataset



* **Returns**

    json response



* **Return type**

    Dataset



#### list_annotation_datas(annotation_id: str, label_names: Optional[list] = None, status: Optional[int] = None, offset=0, page_size=10)
list annotation datas with given annotation_id


* **Parameters**

    
    * **annotation_id** (*str*) – The unique ID of annotation


    * **label_names** (*list**, **optional*) – filter option, label_names. Defaults to None.


    * **status** (*str**, **optional*) – filter option, status.Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.



* **Raises**

    **Exception** – list_annotation_datas failed



* **Returns**

    json response



#### list_annotation_label(dataset_id: str, annotation_id: str)
list annotation label set with given dataset_id and annotation_id


* **Parameters**

    
    * **dataset_id** (*str**, **required*) – The unique ID of the Dataset.


    * **annotation_id** (*str**, **required*) – The unique ID of the Annotation.



* **Raises**

    **Exception** – list_annotation_label failed



* **Returns**

    json response



#### list_annotation_sets(dataset_id: str)
list annotation set with given dataset_id


* **Parameters**

    **dataset_id** (*str*) – The unique ID of Dataset



* **Raises**

    **Exception** – list annotation sets exception



* **Returns**

    json response



#### list_datasets(name=None, name_contains=None, status=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list datasets


* **Parameters**

    
    * **name** (*str**, **optional*) – dataset name


    * **name_contains** (*str**, **optional*) – filter option, check if
    dataset name contains given string. Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘DatasetlName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list datasets exception



* **Returns**

    json response



#### try_delete_annotation_label(annotation_id: str, label: object)

#### update_annotation_data(annotation_id: str, datas: list)
update annotation_data with given annotation_id


* **Parameters**

    
    * **annotation_id** (*str**, **required*) – The unique ID of the Annotation


    * **datas** (*str**, **required*) – New datas of the Annotation.



* **Raises**

    **Exception** – failed to update annotataion_data



* **Returns**

    json response



* **Return type**

    Dataset



#### update_annotation_label(annotation_id: str, labels: list, default_label=None)

#### update_dataset(body)
## volcengine_ml_platform.openapi.inference_service_client module


### class volcengine_ml_platform.openapi.inference_service_client.InferenceServiceClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.openapi.base_client.BaseClient`


#### create_service(service_name: str, model_id: str, model_version_id: str, image_id: str, flavor_id: str, envs: list, replica: Optional[int] = 1, description: Optional[str] = None)
create inference service for models


* **Parameters**

    
    * **service_name** (*str*) – service name


    * **models** (*Model*) – Model object


    * **image_id** (*str*) – container image id


    * **flavor_id** (*str*) – hardward standard id


    * **envs** (*list*) – environment variables


    * **replica** (*int**, **optional*) – replica number. Defaults to 1.


    * **description** (*str**, **optional*) – description of service. Defaults to None.



* **Raises**

    **Exception** – create_service failed



* **Returns**

    json response



#### delete_service(service_id: str)
delete service with service id


* **Parameters**

    **service_id** (*str*) – service unique id



* **Raises**

    **Exception** – delete_service failed



* **Returns**

    json response



#### get_inference_service_instance_status(service_id: str, instance_id_list: list)
get the status of inference service instance


* **Parameters**

    
    * **service_id** (*str**, **required*) – The unique ID of Service


    * **offset** (*list**, **required*) – instance id list



* **Raises**

    **Exception** – get service instance status exception



* **Returns**

    json response



#### get_service(service_id: str)
get service with given service_id


* **Parameters**

    **service_id** (*str*) – The unique ID of the Service



* **Raises**

    **Exception** – raise on get_service failed



* **Returns**

    json response



#### list_inference_service_instances(service_id: str, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list service instances


* **Parameters**

    
    * **service_id** (*str**, **optional*) – The unique ID of Service


    * **offset** (*int**, **optional*) – offset of service. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘InstanceName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list datasets exception



* **Returns**

    json response



#### list_service_versions(service_id: str, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list service versions with given service_id


* **Parameters**

    
    * **service_id** (*str*) – The unique ID of the Service


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ServiceVersion’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list_service_versions failed



* **Returns**

    json response



#### list_services(service_name: Optional[str] = None, service_name_contains: Optional[str] = None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list services


* **Parameters**

    
    * **service_name** (*str**, **optional*) – service name


    * **service_name_contains** (*str**, **optional*) – filter option, check if
    service name contains given string. Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ServiceName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list datasets exception



* **Returns**

    json response



#### modify_service(service_name: str, service_id: str, cluster_id: str)
Modify ServiceName with given ServiceID and ClusterID


* **Parameters**

    
    * **service_name** (*str**, **required*) – New Name of the Service


    * **service_id** (*str**, **required*) – The unique ID of the Service


    * **cluster_id** (*str**, **required*) – The unique ID of the Cluster



* **Raises**

    **Exception** – list datasets exception



* **Returns**

    json response



#### rollback_service_version(service_id: str, service_version_id: str)
Rollback a ServiceVersion with ServiceID and ServiceVersionID


* **Parameters**

    
    * **service_id** (*str**, **required*) – The unique ID of the Service


    * **service_version_id** (*str**, **required*) – The unique ID of the ServiceVersion



* **Raises**

    **Exception** – failed to rollback service version



* **Returns**

    json response



* **Return type**

    Dataset



#### scale_service(service_id: str, replicas: int)
scale service by changing the number of replicas


* **Parameters**

    
    * **service_id** (*str*) – service id


    * **replicas** (*int*) – number of replicas



* **Raises**

    **Exception** – scale_service failed



* **Returns**

    json response



#### start_service(service_id: str)
start service with service id


* **Parameters**

    **service_id** (*str*) – service unique id



* **Raises**

    **Exception** – start_service failed



* **Returns**

    json response



#### stop_service(service_id: str)
stop service with service id


* **Parameters**

    **service_id** (*str*) – service unique id



* **Raises**

    **Exception** – stop_service failed



* **Returns**

    json response



#### update_service(service_id: str, replicas: int, flavor_id: str, model_id: str, model_version_id: str, image_id: str, envs: list, change_type: str, service_description: Optional[str] = None)
## volcengine_ml_platform.openapi.model_client module


### class volcengine_ml_platform.openapi.model_client.ModelClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.openapi.base_client.BaseClient`


#### cancel_perf_job(job_id: str)
cancel a perf job, including all of its tasks


* **Parameters**

    **job_id** (*str**, **required*) – The unique ID of the perf job.



* **Raises**

    **Exception** – raise on cancel perf job failed



* **Returns**

    json response



#### cancel_perf_task(task_id: str)
cancel a perf task
:param task_id: The unique ID of the perf job.
:type task_id: str, required


* **Raises**

    **Exception** – raise on cancel perf task failed



* **Returns**

    json response



#### create_model(model_name: str, model_format: str, model_type: str, path: str, model_id=None, description=None, tensor_config=None, model_metrics=None, source_type='TOS')
create models


* **Parameters**

    
    * **model_name** (*str*) – models’s name


    * **model_format** (*str*) – models’s format, can be ‘SavedModel’, ‘GraphDef’,’TorchScript’,’PTX’,
    ‘CaffeModel’,’NetDef’,’MXNetParams’,’Scikit_Learn’,’XGBoost’,’TensorRT’,’ONNX’,or ‘Custom’


    * **model_type** (*str*) – The type of the ModelVersion, examples: ‘TensorFlow:2.0’


    * **path** (*str*) – source storage path


    * **model_id** (*str**, **optional*) – model_id, a new models will be created if not given. Defaults to None.


    * **description** (*str**, **optional*) – description to the models. Defaults to None.


    * **tensor_config** (*dict**, **optional*) – tensor config of the models.


    * **model_metrics** (*list**, **optional*) – list of models metrics.


    * **source_type** (*str**, **optional*) – storage type. Defaults to ‘TOS’.



* **Raises**

    **Exception** – failed to create models



* **Returns**

    json response



#### create_perf_job(model_version_id: str, tensor_config: dict, job_type: str, job_params: list)
create perf job


* **Parameters**

    
    * **model_version_id** (*str**, **required*) – The unique ID of the model version


    * **tensor_config** (*dict**, **required*) – tensor config of the perf job


    * **job_type** (*str**, **required*) – type of the job, e.g., PERF_ONLY, CONVERT_PERF


    * **job_params** (*list**, **required*) – parameters to run the job



* **Raises**

    **Exception** – raise on create perf job failed



* **Returns**

    json response



#### delete_model(model_id: str)
delete models with given models id


* **Parameters**

    **model_id** (*str*) – The unique ID of the Model



* **Raises**

    **Exception** – raise on delete_model failed



* **Returns**

    json response



#### delete_model_version(model_version_id: str)
delete certain version of a models


* **Parameters**

    **model_version_id** (*str*) – The unique ID of the ModelVersion



* **Raises**

    **Exception** – raise on delete model version failed



* **Returns**

    json response



#### get_model(model_id: str)
get models with given models id


* **Parameters**

    **model_id** (*str*) – The unique ID of the Model



* **Raises**

    **Exception** – raise on get model failed



* **Returns**

    json response



#### get_model_next_version(model_id=None)
get next models version with given model_id


* **Parameters**

    **model_id** (*str**, **required*) – The unique ID of the Model. 1 will return if not given



* **Returns**

    The next version of the Model



* **Return type**

    next_version(int)



#### get_model_version(model_version_id: str)
get certain version of a models


* **Parameters**

    **model_version_id** (*str*) – The unique ID of the ModelVersion



* **Raises**

    **Exception** – raise on get model version failed



* **Returns**

    json response



#### list_model_versions(model_id: str, model_version: Optional[int] = None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list models versions with given model_id


* **Parameters**

    
    * **model_id** (*str*) – The unique ID of the Model


    * **model_version** – filter option, the certain ModelVersion of Model. Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ModelVersion’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – raise on list model versions failed



* **Returns**

    json response



#### list_models(model_name=None, model_name_contains=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list models


* **Parameters**

    
    * **model_name** (*str**, **optional*) – certern models with return if given models name. Defaults to None.


    * **model_name_contains** (*str**, **optional*) – filter option, check if
    models name contains given string. Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to None.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ModelName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list models exception



* **Returns**

    json response



#### list_perf_jobs(model_version_id=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list perf jobs


* **Parameters**

    
    * **model_version_id** (*str**, **optional*) – The unique ID of the model version.


    * **job_id** (*str**, **optional*) – The unique ID of the perf job.


    * **offset** (*int**, **optional*) – offset of database. Defaults to None.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ModelName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – raise on list perf jobs failed



* **Returns**

    json response



#### list_perf_tasks(task_id=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list perf tasks


* **Parameters**

    
    * **task_id** (*str**, **optional*) – The unique ID of the perf task.


    * **job_id** (*str**, **optional*) – The unique ID of the perf job.


    * **offset** (*int**, **optional*) – offset of database. Defaults to None.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ModelName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – raise on list perf tasks failed



* **Returns**

    json response



#### update_model(model_id: str, model_name=None)
update model_name with given model_id


* **Parameters**

    
    * **model_id** (*str**, **required*) – The unique ID of the Model


    * **model_name** (*str**, **optional*) – New ModelName of the Model. Defaults to None.



* **Raises**

    **Exception** – raise on update model failed



* **Returns**

    json response



#### update_model_version(model_version_id: str, description=None, tensor_config=None, model_metrics=None)
update models version


* **Parameters**

    
    * **model_version_id** (*str*) – The unique ID of the ModelVersion


    * **description** (*str**, **optional*) – New Description of the ModelVersion. Defaults to None.


    * **tensor_config** (*dict**, **optional*) – tensor config of the model.


    * **model_metrics** (*list**, **optional*) – list of models metrics.



* **Raises**

    **Exception** – raise on update model version failed



* **Returns**

    json response



#### update_perf_task(task_id: str, task_status=None)
update perf task


* **Parameters**

    
    * **task_id** (*str**, **required*) – The unique ID of the task


    * **task_status** (*str**, **optional*) – Status to update. Defaults to None.



* **Raises**

    **Exception** – raise on update perf task failed



* **Returns**

    json response


## volcengine_ml_platform.openapi.resource_client module


### class volcengine_ml_platform.openapi.resource_client.ResourceClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.openapi.base_client.BaseClient`


#### create_resource(name: str, resource_type: str, v_cpu: float, memory: str, gpu_type: str, gpu_num: float, price: float, region: str)
create resource


* **Parameters**

    
    * **name** (*str*) – resource name


    * **resource_type** – The type of resource


    * **v_cpu** (*str*) – The cpu num of resource


    * **memory** (*str*) – resource memory


    * **gpu_type** (*str*) – The gpu type of resource


    * **gpu_num** (*float*) – The gpu num of resource


    * **price** (*float*) – resource price


    * **region** (*str*) – The region of resource



* **Raises**

    **Exception** – create_resource failed



* **Returns**

    json response



#### delete_resource(flavor_id: str)
delete resource with given flavor id


* **Parameters**

    **flavor_id** (*str*) – The unique ID of the Resource



* **Raises**

    **Exception** – raise on delete_resource failed



* **Returns**

    json response



#### get_resource(flavor_id: str)
get resource with given flavor_id


* **Parameters**

    **flavor_id** (*str*) – The unique ID of the Resource



* **Raises**

    **Exception** – raise on get_resource failed



* **Returns**

    json response



#### list_resource(name=None, name_contains=None, resource_type=None, tag: Optional[list] = None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')
list resource with given service_id


* **Parameters**

    
    * **name** (*str**, **optional*) – resource name


    * **name_contains** (*str**, **optional*) – filter option, check if
    resource name contains given string. Defaults to None.


    * **resource_type** (*str**, **optional*) – filter option, check if
    resource type equals to given string. Defaults to None.


    * **tag** (*list**, **optional*) – filter option, check if
    resource tag in given list. Defaults to None.


    * **offset** (*int**, **optional*) – offset of database. Defaults to 0.


    * **page_size** (*int**, **optional*) – number of results to fetch. Defaults to 10.


    * **sort_by** (*str**, **optional*) – sort by ‘ResourceName’ or ‘CreateTime’. Defaults to ‘CreateTime’.


    * **sort_order** (*str**, **optional*) – ‘Ascend’ or ‘Descend’. Defaults to ‘Descend’.



* **Raises**

    **Exception** – list_resource failed



* **Returns**

    json response


## volcengine_ml_platform.openapi.secure_token_client module


### class volcengine_ml_platform.openapi.secure_token_client.SecureTokenClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.openapi.base_client.BaseClient`


#### get_secure_token(module_name, time_to_live=30, account_id=None, user_id=None)
get secure token to perform some operation


* **Parameters**

    
    * **module_name** (*str*) – module name, eg: inference, customtask


    * **time_to_live** (*int*) – ttl of token, equals to 30 by default


    * **account_id** (*int*) – user’s account id


    * **user_id** (*int*) – user’s user id



* **Raises**

    **Exception** – get_secure_token failed



* **Returns**

    json response


## Module contents
