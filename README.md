# Volcano Engine ML Platform Python SDK


## To start using SDK
https://bytedance.feishu.cn/docs/doccnxximX3BaSrGhB81SCav60f

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
pip install --user git+https://code.byted.org/machinelearning/mlplatform-sdk-python.git
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
Format code
```
yapf -ipr .
```
Python linter (Google style)
```
pylint volcengine_ml_platform
```

### Unit And End2End Test
```
pytest
```

## Git hooks
Pre-commit hook to check format and style for changed files
```
ln -s -f presubmit/pre_commit.sh .git/hooks/pre-commit
```

