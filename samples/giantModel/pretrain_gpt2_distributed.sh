#! /bin/bash

set -x

CHECKPOINT_PATH=/root/code2/gpt-ckp/

mkdir -p $CHECKPOINT_PATH

# Change for multinode config
GPUS_PER_NODE=$MLP_WORKER_GPU
MASTER_ADDR=$MLP_WORKER_0_HOST
MASTER_PORT=2222
NNODES=$MLP_WORKER_NUM
export NODE_RANK=$MLP_ROLE_INDEX

export NCCL_DEBUG=DEBUG
export NCCL_IB_DISABLE=0
export NCCL_IB_HCA=mlx5_1:1
export NCCL_IB_GID_INDEX=3
export NCCL_SOCKET_IFNAME=eth0

export WORKER_0_HOST=$MASTER_ADDR
export WORKER_0_PORT=2223
export NUM_WORKER=$NNODES
export WORKER_RANK=$NODE_RANK
export GPU_PER_WORKER=$GPUS_PER_NODE

export BYTEPS_WITH_UCX=0
export DMLC_ENABLE_UCX=0
eval 'export DMLC_NODE_HOST=${MLP_WORKER_'${NODE_RANK}'_HOST}'
export DMLC_ENABLE_RDMA=1
export DMLC_INTERFACE=eth1
export PYTHONPATH=$PYTHONPATH:/root/code/veGiantModel/

WORLD_SIZE=$(($GPUS_PER_NODE*$NNODES))

base_dir=$(cd `dirname $0`; pwd)
echo base_dir $base_dir

cd $base_dir

TENSORBOARD_DIR=''

DISTRIBUTED_ARGS="--nproc_per_node $GPUS_PER_NODE --nnodes $NNODES \
--node_rank $NODE_RANK --master_addr $MASTER_ADDR \
--master_port $MASTER_PORT"

ds_config='{
    "train_micro_batch_size_per_gpu":16,
    "train_batch_size" : 16,
    "gradient_accumulation_steps": 2,
    "steps_per_print": 1,
    "gradient_clipping": 1.0,
    "zero_optimization": {
      "stage": 1,
      "allgather_partitions": true,
      "allgather_bucket_size": 500000000,
      "overlap_comm": false,
      "reduce_scatter": true,
      "reduce_bucket_size": 500000000,
      "contiguous_gradients" : true,
      "cpu_offload": false
    },
    "fp16": {
      "enabled": true,
      "loss_scale": 0,
      "loss_scale_window": 1000,
      "hysteresis": 2,
      "min_loss_scale": 1
    },
    "wall_clock_breakdown": true
}'

mkdir -p /root/code2/gpt-data2
cp /data00/vocab.json /root/code2/gpt-data2
cp /data00/merges.txt /root/code2/gpt-data2
cp /data00/xxx.bin  /root/code2/gpt-data2
cp /data00/xxx.idx  /root/code2/gpt-data2

DATA_PATH=/root/code2/gpt-data2/xxx
VOCAB_FILE=/root/code2/gpt-data2/vocab.json
MERGE_FILE=/root/code2/gpt-data2/merges.txt

python3 -m torch.distributed.launch $DISTRIBUTED_ARGS \
       --no_python --use_env ${PROFILER_CMD} python3 \
       ${base_dir}/pretrain_gpt2.py \
       --model-parallel-size 4 \
       --num-stages 4 \
       --num-layers 30 \
       --hidden-size 3072 \
       --train-batch-size 96 \
       --gradient_accumulation_steps 24 \
       --num-attention-heads 32 \
       --batch-size 4 \
       --seq-length 1024 \
       --max-position-embeddings 1024 \
       --train-iters 500000 \
       --lr-decay-iters 450000 \
       --save $CHECKPOINT_PATH \
       --load $CHECKPOINT_PATH \
       --data-path $DATA_PATH \
       --vocab-file $VOCAB_FILE \
       --merge-file $MERGE_FILE \
       --data-impl mmap \
       --split 949,50,1 \
       --distributed-backend nccl \
       --lr 0.00025 \
       --lr-decay-style cosine \
       --min-lr 1.0e-5 \
       --weight-decay 1e-2 \
       --clip-grad 1.0 \
       --warmup .02 \
       --log-interval 1 \
       --save-interval 5000 \
       --vocab-size 145608 \
       --DDP-impl torch \
       --tensorboard-dir $TENSORBOARD_DIR \
       --eod-mask-loss \
       --deepspeed-pipeline \
       --fp16 \
       --deepspeed \
       --config_param "$ds_config" \
       $@

set +x
