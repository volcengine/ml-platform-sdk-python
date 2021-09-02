#!/bin/bash


TASK="MRPC"
GLUE_DIR="./download_data/glue_data"
BERT_BASE_DIR='./download_model/bert-base-uncased'

python3.7 -m torch.distributed.launch --nproc_per_node 8 ./run_glue.py \
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
    --output_dir /tmp/$TASK/ \
    --overwrite_output_dir
