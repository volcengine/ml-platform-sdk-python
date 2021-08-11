import logging
from volcengine_ml_platform.datasets.text_dataset import TextDataset
from volcengine_ml_platform.config import credential as auth_credential
import volcengine_ml_platform

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    volcengine_ml_platform.init(auth_credential.Credential(ak, sk, region))
    dataset = TextDataset(dataset_id='d-20210811115227-26fvx')

    dataset.create(local_path='./demo_dataset')

    dataset.split(training_dir='./demo_dataset/train',
                  testing_dir='./demo_dataset/test',
                  ratio=0.5)
