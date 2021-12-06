import argparse
import os
import time

import tensorflow as tf


TRAINING_FILENAMES = tf.io.gfile.glob("/data00/imagenet/tfrecord/train*")
os.environ["TF_GPU_THREAD_MODE"] = "gpu_private"
os.environ["TF_GPU_THREAD_COUNT"] = "2"
os.environ["TF_USE_CUDNN_BATCHNORM_SPATIAL_PERSISTENT"] = "1"
tf.keras.backend.set_image_data_format("channels_last")


def parse_common_options():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--use_synthetic_data", action="store_true")
    parser.add_argument("--num_gpus", type=int, default=8)
    parser.add_argument("--num_epochs", type=int, default=10)
    parser.add_argument("--enable_xla", action="store_true")
    parser.add_argument("--enable_mixed_precision", action="store_true")
    args, leftovers = parser.parse_known_args()
    d = args.__dict__
    for key, value in d.items():
        print(f"{key} = {value}")
    return args


FLAGS = parse_common_options()

print("TF version:", tf.__version__)

num_gpus = FLAGS.num_gpus

# 打印所有设备，此时应包含多块远程 GPU，在 ‘/job:worker’下
print("Available GPUs:", tf.config.list_logical_devices("GPU"))


# 输入
def get_synthetic_input_dataset(dtype, batch_size):
    height = 224
    width = 224
    num_channels = 3
    num_classes = 1001
    inputs = tf.random.truncated_normal(
        [height, width, num_channels],
        dtype=dtype,
        mean=127,
        stddev=60,
        name="synthetic_inputs",
    )
    labels = tf.random.uniform(
        [1], minval=0, maxval=num_classes - 1, dtype=tf.int32, name="synthetic_labels"
    )
    # Cast to float32 for Keras model
    labels = tf.cast(labels, dtype=tf.float32)

    data = tf.data.Dataset.from_tensors((inputs, labels)).repeat()
    data = data.batch(batch_size, drop_remainder=True)
    data = data.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return data


def parse_example_proto(example_serialized):
    # 解析一个样本
    feature_map = {
        "image/encoded": tf.io.FixedLenFeature([], dtype=tf.string, default_value=""),
        "image/class/label": tf.io.FixedLenFeature(
            [], dtype=tf.int64, default_value=-1
        ),
        "image/class/text": tf.io.FixedLenFeature(
            [], dtype=tf.string, default_value=""
        ),
    }
    sparse_float32 = tf.io.VarLenFeature(dtype=tf.float32)
    feature_map.update(
        {
            k: sparse_float32
            for k in [
                "image/object/bbox/xmin",
                "image/object/bbox/ymin",
                "image/object/bbox/xmax",
                "image/object/bbox/ymax",
            ]
        }
    )
    features = tf.io.parse_single_example(
        serialized=example_serialized, features=feature_map
    )

    label = tf.cast(features["image/class/label"], dtype=tf.int32)
    xmin = tf.expand_dims(features["image/object/bbox/xmin"].values, 0)
    ymin = tf.expand_dims(features["image/object/bbox/ymin"].values, 0)
    xmax = tf.expand_dims(features["image/object/bbox/xmax"].values, 0)
    ymax = tf.expand_dims(features["image/object/bbox/ymax"].values, 0)

    # Note that we impose an ordering of (y, x) just to make life difficult.
    bbox = tf.concat([ymin, xmin, ymax, xmax], 0)

    # Force the variable number of bounding boxes into the shape
    # [1, num_boxes, coords].
    bbox = tf.expand_dims(bbox, 0)
    bbox = tf.transpose(a=bbox, perm=[0, 2, 1])
    return features["image/encoded"], label, bbox


def decode_crop_and_flip(image_buffer, bbox, num_channels):
    # 随机裁剪翻转
    sample_distorted_bounding_box = tf.image.sample_distorted_bounding_box(
        tf.image.extract_jpeg_shape(image_buffer),
        bounding_boxes=bbox,
        min_object_covered=0.1,
        aspect_ratio_range=[0.75, 1.33],
        area_range=[0.05, 1.0],
        max_attempts=100,
        use_image_if_no_bounding_boxes=True,
    )
    bbox_begin, bbox_size, _ = sample_distorted_bounding_box

    offset_y, offset_x, _ = tf.unstack(bbox_begin)
    target_height, target_width, _ = tf.unstack(bbox_size)
    crop_window = tf.stack([offset_y, offset_x, target_height, target_width])

    cropped = tf.image.decode_and_crop_jpeg(
        image_buffer, crop_window, channels=num_channels
    )
    cropped = tf.image.random_flip_left_right(cropped)
    return cropped


