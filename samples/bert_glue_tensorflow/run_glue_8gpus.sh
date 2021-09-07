#!/bin/bash


pathvar="$( cd "$( dirname $0 )" && pwd )"
cd $pathvar
python3 -m pip install -r ./requirements.txt --user

TASK="MRPC"
GLUE_DIR=$HOME/.volcengine_ml_platform/samples/bert_glue/glue_data
BERT_BASE_DIR=$HOME/.volcengine_ml_platform/samples/bert_glue/uncased_L-12_H-768_A-12-model

mpirun -np 8 \
    -H localhost:4 \
    -bind-to none -map-by slot \
    -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH \
    -mca pml ob1 -mca btl ^openib \
    --oversubscribe \
    python3 ./main.py \
    --task_name=$TASK \
    --do_train=true \
    --do_eval=true \
    --data_dir=$GLUE_DIR/$TASK \
    --vocab_file=$BERT_BASE_DIR/vocab.txt \
    --bert_config_file=$BERT_BASE_DIR/bert_config.json \
    --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
    --max_seq_length=128 \
    --train_batch_size=32 \
    --learning_rate=2e-5 \
    --num_train_epochs=3.0 \
    --output_dir=/tmp/mrpc_output/
