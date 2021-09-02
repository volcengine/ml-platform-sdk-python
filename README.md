# Volcano Engine ML Platform Python SDK


## To start using SDK

### 1. Install package
* From pypi
```
pip install --user volcengine_ml_platform
```
* Upgrade from pypi
```
pip install --user --upgrade volcengine_ml_platform
```
* To install the development version
```
pip install --user git+https://github.com/volcengine/mlplatform-sdk-python.git
```

### 2. Run Samples
2.1 Setting up the environment(just choose one of following)

* set environment variable
```
export VOLC_ACCESSKEY="replace_with_your_ak"
export VOLC_SECRETKEY="replace_with_your_sk"
export VOLC_REGION="replace_with_region_the_region_you_use_the_most"
export VOLC_ML_PLATFORM_ENV="PROD/BOE"            # optional
```


* edit ~/.volc/config

```json
{
    "ak": "replace_with_your_ak",
    "sk": "replace_with_your_sk",
    "region": "replace_with_region_the_region_you_use_the_most",
    "ml_platform" : {
      "env": "PROD/BOE"
   }
}
```
> the key of ml_platform is optional

* edit samples/env.py
```
cp samples/env.py.template samples/env.py
# edit the content of samples/env.py
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
