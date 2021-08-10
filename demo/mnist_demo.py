import numpy as np
import tensorflow as tf

import volcengine_ml_platform
from volcengine_ml_platform.datasets import ImageDataset
from volcengine_ml_platform.config import credential as auth_credential

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'
train_path = './train_dataset'
test_path = './test_dataset'
dataset_id = 'd-20210524180450-m592h'

if __name__ == '__main__':
    volcengine_ml_platform.init(auth_credential.Credential(ak, sk, region))

    dataset = ImageDataset(dataset_id=dataset_id)

    dataset.create(local_path='./demo_dataset')

    # split Dataset
    training_dataset, testing_dataset = dataset.split(training_dir=train_path,
                                                      testing_dir=test_path,
                                                      ratio=0.8)

    # prepare training data
    x_train, annotations = training_dataset.load_as_np()
    y_train = np.array(
        [int(x['Result'][0]['Data'][0]['Label']) for x in annotations])

    x_test, annotations = testing_dataset.load_as_np()
    y_test = np.array(
        [int(x['Result'][0]['Data'][0]['Label']) for x in annotations])

    # config model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)

    print('test loss, test acc:')
    model.evaluate(x_test, y_test, verbose=2)
