import argparse
import os
import re
import sys

import numpy as np
import tensorflow as tf

from samples.models.swin_transformer_tensorflow.model import SwinTransformer
from volcengine_ml_platform import constant
from volcengine_ml_platform.io import tos
from volcengine_ml_platform.models.model import Model
from volcengine_ml_platform.util import cache_dir
from volcengine_ml_platform.util import metric

sys.path.append("../..")

BUCKET = constant.get_public_examples_readonly_bucket()
CACHE_DIR = cache_dir.create("flower_classification/swin_transformer_tf")

AUTO = tf.data.experimental.AUTOTUNE

client = tos.TOSClient()
DATASET_PATH = "s3://{}/flower-classification/tfrecords/tfrecords-jpeg-224x224".format(
    BUCKET,
)
TRAINING_FILENAMES = tf.io.gfile.glob(DATASET_PATH + "/train/*.tfrec")
VALIDATION_FILENAMES = tf.io.gfile.glob(DATASET_PATH + "/val/*.tfrec")
TEST_FILENAMES = tf.io.gfile.glob(DATASET_PATH + "/test/*.tfrec")

CHECKPOINT_PATH = "s3://{}/flower-classification/checkpoints/tf/cp.ckpt".format(
    BUCKET,
)

CLASSES = [
    "pink primrose",
    "hard-leaved pocket orchid",
    "canterbury bells",
    "sweet pea",
    "wild geranium",
    "tiger lily",
    "moon orchid",
    "bird of paradise",
    "monkshood",
    "globe thistle",  # 00 - 09
    "snapdragon",
    "colt's foot",
    "king protea",
    "spear thistle",
    "yellow iris",
    "globe-flower",
    "purple coneflower",
    "peruvian lily",
    "balloon flower",
    "giant white arum lily",  # 10 - 19
    "fire lily",
    "pincushion flower",
    "fritillary",
    "red ginger",
    "grape hyacinth",
    "corn poppy",
    "prince of wales feathers",
    "stemless gentian",
    "artichoke",
    "sweet william",  # 20 - 29
    "carnation",
    "garden phlox",
    "love in the mist",
    "cosmos",
    "alpine sea holly",
    "ruby-lipped cattleya",
    "cape flower",
    "great masterwort",
    "siam tulip",
    "lenten rose",  # 30 - 39
    "barberton daisy",
    "daffodil",
    "sword lily",
    "poinsettia",
    "bolero deep blue",
    "wallflower",
    "marigold",
    "buttercup",
    "daisy",
    "common dandelion",  # 40 - 49
    "petunia",
    "wild pansy",
    "primula",
    "sunflower",
    "lilac hibiscus",
    "bishop of llandaff",
    "gaura",
    "geranium",
    "orange dahlia",
    "pink-yellow dahlia",  # 50 - 59
    "cautleya spicata",
    "japanese anemone",
    "black-eyed susan",
    "silverbush",
    "californian poppy",
    "osteospermum",
    "spring crocus",
    "iris",
    "windflower",
    "tree poppy",  # 60 - 69
    "gazania",
    "azalea",
    "water lily",
    "rose",
    "thorn apple",
    "morning glory",
    "passion flower",
    "lotus",
    "toad lily",
    "anthurium",  # 70 - 79
    "frangipani",
    "clematis",
    "hibiscus",
    "columbine",
    "desert-rose",
    "tree mallow",
    "magnolia",
    "cyclamen ",
    "watercress",
    "canna lily",  # 80 - 89
    "hippeastrum ",
    "bee balm",
    "pink quill",
    "foxglove",
    "bougainvillea",
    "camellia",
    "mallow",
    "mexican petunia",
    "bromelia",
    "blanket flower",  # 90 - 99
    "trumpet creeper",
    "blackberry lily",
    "common tulip",
    "wild rose",
]


def decode_image(image_data):
    # image format uint8 [0,255]
    image = tf.image.decode_jpeg(image_data, channels=3)
    image = tf.reshape(image, [*IMAGE_SIZE, 3])  # explicit size needed for TPU
    return image


