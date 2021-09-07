#!/bin/bash

pathvar="$( cd "$( dirname $0 )" && pwd )"
cd $pathvar
python3 -m pip install -r ./requirements.txt --user

python3 ./multiproc.py --nproc_per_node 8 ./launch.py --model resnet50 --precision AMP --mode benchmark_training --platform DGX2V ./ --raport-file benchmark.json --epochs 1 --prof 100