def parse_record_fn(raw_record, dtype):
    height = 224
    width = 224
    num_channels = 3

    # 从 TFRecord 里解析出图片和标签
    image_buffer, label, bbox = parse_example_proto(raw_record)
    # 裁剪翻转
    image = decode_crop_and_flip(image_buffer, bbox, num_channels)
    image = tf.compat.v1.image.resize(
        image,
        [height, width],
        method=tf.image.ResizeMethod.BILINEAR,
        align_corners=False,
    )
    image.set_shape([height, width, num_channels])
    # 标准化
    means = tf.broadcast_to([123.68, 116.78, 103.94], tf.shape(image))
    image -= means
    # 数据表示转换
    image = tf.cast(image, dtype)
    label = tf.cast(
        tf.cast(tf.reshape(label, shape=[1]), dtype=tf.int32) - 1, dtype=tf.float32
    )
    return image, label


def get_input_dataset(dtype, batch_size):
    # 构造数据集
    keys = TRAINING_FILENAMES
    dataset = tf.data.Dataset.from_tensor_slices(keys)
    dataset = dataset.shuffle(buffer_size=len(keys))

    # cycle_length 表示数据集里文件处理的并行度
    dataset = dataset.interleave(
        lambda file: tf.data.TFRecordDataset(file, buffer_size=16 << 20),
        cycle_length=40,
        num_parallel_calls=32,
    )  # tf.data.experimental.AUTOTUNE)

    # 内存足够时使用数据缓存，注意 Turing DevBox 里每张 GPU 会对应 40GB 主存
    # if num_gpus == 8:
    #    dataset = dataset.cache()
    dataset = dataset.shuffle(buffer_size=2000)
    dataset = dataset.repeat()

    dataset = dataset.map(
        lambda value: parse_record_fn(value, dtype),
        num_parallel_calls=tf.data.experimental.AUTOTUNE,
    )
    dataset = dataset.batch(batch_size, drop_remainder=True)

    # 使用数据预取
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    return dataset


# 定义学习速率调度器，采用预热+分段常数衰减策略
class PiecewiseConstantDecayWithWarmup(
    tf.keras.optimizers.schedules.LearningRateSchedule
):
    def __init__(self, batch_size, epoch_size, name=None):
        super().__init__()
        base_lr_batch_size = 256
        steps_per_epoch = epoch_size // batch_size
        base_learning_rate = 0.1
        self.rescaled_lr = base_learning_rate * batch_size / base_lr_batch_size

        # (multiplier, epoch to start) 元组
        lr_schedule = [(1.0, 5), (0.1, 30), (0.01, 60), (0.001, 80)]
        warmup_epochs = lr_schedule[0][1]
        boundaries = list(p[1] for p in lr_schedule[1:])
        multipliers = list(p[0] for p in lr_schedule)
        self.step_boundaries = [float(steps_per_epoch) * x for x in boundaries]
        self.lr_values = [self.rescaled_lr * m for m in multipliers]
        self.warmup_steps = warmup_epochs * steps_per_epoch
        self.compute_lr_on_cpu = True
        self.name = name

    def __call__(self, step):
        # 计算某一步的学习速率
        with tf.name_scope("PiecewiseConstantDecayWithWarmup"):

            def warmup_lr(step):
                return self.rescaled_lr * (
                    tf.cast(step, tf.float32) / tf.cast(self.warmup_steps, tf.float32)
                )

            def piecewise_lr(step):
                return tf.compat.v1.train.piecewise_constant(
                    step, self.step_boundaries, self.lr_values
                )

            return tf.cond(
                step < self.warmup_steps,
                lambda: warmup_lr(step),
                lambda: piecewise_lr(step),
            )

    def get_config(self):
        return {
            "rescaled_lr": self.rescaled_lr,
            "step_boundaries": self.step_boundaries,
            "lr_values": self.lr_values,
            "warmup_steps": self.warmup_steps,
            "compute_lr_on_cpu": self.compute_lr_on_cpu,
            "name": self.name,
        }


