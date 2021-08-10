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

### 2. Usage



### 3. Document




## To start developing SDK
### Installation dependencies
```
python setup.py install
```
### Code style
Format code
```
yapf -ipr .
```
Python linter (Google style)
```
pylint operator_sdk
```

## Git hooks
Pre-commit hook to check format and style for changed files
```
ln -s -f presubmit/pre_commit.sh .git/hooks/pre-commit
```