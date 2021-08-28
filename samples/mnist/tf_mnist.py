import os

import numpy as np
import tensorflow as tf

from volcengine_ml_platform import constant
from volcengine_ml_platform.tos import tos
from volcengine_ml_platform.util import cache_dir
from volcengine_ml_platform.util import metric

CACHE_DIR = cache_dir.create('mnist/tf_mnist')


def download_dataset_from_tos():
    start_time = metric.current_ts()
    tos_client = tos.TOSClient()
    file_name = 'datasets/mnist.npz'
    dst_path = CACHE_DIR.subpath(file_name)
    tos_client.download_file(
        file_path=dst_path, bucket=constant.PUBLIC_EXAMPLES_TOS_BUCKET, key=file_name,
    )
    print(
        'time-cost(ms)={}, finish download mnist dataset from tos'.format(
            metric.cost_time(start_time),
        ),
    )
    return dst_path


def load_dataset(path):
    with np.load(path, allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']

        return (x_train, y_train), (x_test, y_test)


def get_saved_path():
    return CACHE_DIR.subpath('mnist_model')


def main():
    dataset_local_path = download_dataset_from_tos()
    (x_train, y_train), (x_test, y_test) = load_dataset(dataset_local_path)

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax'),
        ],
    )

    model.compile(
        optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'],
    )
    model.summary()

    log_dir = os.getenv('TENSORBOARD_LOG_PATH', '/tmp/tensorboard_logs/')
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, write_images=False, histogram_freq=1,
    )

    model.fit(x_train, y_train, epochs=5, callbacks=[tensorboard_callback])

    model.evaluate(x_test, y_test, verbose=2)

    tf.saved_model.save(model, get_saved_path())


if __name__ == '__main__':
    main()
    print('finish model training')
