import os
import re
import shutil
import argparse
import tensorflow as tf
import numpy as np
from swintransformer import SwinTransformer
from volcengine_ml_platform.tos import tos
from volcengine_ml_platform.modelrepo.models import Model
from volcengine_ml_platform.config import credential as auth_credential
import volcengine_ml_platform

AUTO = tf.data.experimental.AUTOTUNE

REGION_NAME = "cn-north-1"
END_POINT = "http://boe-s3-official-test.volces.com"
AC_AK = "AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE"
AC_SK = "WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=="
BUCKET = "tfrecord"

os.environ["AWS_REGION"] = REGION_NAME
os.environ["AWS_ACCESS_KEY_ID"] = AC_AK
os.environ["AWS_SECRET_ACCESS_KEY"] = AC_SK
os.environ["S3_ENDPOINT"] = END_POINT

GCS_PATH = 's3://tfrecord/flower-classification-with-tpus/tfrecords-jpeg-224x224'
TRAINING_FILENAMES = tf.io.gfile.glob(GCS_PATH + '/train/*.tfrec')
VALIDATION_FILENAMES = tf.io.gfile.glob(GCS_PATH + '/val/*.tfrec')
TEST_FILENAMES = tf.io.gfile.glob(
    GCS_PATH + '/test/*.tfrec'
)  # predictions on this dataset should be submitted for the competition

CLASSES = [
    'pink primrose',
    'hard-leaved pocket orchid',
    'canterbury bells',
    'sweet pea',
    'wild geranium',
    'tiger lily',
    'moon orchid',
    'bird of paradise',
    'monkshood',
    'globe thistle',  # 00 - 09
    'snapdragon',
    "colt's foot",
    'king protea',
    'spear thistle',
    'yellow iris',
    'globe-flower',
    'purple coneflower',
    'peruvian lily',
    'balloon flower',
    'giant white arum lily',  # 10 - 19
    'fire lily',
    'pincushion flower',
    'fritillary',
    'red ginger',
    'grape hyacinth',
    'corn poppy',
    'prince of wales feathers',
    'stemless gentian',
    'artichoke',
    'sweet william',  # 20 - 29
    'carnation',
    'garden phlox',
    'love in the mist',
    'cosmos',
    'alpine sea holly',
    'ruby-lipped cattleya',
    'cape flower',
    'great masterwort',
    'siam tulip',
    'lenten rose',  # 30 - 39
    'barberton daisy',
    'daffodil',
    'sword lily',
    'poinsettia',
    'bolero deep blue',
    'wallflower',
    'marigold',
    'buttercup',
    'daisy',
    'common dandelion',  # 40 - 49
    'petunia',
    'wild pansy',
    'primula',
    'sunflower',
    'lilac hibiscus',
    'bishop of llandaff',
    'gaura',
    'geranium',
    'orange dahlia',
    'pink-yellow dahlia',  # 50 - 59
    'cautleya spicata',
    'japanese anemone',
    'black-eyed susan',
    'silverbush',
    'californian poppy',
    'osteospermum',
    'spring crocus',
    'iris',
    'windflower',
    'tree poppy',  # 60 - 69
    'gazania',
    'azalea',
    'water lily',
    'rose',
    'thorn apple',
    'morning glory',
    'passion flower',
    'lotus',
    'toad lily',
    'anthurium',  # 70 - 79
    'frangipani',
    'clematis',
    'hibiscus',
    'columbine',
    'desert-rose',
    'tree mallow',
    'magnolia',
    'cyclamen ',
    'watercress',
    'canna lily',  # 80 - 89
    'hippeastrum ',
    'bee balm',
    'pink quill',
    'foxglove',
    'bougainvillea',
    'camellia',
    'mallow',
    'mexican petunia',
    'bromelia',
    'blanket flower',  # 90 - 99
    'trumpet creeper',
    'blackberry lily',
    'common tulip',
    'wild rose'
]


def decode_image(image_data):
    image = tf.image.decode_jpeg(image_data,
                                 channels=3)  # image format uint8 [0,255]
    image = tf.reshape(image, [*IMAGE_SIZE, 3])  # explicit size needed for TPU
    return image


def read_labeled_tfrecord(example):
    labeled_tfrec_format = {
        "image": tf.io.FixedLenFeature([],
                                       tf.string),  # tf.string means bytestring
        "class": tf.io.FixedLenFeature(
            [], tf.int64),  # shape [] means single element
    }
    example = tf.io.parse_single_example(example, labeled_tfrec_format)
    image = decode_image(example['image'])
    label = tf.cast(example['class'], tf.int32)
    return image, label  # returns a dataset of (image, label) pairs


def read_unlabeled_tfrecord(example):
    unlabeled_tfrec_format = {
        "image": tf.io.FixedLenFeature([],
                                       tf.string),  # tf.string means bytestring
        "id": tf.io.FixedLenFeature([],
                                    tf.string),  # shape [] means single element
        # class is missing
    }
    example = tf.io.parse_single_example(example, unlabeled_tfrec_format)
    image = decode_image(example['image'])
    idnum = example['id']
    return image, idnum  # returns a dataset of image(s)


