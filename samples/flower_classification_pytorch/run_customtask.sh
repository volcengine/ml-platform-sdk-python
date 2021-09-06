#!/bin/bash
FILE_PATH=$(cd "$(dirname "$0")";pwd)
cd $FILE_PATH
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
export PYTHONPATH="../../"
python -m torch.distributed.launch \
		--nproc_per_node 1 \
		--master_addr $MASTER_ADDR  \
		--node_rank $RANK \
		--master_port $MASTER_PORT  \
		--nnodes=$ML_PLATFORM_WORKER_NUM \
		main.py \
		--cfg ./configs/swin_tiny_patch4_window7_224.yaml \
		--batch-size 32 \
		--load_pretrained
