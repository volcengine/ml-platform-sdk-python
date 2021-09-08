import pathlib
import random
import time

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPool2D


try:
    import env

    env.init()
except Exception:
    pass


DATA_PATH = "s3://chinese-mnist/data"
BATCH_SIZE = 32


def load_and_preprocess_from_path_label(path, label):

    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, size=[64, 64])
    image /= 255.0

    return image, label


def create_dataset(data_root):
    print("start count image num")
    all_image_paths = tf.io.gfile.glob(data_root + "/*.jpg")
    print("image num:", len(all_image_paths))
    random.shuffle(all_image_paths)

    label_names = sorted({item.split("_")[-1] for item in all_image_paths})
    label_to_index = {name: index for index, name in enumerate(label_names)}
    print("label num:", len(label_names))

    all_image_labels = [
        label_to_index[pathlib.Path(path).name.split("_")[-1]]
        for path in all_image_paths
    ]

    ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))
    image_label_ds = ds.map(
        load_and_preprocess_from_path_label, num_parallel_calls=32, deterministic=False
    )
    ds = image_label_ds.shuffle(buffer_size=2048)
    ds = ds.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return ds


dataset = create_dataset(DATA_PATH)
# Be careful do NOT batch before '.take()' or '.skip()', it should be the samples number but
# not the batches number to be considered
test_ds = dataset.take(1000)
train_ds = dataset.skip(1000)
train_length = 14000
test_length = 1000
# Be careful for the '.repeat()' applied on tf dataset, if a repeated dataset is iterated
# in the loop like 'for x, y in dataset: ...', it will cause a ever-loop that never
# break, thus manually breaking is needed
train_ds = train_ds.batch(BATCH_SIZE).repeat()
test_ds = test_ds.batch(BATCH_SIZE).repeat()


class Net(Model):
    def __init__(self):
        super().__init__()

        self.conv1 = Conv2D(32, 3, padding="same", activation="relu")
        self.pool1 = MaxPool2D(3, padding="same")
        self.flatten = Flatten()
        self.fc1 = Dense(128, activation="relu")
        self.fc2 = Dense(15, activation="softmax")

    def call(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.flatten(x)
        x = self.fc1(x)
        return self.fc2(x)


model = Net()

from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Mean, SparseCategoricalAccuracy

loss_object = SparseCategoricalCrossentropy(from_logits=True)
optimizer = Adam()

train_loss = Mean("train_loss")
train_acc = SparseCategoricalAccuracy("train_acc")

test_loss = Mean("test_loss")
test_acc = SparseCategoricalAccuracy("test_acc")


@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = loss_object(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_acc(y, predictions)


@tf.function
def test_step(x, y):
    predictions = model(x)
    loss = loss_object(y, predictions)

    test_loss(loss)
    test_acc(y, predictions)


print("### Starting ###")

EPOCHS = 10

for epoch in range(EPOCHS):
    print("epoch=" + str(epoch))

    train_loss.reset_states()
    train_acc.reset_states()
    test_loss.reset_states()
    test_acc.reset_states()
    idx = 0
    start = time.time()
    for x, y in train_ds:
        if idx % 100 == 0:
            print(f"{idx} train speed: {100 * BATCH_SIZE / (time.time() - start)}")
            start = time.time()
        idx += 1
        train_step(x, y)
        # have to break manually
        if idx * BATCH_SIZE >= train_length:
            break
    idx_ = 0
    for x, y in test_ds:
        if idx_ % 100 == 0:
            print(f"{idx_} val speed: {100 * BATCH_SIZE / (time.time() - start)}")
            start = time.time()
        idx_ += 1
        test_step(x, y)
        # have to break manually
        if idx_ * BATCH_SIZE >= test_length:
            break

    print(
        f"Epoch {epoch + 1}, "
        f"Loss: {train_loss.result()}, "
        f"Accuracy: {train_acc.result() * 100}, "
        f"Test Loss: {test_loss.result()}, "
        f"Test Accuracy: {test_acc.result() * 100}"
    )
