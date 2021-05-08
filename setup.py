import sys
from setuptools import setup, find_packages

require_list = []
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
