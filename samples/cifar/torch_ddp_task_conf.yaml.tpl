# 1. 按照volc命令行工具
# 2. volc ml_task submit --job_config=./samples/cifiar/torch_ddp_task_conf.yaml

TaskName: "pytorch_ddp_example_from_cli"
Description: ""
# 运行命令
#Entrypoint: "sleep 1d"
Entrypoint: "python -m torch.distributed.launch --nproc_per_node $ML_PLATFORM_WORKER_GPU --master_addr $ML_PLATFORM_WORKER_0_HOST --node_rank $ML_PLATFORM_ROLE_INDEX --master_port $ML_PLATFORM_WORKER_0_PORT --nnodes=$ML_PLATFORM_WORKER_NUM /root/code/samples/cifiar/torch_ddp.py"
# Args参数，补充空格后，拼接到Entrypoint后面，作为提交给容器运行的entryPoint
Args: "--epoch 1000 --batch-size 256"
Tags: []
# 源代码目录，指向运行volc命令行工具电脑上的某一个目录，最多10个文件，10GB大小
UserCodePath: "./samples"

# remote path mount in container
RemoteMountCodePath: "/root/code/"
# user define env var
Envs: []
Image: "ml_platform/pytorch:1.7"
ResourceGroupID: "${repleace_with_your_resource_group_id}"
# Distributed training framework, support: TensorFlowPS, PyTorchDDP, Horvod, BytePS, Custom
Framework: "PyTorchDDP"
# 3机2卡
TaskRoleSpecs:
  - RoleName: "worker"
    RoleReplicas: 2
    Flavor: "ml.g1v.8xlarge"
ActiveDeadlineSeconds: 432000
EnableTensorBoard: false
Storages:
  - Type: "Tos"
    MountPath: "/data00"
    Bucket: "jingyan-test"
