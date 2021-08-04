# Modified from https://github.com/pytorch/examples/blob/master/mnist/main.py
from __future__ import print_function
import time
from PIL import Image
import torch
# pylint: disable=consider-using-from-import
from torchvision import transforms

from ml_platform_sdk.config import credential as auth_credential
from ml_platform_sdk.datasets.image_dataset import ImageDataset

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-beijing'
tos_source = "tos://mnist-demo-do-not-delete/resnet_training_set.manifest"


def main():
    seed = 100
    batch_size = 64
    interval = 10
    torch.manual_seed(seed)

    train_kwargs = {
        'batch_size': batch_size,
        'num_workers': 32,
        'shuffle': True
    }

    image_transform = transforms.Compose([
        transforms.RandomResizedCrop(220, interpolation=Image.BILINEAR),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])

    def transform(data_):
        image = image_transform(data_)
        return image

    def target_transform(target):
        target = int(target['Result'][0]["Data"][0]["Label"])
        return target

    crdt = auth_credential.Credential(ak=ak, sk=sk, region=region)
    train_dataset = ImageDataset(
        credential=crdt,
        tos_source=tos_source,
        local_path="./demo_train_manifest",
    )
    train_dataset = train_dataset.init_torch_dataset(
        transform=transform,
        target_transform=target_transform,
    )

    train_loader = torch.utils.data.DataLoader(train_dataset, **train_kwargs)

    start = time.time()
    for idx, data in enumerate(train_loader):
        if idx > 0 and idx % interval == 0:
            print(f"speed: {interval * batch_size / (time.time() - start)}")
            start = time.time()


if __name__ == '__main__':
    main()
