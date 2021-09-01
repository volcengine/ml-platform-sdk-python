#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY"
export VOLC_ML_PLATFORM_ENV="BOE"

python3 -m py.test tests/unit
popd
