import os

import setuptools

NAME = "volcengine_ml_platform"
VERSION = "1.0.3"
description = "Volcengine ML Platform API client library"

setup_requires = ["setuptools>=41.0.0"]

install_requires = [
    "volcengine>=1.0.19",
    "boto3>=1.18.29",
    "requests>=2.18.0",
    "six>=1.11.0",
    "Pillow>=4.0.0",
    "numpy>=1.14.0",
    "jsonschema>=3.0.0",
    "tqdm>=4.19.2",
    "prettytable>=2.0.0",
]

# test
pytorch_requires = ["torch==1.8.0"]
full_requires = list(set(pytorch_requires))

package_root = os.path.abspath(os.path.dirname(__file__))
readme_filename = os.path.join(package_root, "README.md")
with open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=[
        package
        for package in setuptools.PEP420PackageFinder.find()
        if package.startswith(NAME)
    ],
    entry_points={},
    namespace_packages=(),
    author="Volcengine LLC",
    author_email="developer@volce.com",
    license="MIT Licence",
    url="https://github.com/volcengine/ml-platfrom-sdk-python",
    platforms="Posix; MacOS X; Windows",
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require={
        "full": full_requires,
        "pytorch": pytorch_requires,
    },
    python_requires=">=3.6",
    scripts=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False,
)
