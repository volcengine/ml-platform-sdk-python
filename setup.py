import sys
from setuptools import setup, find_packages

require_list = [
    'boto3~=1.17.111',
    'requests~=2.26.0',
    'six',
    'volcengine~=1.0.17',
    'numpy==1.20.0',
    'tqdm~=4.61.2',
    'pillow==8.2.0',
    'six',
    'setuptools~=57.1.0',
    'botocore~=1.20.111',
    'prettytable~=2.1.0',
    'torch'
]

test_require_list = []


def is_build_action():
    if len(sys.argv) <= 1:
        return False

    if sys.argv[1].startswith('build'):
        return True

    if sys.argv[1].startswith('bdist'):
        return True

    if sys.argv[1].startswith('install'):
        return True

    return False


setup(name='operator_sdk',
      packages=find_packages(exclude=[".test"]),
      setup_requires=require_list if is_build_action() else [],
      install_requires=require_list,
      tests_require=test_require_list,
      python_requires='>=3.6',
      zip_safe=False)

setup(name='ml_platform_sdk',
      version="1.0",
      packages=find_packages(exclude=[".test"]),
      setup_requires=require_list if is_build_action() else [],
      install_requires=require_list,
      tests_require=test_require_list,
      python_requires='>=3.6',
      zip_safe=False
)