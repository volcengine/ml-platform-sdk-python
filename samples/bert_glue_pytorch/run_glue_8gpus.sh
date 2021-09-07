#!/bin/bash

pathvar="$( cd "$( dirname $0 )" && pwd )"
cd $pathvar

pip install -r ./requirements.txt --user -i https://pypi.tuna.tsinghua.edu.cn/simple

TASK="MRPC"
GLUE_DIR="$HOME/.volcengine_ml_platform/samples/bert_glue/glue_data"
BERT_BASE_DIR="$HOME/.volcengine_ml_platform/samples/bert_glue/bert-base-uncased-model"

python prepare_data.py

python -m torch.distributed.launch --nproc_per_node 8 ./main.py \
    --model_type bert \
    --model_name_or_path $BERT_BASE_DIR \
    --task_name $TASK \
    --do_train \
    --do_lower_case \
    --data_dir $GLUE_DIR/$TASK \
    --max_seq_length 128 \
    --per_gpu_train_batch_size=32 \
    --learning_rate 2e-5 \
    --num_train_epochs 3.0 \
    --output_dir "/tmp/${TASK}" \
    --overwrite_output_dir