def load_dataset(filenames, labeled=True, ordered=False):
    # Read from TFRecords. For optimal performance, reading from multiple files at once and
    # disregarding data order. Order does not matter since we will be shuffling the data anyway.

    ignore_order = tf.data.Options()
    if not ordered:
        ignore_order.experimental_deterministic = False  # disable order, increase speed

    dataset = tf.data.TFRecordDataset(
        filenames, num_parallel_reads=AUTO
    )  # automatically interleaves reads from multiple files
    dataset = dataset.with_options(
        ignore_order
    )  # uses data as soon as it streams in, rather than in its original order
    dataset = dataset.map(
        read_labeled_tfrecord if labeled else read_unlabeled_tfrecord,
        num_parallel_calls=AUTO)
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
    dataset = dataset.repeat(
    )  # the training dataset must repeat for several epochs
    dataset = dataset.shuffle(2048)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    dataset = dataset.prefetch(
        AUTO
    )  # prefetch next batch while training (autotune prefetch buffer size)
    return dataset


def get_validation_dataset(ordered=False):
    dataset = load_dataset(VALIDATION_FILENAMES, labeled=True, ordered=ordered)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    dataset = dataset.cache()
    dataset = dataset.prefetch(
        AUTO
    )  # prefetch next batch while training (autotune prefetch buffer size)
    return dataset


def get_test_dataset(ordered=False):
    dataset = load_dataset(TEST_FILENAMES, labeled=False, ordered=ordered)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(
        AUTO
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
        'Dataset: {} training images, {} validation images, {} unlabeled test images'
        .format(num_training_images, num_validation_images, num_test_images))
    return num_training_images, num_validation_images, num_test_images


def get_pretrained_from_tos():
    tos_client = tos.TOSClient(
        auth_credential.Credential(AC_AK, AC_SK, REGION_NAME))
    obj = tos_client.get_object(bucket="tfrecord", key="swin_tiny_224.tar.gz")

    src_path = os.path.join(os.path.dirname(__file__), "swin_tiny_224.tar.gz")
    dst_path = "/root/.keras/datasets/swin_tiny_224.tar.gz"

    with open(src_path, "wb") as file:
        file.write(obj.read())

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.move(src_path, dst_path)


if __name__ == '__main__':

    # args parser
    parser = argparse.ArgumentParser(
        description='Swin Transformer Training Example')
    parser.add_argument('--batch-size',
                        type=int,
                        help='input batch size for training')
    parser.add_argument('--epochs',
                        type=int,
                        default=10,
                        help='number of epochs to train')
    parser.add_argument('--steps-per-epoch',
                        type=int,
                        help='number of epochs to train')
    parser.add_argument('--validation-steps',
                        type=int,
                        help='number of epochs to train')

    args = parser.parse_args()

    # detect GPUs
    strategy = tf.distribute.MirroredStrategy()  # for GPU or multi-GPU machines
    # strategy = tf.distribute.get_strategy()
    # default strategy that works on CPU and single GPU
    # strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
    # # for clusters of multi-GPU machines
    print("Number of accelerators: ", strategy.num_replicas_in_sync)

    IMAGE_SIZE = [224, 224
                 ]  # For GPU training, please select 224 x 224 px image size.
    BATCH_SIZE = 16 * strategy.num_replicas_in_sync if args.batch_size is None else args.batch_size

    NUM_TRAINING_IMAGES, NUM_VALIDATION_IMAGES, NUM_TEST_IMAGES = get_datasets_info(
    )

    STEPS_PER_EPOCH = NUM_TRAINING_IMAGES // BATCH_SIZE if args.steps_per_epoch is None else args.steps_per_epoch

    VALIDATION_STEPS = -(
        -NUM_VALIDATION_IMAGES //
        BATCH_SIZE) if args.validation_steps is None else args.validation_steps

    EPOCHS = args.epochs

    get_pretrained_from_tos()

    # build model
    with strategy.scope():
        img_adjust_layer = tf.keras.layers.Lambda(
            lambda data: tf.keras.applications.imagenet_utils.preprocess_input(
                tf.cast(data, tf.float32), mode="torch"),
            input_shape=[*IMAGE_SIZE, 3])
        pretrained_model = SwinTransformer('swin_tiny_224',
                                           num_classes=len(CLASSES),
                                           include_top=False,
                                           pretrained=True)

        model = tf.keras.Sequential([
            img_adjust_layer, pretrained_model,
            tf.keras.layers.Dense(len(CLASSES), activation='softmax')
        ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5,
                                                     epsilon=1e-8),
                  loss='sparse_categorical_crossentropy',
                  metrics=['sparse_categorical_accuracy'])
    model.summary()

    # tensorboard
    log_dir = os.getenv("TENSORBOARD_LOG_PATH",
                        default=os.path.join(os.path.dirname(__file__),
                                             "tensorboard_logs"))
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir,
                                                          write_images=False,
                                                          histogram_freq=1)

    # train model
    HISTORY = model.fit(get_training_dataset(),
                        steps_per_epoch=STEPS_PER_EPOCH,
                        epochs=EPOCHS,
                        validation_data=get_validation_dataset(),
                        validation_steps=VALIDATION_STEPS,
                        callbacks=[tensorboard_callback])

    SAVED_MODEL_PATH = os.path.join(os.path.dirname(__file__), "tf_save/1")
    model.save(SAVED_MODEL_PATH)

    # register new model_version to mlplatform.model_repo
    volcengine_ml_platform.init(auth_credential.Credential(AC_AK, AC_SK, REGION_NAME))
    model = Model(local_path=SAVED_MODEL_PATH)
    model.register(model_name='swinTransformerTestModel',
                   model_format='SavedModel',
                   model_type='TensorFlow:2.4',
                   description='Flower Classification Model')

    # get model detail
    model.print()

    # deploy the selected model_version
    inference_service = model.deploy(
        flavor='ml.highcpu.large',
        replica=1,
        model_version=1,
        image_url=
        "cr-stg-cn-beijing.volces.com/machinelearning/tfserving:tf-cuda11.0")
