# volcengine_ml_platform.innerapi package

## Submodules

## volcengine_ml_platform.innerapi.base_client module


### class volcengine_ml_platform.innerapi.base_client.InnerApiBaseClient(\*args, \*\*kwargs)
Bases: `object`


#### common_json_handler(api, body, token)

#### get_tos_upload_path(service_name: str, token: str, path=None)

* **Parameters**

    
    * **service_name** (*str*) – server name


    * **token** (*str*) – The secure token


    * **path** – 


Returns:


### volcengine_ml_platform.innerapi.base_client.define_inner_api(name, method='POST')
## volcengine_ml_platform.innerapi.dataset_client module


### class volcengine_ml_platform.innerapi.dataset_client.InnerDatasetClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.innerapi.base_client.InnerApiBaseClient`


#### get_annotation_set(dataset_id: str, annotation_id: str, token: str)

#### get_dataset(dataset_id: str, token: str)
## volcengine_ml_platform.innerapi.model_client module


### class volcengine_ml_platform.innerapi.model_client.ModelInnerApiClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.innerapi.base_client.InnerApiBaseClient`


#### create_model(model_name: str, model_format: str, model_type: str, path: str, token: str, model_id=None, description=None, tensor_config=None, model_metrics=None, model_category=None, dataset_id=None, source_type='TOS', base_model_version_id=None, source_id=None, model_tags=None)
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


    * **model_category** (*str**, **optional*) – category of the model.
    values can be ‘TextClassification’, ‘TabularClassification’, ‘TabularRegression’, ‘ImageClassification’


    * **dataset_id** (*str**, **optional*) – id of the dataset based on which the model is trained


    * **source_type** (*str**, **optional*) – storage type. Defaults to ‘TOS’.


    * **token** (*str*) – The secure token


    * **base_model_version_id** (*str**, **optional*) – perf转换任务生成的模型，所基于的模型版本ID


    * **source_id** (*str**, **optional*) – 对于perf转换任务生成的模型，产生这个模型的perf task id


    * **model_tags** (*list**, **optional*) – model tags. e.g. [{“Key”: “tag_key”, “Value”: “tag_key_value”}]



* **Raises**

    **Exception** – failed to create models



* **Returns**

    json response



#### get_model_version(model_version_id: str, token: str)
get certain version of a models


* **Parameters**

    
    * **model_version_id** (*str*) – The unique ID of the ModelVersion


    * **token** (*str*) – The secure token



* **Raises**

    **Exception** – raise on get model version failed



* **Returns**

    json response



#### update_model_version(model_version_id: str, token: str, description=None, tensor_config=None, model_metrics=None)
update models version


* **Parameters**

    
    * **model_version_id** (*str*) – The unique ID of the ModelVersion


    * **token** (*str*) – The secure token


    * **description** (*str**, **optional*) – New Description of the ModelVersion. Defaults to None.


    * **tensor_config** (*dict**, **optional*) – tensor config of the model.


    * **model_metrics** (*list**, **optional*) – list of models metrics.



* **Raises**

    **Exception** – raise on update model version failed



* **Returns**

    json response


## volcengine_ml_platform.innerapi.sts_token module


### class volcengine_ml_platform.innerapi.sts_token.STSApiClient(\*args, \*\*kwargs)
Bases: `volcengine_ml_platform.innerapi.base_client.InnerApiBaseClient`


#### get_sts_token(token, duration=3600)
## Module contents
