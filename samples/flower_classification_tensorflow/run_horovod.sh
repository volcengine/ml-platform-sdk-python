#!/bin/bash

FILE_PATH=$(cd "$(dirname "$0")";pwd)
cd $FILE_PATH

export PYTHONPATH="../../"

horovodrun -np ML_PLATFORM_MPI_NP -H "${MLP_MPI_HOSTS}" python swin_transformer_horovod.py || true

sleep 1d
