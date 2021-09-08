#!/bin/bash

FILE_PATH=$(cd "$(dirname "$0")";pwd)
cd $FILE_PATH
export PYTHONPATH="../../"

python xgboost_house_price.py
