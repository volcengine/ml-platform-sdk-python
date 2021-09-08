# Volcano Engine ML Platform Python SDK


## To start using SDK

### 1. Install package
* From TOS
```
pip install --user https://ml-platform-public-examples-cn-beijing.tos-cn-beijing.volces.com/python_sdk_installer/volcengine_ml_platform-1.0.0-py3-none-any.whl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

* From Pypi
```
敬请期待
```

### 2. Run Samples

Volcengine Region List

|  name   | endpoint  |
|  ----    | ----  |
| cn-beijing  | xxxx |
| cn-qingdao  | xxxx |

2.1 Setting up the environment

There are two ways to set up. In WebIDE, you can use both, but in Customtask, you are required to do this by setting environment variable.


* set environment variable
```
export VOLC_ACCESSKEY="replace_with_your_ak"
export VOLC_SECRETKEY="replace_with_your_sk"
export VOLC_REGION="replace_with_region_the_region_you_use_the_most"
```

​	ps: for more details about this in Customtask, invite [Customtask](https://www.volcengine.com/docs/6459/72350).

* edit ~/.volc/config

```json
{
    "ak": "replace_with_your_ak",
    "sk": "replace_with_your_sk",
    "region": "replace_with_region_the_region_you_use_the_most"
}
```

* call method: volcengine_ml_platform.init()

> You can refer to samples/env.py.template

```
import volcengine_ml_platform

AK = "replace_with_your_ak"
SK = "replace_with_your_sk=="
REGION_NAME = "replace_with_region_the_region_you_use_the_most"

volcengine_ml_platform.init(ak=AK, sk=SK, region=REGION_NAME)
```

- here are some samples in *mlplatform-sdk-python/samples* , to run these samples, using the follow commands:

| sample                                   | run in WebIDE                                                | run in Customtask                                            |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| flower_classification_tensorflow         | cd mlplatform-sdk-python/samples/flower_classification_tensorflow && bash run.sh | cd mlplatform-sdk-python/samples/flower_classification_tensorflow && bash run.sh |
| flower_classification_tensorflow_horovod | cd mlplatform-sdk-python/samples/flower_classification_tensorflow && bash run_horovod_webide.sh | cd mlplatform-sdk-python/samples/flower_classification_tensorflow && bash run_horovod_customtask.sh |
| flower_classification_pytorch            | cd mlplatform-sdk-python/samples/flower_classification_pytorch&& bash run_webide.sh | cd mlplatform-sdk-python/samples/flower_classification_pytorch && bash run_customtask.sh |
| house_price_prediction_xgboost           | cd mlplatform-sdk-python/samples/house_price_prediction_xgboost&& bash run_webide.sh | cd mlplatform-sdk-python/samples/house_price_prediction_xgboost&& bash run_customtask.sh |

- What can you learn by this samples?

| sample                                   | what can you learn                                           |
| ---------------------------------------- | ------------------------------------------------------------ |
| flower_classification_tensorflow         | How to load datasets from TOS and build dataset by tf.io.gfile.glob() and load_dataset()<br />How to load pretrained model from TOS<br />How to save checkpoints and upload to TOS by callbacks<br />How to load checkpoints from TOS |
| flower_classification_tensorflow_horovod | How to use horovod in Webide and Customtask                  |
| flower_classification_pytorch            | How to load datasets from TOS and build dataset by our SDK<br />How to load checkpoint from TOS and upload checkpoint to TOS<br />How to use pytorch DDP in WebIDE and Customtask |

### 3. Usage



### 4. Document



## To start developing SDK
### Installation dependencies
```
python setup.py install
pip install -r requirements.txt
```
### Code style
```
pip install pre-commit
pre-commit install           # install pre-commit hook to git
```
You can also manually check all files with the following command
```
pre-commit run --all-files
```

### Unittest
```
make unit_test
```

### end2end test
```
make end2end_test
```
### Write Comment

[look it](./docs/README.md)
