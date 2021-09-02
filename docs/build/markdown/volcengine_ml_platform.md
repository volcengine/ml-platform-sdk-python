# volcengine_ml_platform package

## Subpackages


* volcengine_ml_platform.annotation package


    * Submodules


    * volcengine_ml_platform.annotation.annotation module


    * volcengine_ml_platform.annotation.image_classification_annotation module


    * volcengine_ml_platform.annotation.image_detection_annotation module


    * volcengine_ml_platform.annotation.image_segmentation_annotation module


    * volcengine_ml_platform.annotation.text_classification_annotation module


    * volcengine_ml_platform.annotation.text_entity_annotation module


    * volcengine_ml_platform.annotation.ttypes module


    * Module contents


* volcengine_ml_platform.datasets package


    * Submodules


    * volcengine_ml_platform.datasets.dataset module


    * volcengine_ml_platform.datasets.image_dataset module


    * volcengine_ml_platform.datasets.tabular_dataset module


    * volcengine_ml_platform.datasets.text_dataset module


    * volcengine_ml_platform.datasets.video_dataset module


    * Module contents


* volcengine_ml_platform.inferences package


    * Submodules


    * volcengine_ml_platform.inferences.inference module


    * Module contents


* volcengine_ml_platform.infrastructure package


    * Submodules


    * volcengine_ml_platform.infrastructure.ml_sts_token_service module


    * Module contents


* volcengine_ml_platform.io package


    * Submodules


    * volcengine_ml_platform.io.tos module


    * volcengine_ml_platform.io.tos_dataset module


    * Module contents


* volcengine_ml_platform.models package


    * Submodules


    * volcengine_ml_platform.models.model module


    * volcengine_ml_platform.models.validation module


    * Module contents


* volcengine_ml_platform.openapi package


    * Submodules


    * volcengine_ml_platform.openapi.base_client module


    * volcengine_ml_platform.openapi.dataset_client module


    * volcengine_ml_platform.openapi.inference_service_client module


    * volcengine_ml_platform.openapi.model_client module


    * volcengine_ml_platform.openapi.resource_client module


    * Module contents


## Module contents


### class volcengine_ml_platform.EnvHolder()
Bases: `object`


#### ENV_NAME( = 'PROD')

#### GLOBAL_CREDENTIALS( = None)

#### STRESS_FLAG( = '')

#### classmethod get_credentials()

#### classmethod init(ak, sk, region, env_name, init_aws_env)

#### classmethod pickup_non_blank_value(\*args)

### volcengine_ml_platform.get_credentials()

### volcengine_ml_platform.get_encrypted_key()

### volcengine_ml_platform.get_env_name()

### volcengine_ml_platform.get_service_direct_host()

### volcengine_ml_platform.get_service_host()

### volcengine_ml_platform.get_service_name()

### volcengine_ml_platform.get_stress_flag()

### volcengine_ml_platform.get_tos_endpoint_url()

### volcengine_ml_platform.init(ak=None, sk=None, region='cn-beijing', env_name=None, init_aws_env=True)

### volcengine_ml_platform.mark_stress(flag=None)