def read_labeled_tfrecord(example):
    labeled_tfrec_format = {
        # tf.string means bytestring
        "image": tf.io.FixedLenFeature([], tf.string),
        # shape [] means single element
        "class": tf.io.FixedLenFeature([], tf.int64),
    }
    example = tf.io.parse_single_example(example, labeled_tfrec_format)
    image = decode_image(example["image"])
    label = tf.cast(example["class"], tf.int32)
    return image, label  # returns a dataset of (image, label) pairs


def read_unlabeled_tfrecord(example):
    unlabeled_tfrec_format = {
        # tf.string means bytestring
        "image": tf.io.FixedLenFeature([], tf.string),
        # shape [] means single element
        "id": tf.io.FixedLenFeature([], tf.string),
        # class is missing
    }
    example = tf.io.parse_single_example(example, unlabeled_tfrec_format)
    image = decode_image(example["image"])
    idnum = example["id"]
    return image, idnum  # returns a dataset of image(s)


def load_dataset(filenames, labeled=True, ordered=False):
    # Read from TFRecords. For optimal performance, reading from multiple files at once and
    # disregarding data order. Order does not matter since we will be shuffling the data anyway.

    ignore_order = tf.data.Options()
    if not ordered:
        ignore_order.experimental_deterministic = False  # disable order, increase speed

    dataset = tf.data.TFRecordDataset(
        filenames,
        num_parallel_reads=AUTO,
    )  # automatically interleaves reads from multiple files
    dataset = dataset.with_options(
        ignore_order,
    )  # uses data as soon as it streams in, rather than in its original order
    dataset = dataset.map(
        read_labeled_tfrecord if labeled else read_unlabeled_tfrecord,
        num_parallel_calls=AUTO,
    )
    # returns a dataset of (image, label) pairs
    # if labeled=True or (image, id) pairs if labeled=False
    print(dataset)
    return dataset


def data_augment(image, label):
    # data augmentation.
    # Thanks to the dataset.prefetch(AUTO) statement in the next function (below),
    # this happens essentially for free on TPU. Data pipeline code is executed on the "CPU" part
    # of the TPU while the TPU itself is computing gradients.
    image = tf.image.random_flip_left_right(image)
    # image = tf.image.random_saturation(image, 0, 2)
    return image, label


def get_training_dataset():
    dataset = load_dataset(TRAINING_FILENAMES, labeled=True)
    dataset = dataset.map(data_augment, num_parallel_calls=AUTO)
    dataset = dataset.repeat()  # the training dataset must repeat for several epochs
    dataset = dataset.shuffle(2048)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    dataset = dataset.prefetch(
        AUTO,
    )  # prefetch next batch while training (autotune prefetch buffer size)
    return dataset


def get_validation_dataset(ordered=False):
    dataset = load_dataset(VALIDATION_FILENAMES, labeled=True, ordered=ordered)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    dataset = dataset.cache()
    dataset = dataset.prefetch(
        AUTO,
    )  # prefetch next batch while training (autotune prefetch buffer size)
    return dataset


def get_test_dataset(ordered=False):
    dataset = load_dataset(TEST_FILENAMES, labeled=False, ordered=ordered)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(
        AUTO,
    )  # prefetch next batch while training (autotune prefetch buffer size)
    return dataset


def count_data_items(filenames):
    # the number of data items is written in the name of the .tfrec files
    # i.e. flowers00-230.tfrec = 230 data items
    num = [
        int(re.compile(r"-([0-9]*)\.").search(filename).group(1))
        for filename in filenames
    ]
    return np.sum(num)


def get_datasets_info():
    num_training_images = count_data_items(TRAINING_FILENAMES)
    num_validation_images = count_data_items(VALIDATION_FILENAMES)
    num_test_images = count_data_items(TEST_FILENAMES)
    print(
        "Dataset: {} training images, {} validation images, {} unlabeled test images".format(
            num_training_images,
            num_validation_images,
            num_test_images,
        ),
    )
    return num_training_images, num_validation_images, num_test_images


def download_pretrained_ckpt_from_tos():
    start_time = metric.current_ts()
    tos_client = tos.TOSClient()
    file_name = "swin_tiny_224.tar.gz"
    dst_path = CACHE_DIR.subpath(file_name)
    tos_client.download_file(
        file_path=dst_path,
        bucket=BUCKET,
        key="flower-classification/swin_tiny_224.tar.gz",
    )
    print(
        "time-cost(ms)={}, finish dowload pretrain_ckpt from tos".format(
            metric.cost_time(start_time),
        ),
    )
    return CACHE_DIR.get_root_path()


