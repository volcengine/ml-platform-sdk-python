#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY/operator_sdk"
python3 -m unittest discover "*_test.py"
popd
