#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

python3 -m py.test tests/end2end
popd
