#!/bin/bash

WORKPATH=$(pwd)
python3.7 $WORKPATH/multiproc.py --nproc_per_node 8 $WORKPATH/launch.py --model resnet50 --precision AMP --mode benchmark_training --platform DGX2V ./ --raport-file benchmark.json --epochs 1 --prof 100
