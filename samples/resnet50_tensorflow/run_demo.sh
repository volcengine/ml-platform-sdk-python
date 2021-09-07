#!/bin/bash


pathvar="$( cd "$( dirname $0 )" && pwd )"
cd $pathvar
python3 -m pip install -r ./requirements.txt --user

python3 ./resnet50_multi_gpu.py --enable_mixed_precision --enable_xla
