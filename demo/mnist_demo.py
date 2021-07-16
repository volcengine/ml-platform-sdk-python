import numpy as np
import tensorflow as tf

import ml_platform_sdk
from ml_platform_sdk.datasets import ImageDataset
from ml_platform_sdk.config import credential as auth_credential

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-qingdao'
train_path = './train_dataset'
test_path = './test_dataset'
dataset_id = 'd-20210524180450-m592h'

if __name__ == '__main__':
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    dataset = ImageDataset(dataset_id=dataset_id)

    dataset.create(local_path='./demo_dataset')

    # split Dataset
    training_dataset, testing_dataset = dataset.split(training_dir=train_path,
                                                      testing_dir=test_path,
                                                      ratio=0.8)

    # prepare training data
    X_train, annotations = training_dataset.load_as_np()
    y_train = np.array(
        [int(x['result'][0]['data'][0]['label']) for x in annotations])

    X_test, annotations = testing_dataset.load_as_np()
    y_test = np.array(
        [int(x['result'][0]['data'][0]['label']) for x in annotations])

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

    model.fit(X_train, y_train, epochs=5)

    print('test loss, test acc:')
    model.evaluate(X_test, y_test, verbose=2)
