# 1. 按照volc命令行工具
# 2. volc ml_task submit --config=./samples/cifar/torch_ddp_task_conf.yaml
TaskName: "cifar_pytorch_ddp_example"
Description: ""
# 运行命令
Entrypoint: "python -m torch.distributed.launch
  --master_addr $MLP_WORKER_0_HOST --master_port $MLP_WORKER_0_PORT
  --nnodes=$MLP_WORKER_NUM --nproc_per_node $MLP_WORKER_GPU --node_rank $MLP_ROLE_INDEX
  /root/code/samples/cifar/torch_ddp.py
"

# Args参数，补充空格后，拼接到Entrypoint后面，作为提交给容器运行的entryPoint
Args: "--epoch 100 --batch-size 256"
Tags: []
# 源代码目录，指向运行volc命令行工具电脑上的某一个目录，最多10个文件，10GB大小
UserCodePath: "./samples"

# remote path mount in container
RemoteMountCodePath: "/root/code/"
# user define env var
Envs: []
Image: "ml_platform/pytorch:1.7"
ResourceGroupID: "${replace_with_your_resource_group_id}"
# Distributed training framework, support: TensorFlowPS, PyTorchDDP, Horvod, BytePS, Custom
Framework: "PyTorchDDP"
# 3机2卡
TaskRoleSpecs:
  - RoleName: "worker"
    RoleReplicas: 2
    Flavor: "ml.g1tl.8xlarge"
ActiveDeadlineSeconds: 432000
EnableTensorBoard: true
Storages:
  - Type: "Tos"
    MountPath: "/data00"
    Bucket: "${replace_with_your_tos_bucket_name}"
