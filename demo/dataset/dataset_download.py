import logging
from volcengine_ml_platform.datasets.text_dataset import TextDataset
from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.datasets.tabular_dataset import TabularDataset
from volcengine_ml_platform.datasets.video_dataset import VideoDataset

# upload dataset with 2100000050 account_id
# export env vars as follow:

#  export VOLC_ACCESSKEY="AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE"
#  export VOLC_SECRETKEY="WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=="
#  export VOLC_REGION="cn-north-1"
#  export VOLC_ML_PLATFORM_ENV="BOE"            # optional

middle_image_dataset = "d-20210818140750-gwbgc"
small_image_dataset = 'd-20210805035905-gp822'


def test_image_dataset(local_path='./demo/demo_dataset_image',
                       dataset_id=small_image_dataset):
    dataset = ImageDataset(dataset_id=dataset_id)

    dataset.download(local_path=local_path)

    dataset.split(training_dir=local_path + '/train',
                  testing_dir=local_path + '/test',
                  ratio=0.5)


def test_text_dataset(local_path='./demo/demo_dataset_text'):
    dataset = TextDataset(dataset_id='d-20210803143139-bgglt')

    dataset.download(local_path=local_path)

    dataset.split(training_dir=local_path + '/train',
                  testing_dir=local_path + '/test',
                  ratio=0.5)


def test_tabular_dataset(local_path='./demo/demo_dataset_tabular'):
    dataset = TabularDataset(dataset_id='d-20210718161642-d99kb')

    dataset.download(local_path=local_path)

    dataset.split(training_dir=local_path + '/train',
                  testing_dir=local_path + '/test',
                  ratio=0.5)


def test_video_dataset(local_path='./demo/demo_dataset_video'):
    dataset = VideoDataset(dataset_id='d-20210713212148-297zj'
                          )  #to upload dataset in  2100000050 account_id

    dataset.download(local_path=local_path)

    dataset.split(training_dir=local_path + '/train',
                  testing_dir=local_path + '/test',
                  ratio=0.5)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    test_image_dataset(dataset_id=middle_image_dataset)
    # test_video_dataset()
    # test_text_dataset()
    # test_tabular_dataset()
