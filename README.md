# Python Operator SDK

## Document
https://bytedance.feishu.cn/docs/doccnxximX3BaSrGhB81SCav60f

## Usage
Install package
```
python3 setup.py install
```

## Code style
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