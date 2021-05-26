import numpy as np
import tensorflow as tf

from ml_platform_sdk.dataset.dataset_service import DatasetService

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'
train_path = './train_dataset'
test_path = './test_dataset'
dataset_id = 'd-20210524180450-m592h'

if __name__ == '__main__':
    client = DatasetService()
    client.set_ak(ak)
    client.set_sk(sk)

    # List Datasets
    # print(client.list_datasets())

    # Get Dataset
    # print(client.get_dataset('d-20210524144453-tr6mp'))

    # Download Dataset
    # manifest = client.download_dataset('d-20210524144453-tr6mp', './')

    # download and split Dataset
    training_dataset, testing_dataset = client.download_and_split_dataset(
        train_path, test_path, dataset_id, limit=1000)

    # prepare training data
    X_train, annotations = training_dataset.load_images_np()
    y_train = np.array(
        [int(x['result'][0]['data'][0]['label']) for x in annotations])

    X_test, annotations = testing_dataset.load_images_np()
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
