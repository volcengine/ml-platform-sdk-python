from ml_platform_sdk.datasets.image_dataset import ImageDataset
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-qingdao'

if __name__ == '__main__':
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))
    dataset = ImageDataset(dataset_id='d-20210713202131-ps49q')

    dataset.create(local_path='./demo_dataset')

    dataset.split(training_dir='./demo_dataset/train',
                  testing_dir='./demo_dataset/test',
                  ratio=0.5)
