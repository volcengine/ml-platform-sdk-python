# How to run giant Model samples on volcengine
1. git clone --recusive https://github.com/volcengine/veGiantModel

2. modify 16_gpus.yaml with followings:
    a. change "UserCodePath" field to point to the local path where
      veGiantModel is. For example, if first step was run at
      path /Users/user1/workspace, then set
      UserCodePath: "/Users/user1/workspace/veGiantModel".
    b. change "ResourceGroupID" field accordingly.
    c. if tos is needed, uncomment "Storages" and change "Bucket" accordingly.
    d. change "TaskName" accordingly if needed.

3. modify pretrain_gpt2_distributed.sh
     a. change TENSORBOARD_DIR value accordingly
     b. change Line 73-76 to copy training data from tos
       (assuming training stored in tos and tos is mounted at /data00).
     c. change Line 78-80 accordingly so that DATA_PATH/VOCAB_FILE/MERGE_FILE
       point to correct file path.

4. replace veGiantModel/examples/gpt/pretrain_gpt2_distributed.sh with
    pretrain_gpt2_distributed.sh script in this folder modified in step 3.
5. submit task: volc ml_task submit --job_config=16_gpus.yaml
