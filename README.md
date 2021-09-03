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

2.1 Setting up the environment(just choose one of following)


* set environment variable
```
export VOLC_ACCESSKEY="replace_with_your_ak"
export VOLC_SECRETKEY="replace_with_your_sk"
export VOLC_REGION="replace_with_region_the_region_you_use_the_most"
```

* edit ~/.volc/config

```json
{
    "ak": "replace_with_your_ak",
    "sk": "replace_with_your_sk",
    "region": "replace_with_region_the_region_you_use_the_most"
}
```

* call method: volcengine_ml_platform.init()
```
import volcengine_ml_platform

AK = "replace_with_your_ak"
SK = "replace_with_your_sk=="
REGION_NAME = "replace_with_region_the_region_you_use_the_most"

volcengine_ml_platform.init(ak=AK, sk=SK, region=REGION_NAME)
```
```
cp samples/env.py.template samples/env.py
```

> Please set the content of the env.py file correctly, and pay attention to the following 2 points:
>   - samples/env.py has been added to .gitignore
>   - don't modify env.py.template


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