# 定义回调输出训练速度
class TimeHistory(tf.keras.callbacks.Callback):
    def __init__(self, batch_size, log_steps):
        self.batch_size = batch_size
        super().__init__()
        self.log_steps = log_steps
        self.last_log_step = 0
        self.steps_before_epoch = 0
        self.steps_in_epoch = 0
        self.start_time = None

    @property
    def global_steps(self):
        return self.steps_before_epoch + self.steps_in_epoch

    def on_batch_begin(self, batch, logs=None):
        if not self.start_time:
            self.start_time = time.time()

    def on_batch_end(self, batch, logs=None):
        self.steps_in_epoch = batch + 1
        steps_since_last_log = self.global_steps - self.last_log_step
        if steps_since_last_log >= self.log_steps:
            now = time.time()
            elapsed_time = now - self.start_time
            steps_per_second = steps_since_last_log / elapsed_time
            examples_per_second = steps_per_second * self.batch_size
            print(
                "TimeHistory: {:.2f} seconds, {:.2f} images/sec between steps {} and {}".format(
                    elapsed_time,
                    examples_per_second,
                    self.last_log_step,
                    self.global_steps,
                )
            )

            self.last_log_step = self.global_steps
            self.start_time = None

    def on_epoch_end(self, epoch, logs=None):
        self.steps_before_epoch += self.steps_in_epoch
        self.steps_in_epoch = 0


def train(dtype, batch_size):
    print(f"batch size: {batch_size}, dtype: {dtype}")
    num_images_to_train = 1281167
    if FLAGS.use_synthetic_data:
        print("Use synthetic data...")
        train_input_dataset = get_synthetic_input_dataset(dtype, batch_size)
    else:
        print("Read TOS TFRecord data...")
        train_input_dataset = get_input_dataset(dtype, batch_size)

    # 多卡训练采用 MirroredStrategy
    # 由于 GPU 间采用 NVlink/NVSwitch 互连，建议使用 NCCL 通信，另一可选方式为 tf.distribute.HierarchicalCopyAllReduce
    devices = ["device:GPU:%d" % i for i in range(num_gpus)]
    strategy = tf.distribute.MirroredStrategy(
        devices=devices, cross_device_ops=tf.distribute.NcclAllReduce(num_packs=1)
    )
    lr_schedule = PiecewiseConstantDecayWithWarmup(batch_size, num_images_to_train)

    # 定义模型
    with strategy.scope():
        optimizer = tf.keras.optimizers.SGD(learning_rate=lr_schedule, momentum=0.9)
        model = tf.keras.applications.resnet50.ResNet50(weights=None)
        # 性能优化：experimental_steps_per_execution 设置越大越好，可减少与远程频繁交互导致的性能损耗
        model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer=optimizer,
            metrics=(["sparse_categorical_accuracy"]),
            run_eagerly=False,
            experimental_steps_per_execution=100,
        )

    # 开始训练
    callback = TimeHistory(batch_size, log_steps=10)
    _ = model.fit(
        train_input_dataset,
        epochs=300,
        steps_per_epoch=num_images_to_train // batch_size,
        callbacks=[callback],
        verbose=2,
    )


# 设置混合精度训练策略
def enable_mixed_precision():
    print("Enable mixed precision training.")
    mixed_precision_policy = tf.keras.mixed_precision.experimental.Policy(
        "mixed_float16", loss_scale=128
    )
    tf.keras.mixed_precision.experimental.set_policy(mixed_precision_policy)
    print("Compute dtype: %s" % mixed_precision_policy.compute_dtype)
    print("Variable dtype: %s" % mixed_precision_policy.variable_dtype)


# For highest speed, please enable mixed precision and xla by running the following command:
# python3 resnet50_multi_gpu.py --enable_mixed_precision --enable_xla
# This script is tested in TF 2.3 and TF 2.4 and can run in local CPU environment, e.g., your Macbook Pro, devbox, container, notebook, linux shell, etc.

# 使用默认数据类型 float32 训练
# 训练速度：单卡 372 images/sec，8卡 2550 images/sec

# 混合精度训练可以使用更大的 batch size
# 单卡 610 images/sec，8卡 4650 images/sec

# 使用 XLA
# 单卡 1160 images/sec，8卡 8600 images/sec

if __name__ == "__main__":
    batch_size = FLAGS.num_gpus * 32  # 192
    if FLAGS.enable_xla:
        tf.config.optimizer.set_jit(True)
    dtype = tf.float32
    if FLAGS.enable_mixed_precision:
        enable_mixed_precision()
        dtype = tf.float16
        # You may set a larger batch size if GPU memory allows.
        batch_size = FLAGS.num_gpus * 32
    train(dtype=dtype, batch_size=batch_size)
