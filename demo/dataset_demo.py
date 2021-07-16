from ml_platform_sdk.datasets.text_dataset import TextDataset
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-qingdao'

if __name__ == '__main__':
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))
    dataset = TextDataset(dataset_id='d-20210715165619-s6x25')

    dataset.create(local_path='./demo_dataset')

    dataset.split(training_dir='./demo_dataset/train',
                  testing_dir='./demo_dataset/test',
                  ratio=0.5)
