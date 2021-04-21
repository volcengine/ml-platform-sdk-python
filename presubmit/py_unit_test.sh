#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY"
python3 -m unittest discover "operator_sdk" "*_test.py"
popd
