#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY"
python3 -m unittest discover "*_test.py"
popd
