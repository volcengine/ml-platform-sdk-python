#!/bin/bash
FILE_PATH=$(cd "$(dirname "$0")";pwd)
cd $FILE_PATH
export PYTHONPATH="../../"
horovodrun -np 2 -H "${ML_PLATFORM_MPI_HOSTS}" python swin_transformer_horovod.py
