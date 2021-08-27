#!/bin/bash

set -e

ROOT_DIRECTORY=$(dirname "$(dirname "$0")")

pushd "$ROOT_DIRECTORY"
export VOLC_ACCESSKEY="AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE"
export VOLC_SECRETKEY="WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=="
export VOLC_ML_PLATFORM_ENV="BOE"

python3 -m py.test tests/unit
popd