if __name__ == "__main__":
    # args parser
    parser = argparse.ArgumentParser(
        description="Swin Transformer Training Example",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="input batch size for training",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="number of epochs to train",
    )
    parser.add_argument(
        "--steps-per-epoch",
        type=int,
        help="number of steps per epoch to train",
    )
    parser.add_argument(
        "--validation-steps",
        type=int,
        help="number of validation steps per epoch to train",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default="mirrored",
        help="number of validation steps per epoch to train",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        help="the path to load checkpoints",
    )

    args = parser.parse_args()

    # select a strategy
    if args.strategy == "default":
        strategy = (
            tf.distribute.get_strategy()
        )  # default strategy that works on CPU and single GPU
    elif args.strategy == "mirrored":
        strategy = tf.distribute.MirroredStrategy()  # for GPU or multi-GPU machines
    print("Number of accelerators: ", strategy.num_replicas_in_sync)

    # For GPU training, please select 224 x 224 px image size.
    IMAGE_SIZE = [224, 224]
    BATCH_SIZE = (
        16 * strategy.num_replicas_in_sync
        if args.batch_size is None
        else args.batch_size
    )

    NUM_TRAINING_IMAGES, NUM_VALIDATION_IMAGES, NUM_TEST_IMAGES = get_datasets_info()

    STEPS_PER_EPOCH = (
        NUM_TRAINING_IMAGES // BATCH_SIZE
        if args.steps_per_epoch is None
        else args.steps_per_epoch
    )

    VALIDATION_STEPS = (
        -(-NUM_VALIDATION_IMAGES // BATCH_SIZE)
        if args.validation_steps is None
        else args.validation_steps
    )

    EPOCHS = args.epochs

    pretrained_ckpt_path = download_pretrained_ckpt_from_tos()

    # build models
    with strategy.scope():
        img_adjust_layer = tf.keras.layers.Lambda(
            lambda data: tf.keras.applications.imagenet_utils.preprocess_input(
                tf.cast(data, tf.float32),
                mode="torch",
            ),
            input_shape=[*IMAGE_SIZE, 3],
        )
        pretrained_model = SwinTransformer(
            "swin_tiny_224",
            num_classes=len(CLASSES),
            include_top=False,
            cache_dir=pretrained_ckpt_path,
        )

        model = tf.keras.Sequential(
            [
                img_adjust_layer,
                pretrained_model,
                tf.keras.layers.Dense(len(CLASSES), activation="softmax"),
            ],
        )

        if args.checkpoint is not None:
            model.load_weights(args.checkpoint)
            print("load checkpoint successfully")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5, epsilon=1e-8),
        loss="sparse_categorical_crossentropy",
        metrics=["sparse_categorical_accuracy"],
    )
    model.summary()

    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=CHECKPOINT_PATH,
        save_weights_only=True,
        verbose=1,
    )

    # tensorboard
    log_dir = os.getenv(
        "TENSORBOARD_LOG_PATH",
        default=os.path.join(os.path.dirname(__file__), "tensorboard_logs"),
    )
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir,
        write_images=False,
        histogram_freq=1,
    )

    callbacks = [model_checkpoint_callback, tensorboard_callback]

    # train models
    HISTORY = model.fit(
        get_training_dataset(),
        steps_per_epoch=STEPS_PER_EPOCH,
        epochs=EPOCHS,
        validation_data=get_validation_dataset(),
        validation_steps=VALIDATION_STEPS,
        callbacks=callbacks,
    )

    SAVED_MODEL_PATH = CACHE_DIR.subpath("tf_saved_model")
    model.save(SAVED_MODEL_PATH)

    # register new model_version to mlplatform.model_repo
    model = Model(local_path=SAVED_MODEL_PATH)
    model.register(
        model_name="test-swin-transformer-model",
        model_format="SavedModel",
        model_type="TensorFlow:2.4",
        description="Flower Classification Model",
    )

    # get models detail
    model.print()

    # deploy the selected model_version
    inference_service = model.deploy(
        flavor="ml.highcpu.large",
        replica=1,
        model_version=1,
        image_id="machinelearning/tfserving:tf-cuda11.0",
    )
