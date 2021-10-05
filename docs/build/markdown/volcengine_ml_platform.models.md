# volcengine_ml_platform.models package

## Submodules

## volcengine_ml_platform.models.model module


### class volcengine_ml_platform.models.model.Model(local_path='.')
Bases: `object`


#### calcel_perf_task(task_id: str)

#### cancel_perf_job(job_id: str)

#### create_perf_job(model_id: str, model_version: int, tensor_config: dict, job_type: str, job_params: list)

#### deploy(model_id: str, model_version: int, service_name: str, flavor: str = 'ml.highcpu.large', image_id: str = 'machinelearning/tfserving:tf-cuda10.1', envs=None, replica: Optional[int] = 1, description: Optional[str] = None)

#### download(model_id: str, model_version: int, local_path: Optional[str] = None)

#### get_model_versions(model_id: str, model_version: Optional[int] = None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')

#### list_models(model_name_contains=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')

#### list_perf_jobs(model_id=None, model_version=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')

#### list_perf_tasks(task_id=None, job_id=None, offset=0, page_size=10, sort_by='CreateTime', sort_order='Descend')

#### register(local_path: str, model_id: Optional[str] = None, model_name: Optional[str] = None, model_format: Optional[str] = None, model_type: Optional[str] = None, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None)

#### unregister(model_id: str, model_version: int)

#### unregister_all_versions(model_id: str)

#### update_model(model_id: str, model_name: Optional[str] = None)

#### update_model_version(model_id: str, model_version: int, description: Optional[str] = None, tensor_config: Optional[dict] = None, model_metrics: Optional[list] = None)

#### update_perf_task(task_id: str, task_status=None)
## volcengine_ml_platform.models.validation module


### volcengine_ml_platform.models.validation.valid_json(serialized_data)

### volcengine_ml_platform.models.validation.validate_metrics(model_metrics)

### volcengine_ml_platform.models.validation.validate_tensor_config(tensor_config)
## Module contents
