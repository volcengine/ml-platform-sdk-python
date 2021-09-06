#!/bin/bash
FILE_PATH=$(cd "$(dirname "$0")";pwd)
cd $FILE_PATH
export PYTHONPATH="../../"
horovodrun -np 1  python swin_transformer_horovod.py
