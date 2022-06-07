# vepfs存储测试说明
使用`PyTorch`与`Tensorflow`构建`ResNet-50`分类模型，从vepfs加载数据进行训练测试，其中数据为`ILSVRC2012`,并将其扩充10倍及转换为`TFRecord`格式，共形成四种训练数据：

1. `ILSVRC2012`

2. `ILSVRC2012-Large`
3. `ILSVRC2012-TF`
4. `ILSVRC2012-TF-Large`

将训练数据和依赖文件下载到个人vepfs中，其挂载路径为`{MountPath}`，文件列表为：

```
|-{MountPath}
    |-imgnet
        |-ILSVRC2012
        |-ILSVRC2012-Large
        |-ILSVRC2012-TF
        |-ILSVRC2012-TF-Large
        |-val
    |-pkg
        |-dllogger
        |-nvidia_dali_cuda110-1.6.0-2993096-py3-none-manylinux2014_x86_64.whl
```

---

## PyTorch

Image: `ml_platform/Pytorch:1.7`

假设远程代码路径`RemoteMountCodePath`为`/root/code`

需要安装依赖库：

1. 安装`torchvision`与`nvidia-pyindex`，

   `cd /root/code/ml_benchmark/ConvNets && pip install -r ./requirements.txt`

2. 安装`nvidia-dllogger`，

   - `pip install nvidia-dllogger`,网络环境良好时，可以将其放入`requirements.txt`中与上一条一同执行；
   - 网络不好时，使用离线安装方式，获取离线文件后安装：`cd {MountPath}/pkg/dllogger && pip install .`

3. 安装`nvidia-dali-cuda110`
   - 网络良好时，`pip install --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110`
   - 离线安装，`pip install {MountPath}/pkg/nvidia_dali_cuda110-1.6.0-2993096-py3-none-manylinux2014_x86_64.whl`

- 使用`ILSVRC2012`训练，`Entrypoint`为:

  ```bash
  cd /root/code/ml_benchmark/ConvNets && pip install -r ./requirements.txt && cd {MountPath}/pkg/dllogger && pip install . && pip install {MountPath}/pkg/nvidia_dali_cuda110-1.6.0-2993096-py3-none-manylinux2014_x86_64.whl && cd /root/code/ml_benchmark/ConvNets && python3 ./multiproc.py --nproc_per_node 8 ./launch.py --model resnet50 --precision AMP --mode benchmark_training --platform DGX1V {MountPath}/imgnet/ILSVRC2012/train --raport-file benchmark.json --epochs 400 --training-only
  ```

- 使用`ILSVRC2012-Large`训练，`Entrypoint`为:

  ```bash
  cd /root/code/ml_benchmark/ConvNets && pip install -r ./requirements.txt && cd {MountPath}/pkg/dllogger && pip install . && pip install {MountPath}/pkg/nvidia_dali_cuda110-1.6.0-2993096-py3-none-manylinux2014_x86_64.whl && cd /root/code/ml_benchmark/ConvNets && python3 ./multiproc.py --nproc_per_node 8 ./launch.py --model resnet50 --precision AMP --mode benchmark_training --platform DGX1V {MountPath}/imgnet/ILSVRC2012-Large/train --raport-file benchmark.json --epochs 400 --num_classes 10000 --training-only
  ```

---

## TensorFlow

Image: `ml_platform/tensorflow:2.4`

- 使用`ILSVRC2012-TF`训练，`Entrypoint`为:

  ```bash
  cd /root/code/ml_tf_benchmark/image_classification/tensorflow2 && sh run_8gpus_training_on_posix_data.sh
  ```

- 使用`ILSVRC2012-TF-Large`训练，需要`Entrypoint`为:

  ~~~bash
  cd /root/code/ml_tf_benchmark/image_classification/tensorflow2 && sh run_8gpus_training_on_posix_data_large.sh
  ~~~

需要到`run_8gpus_training_on_posix_data.sh`与`run_8gpus_training_on_posix_data_large.sh`中更改训练数据目录及分类数目。

---

训练过程中的日志信息存放在`/root/logs/log`中。
