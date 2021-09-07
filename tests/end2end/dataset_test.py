import logging
import os
import random
import re
import string
import time
from datetime import datetime
from pathlib import Path

from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.datasets.tabular_dataset import TabularDataset
from volcengine_ml_platform.io.tos import TOSClient
from volcengine_ml_platform.openapi.dataset_client import DataSetClient

test_upload_number = 10
benchmark_upload_number = 50000
bucket_prefix = "ml-platform-test-dataset-"


# pass test data path and dataset type to generate general test procedure
def inner_test_dataset_download(
    tmp_path,
    data_path,
    dataset_type,
    upload_file_number: int,
    checkout_file_number: int,
):
    clean_buckets()

    bucket = "ml-platform-test-dataset-" + genRandonString(20)
    file = Path(data_path)

    # upload resource
    tos_cli = TOSClient()
    if not tos_cli.bucket_exists(bucket):
        tos_cli.create_bucket(bucket)
    time.sleep(4)  # wait 3 seconds as server need time to create a bucket
    assert tos_cli.bucket_exists(bucket)

    for i in range(upload_file_number):
        tos_cli.upload_file(str(file), bucket, f"origin{i}.jpg")
    url = "tos://" + bucket

    # create a dataset
    api_cli = DataSetClient()
    dataset = "test-image-dataset-auto-" + genRandonString(5)
    if dataset_type is ImageDataset:
        request = {
            "Name": dataset,
            "DataType": "Image",
            "AnnotationTemplate": "ImageClassification",
            "GenerationMode": "Folder",
            "Description": "created by python sdk {}".format(
                datetime.now().strftime("%Y %H:%M:%S"),
            ),
            "SourcePath": url,
            "StorageType": "TOS",
        }
    elif dataset_type is TabularDataset:
        request = {
            "Name": dataset,
            "DataType": "Tabular",
            "AnnotationTemplate": "TimeSeriesPrediction",
            "GenerationMode": "File",
            "Description": "created by python sdk {}".format(
                datetime.now().strftime("%Y %H:%M:%S"),
            ),
            "SourcePath": url,
            "StorageType": "TOS",
        }
    else:
        raise BaseException("Invalid dataset type")

    resp = api_cli.create_dataset(body=request)
    dataset_id = resp["Result"]["DatasetID"]
    time.sleep(3)  # wait 3 seconds as ml-engine need time to create the dataset
    # download the dataset
    ds = dataset_type(dataset_id=dataset_id)
    ds.download(local_path=tmp_path)
    assert len(os.listdir(tmp_path)) == checkout_file_number

    # delete resource
    for t in range(3):
        try:
            clean_buckets()
            api_cli.delete_dataset(dataset_id)
            break
        except BaseException as e:
            print("Err:", e)
            continue
        finally:
            print("try %d times", t + 1)


def test_create_image_dataset(tmp_path):
    inner_test_dataset_download(
        tmp_path,
        data_path="./tests/testdata/origin.jpg",
        dataset_type=ImageDataset,
        upload_file_number=10,
        checkout_file_number=12,
    )


def test_create_tabular_dataset(tmp_path):
    inner_test_dataset_download(
        tmp_path,
        data_path="./tests/testdata/train.csv",
        dataset_type=TabularDataset,
        upload_file_number=1,
        checkout_file_number=1,
    )


def genRandonString(n):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(n))


def clean_buckets():
    tos_cli = TOSClient()
    buckets = tos_cli.list_buckets()
    for bucket in buckets:
        if re.match(bucket_prefix, bucket["Name"]):
            tos_cli.clear_bucket_objects(bucket["Name"])
            tos_cli.delete_bucket(bucket["Name"])
            logging.info("delete bucket %s", bucket["Name"])


if __name__ == "__main__":
    test_create_image_dataset("./testdata1")
    test_create_tabular_dataset("./testdata2")
