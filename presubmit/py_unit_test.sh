#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY"
python3 -m unittest discover "volcengine_ml_platform" "*_test.py"
popd
