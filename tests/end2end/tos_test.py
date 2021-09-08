import logging
import os
import random
import re
import string
import time
from pathlib import Path

from volcengine_ml_platform.io.tos import TOSClient

test_upload_number = 10
benchmark_upload_number = 50000
bucket_prefix = "ml-platform-test-tos-"


def inner_dataset_download(
    tmp_path,
    tos_cli: TOSClient,
    bucket,
    keys,
    checkout_file_number: int,
):

    # testes for download_file
    assert len(keys) >= 4
    tos_cli.download_file(bucket, keys[0], target_dir_path=tmp_path)

    filepath1 = os.path.join(tmp_path, "notOrigin1.png")
    tos_cli.download_file(bucket, keys[1], target_file_path=filepath1)

    url = "tos://" + bucket + "/" + keys[2]
    tos_cli.download_file(tos_url=url, target_dir_path=tmp_path)

    filepath2 = os.path.join(tmp_path, "notOrigin2.png")
    tos_cli.download_file(tos_url=url, target_file_path=filepath2)

    assert len(os.listdir(tmp_path)) == 4

    # testes for download_files
    new_dir1 = os.path.join(tmp_path, "dirdownload1")
    tos_cli.download_files(bucket=bucket, keys=keys, target_dir_path=new_dir1)
    assert len(os.listdir(new_dir1)) == checkout_file_number

    new_dir2 = os.path.join(tmp_path, "dirdownload2")
    tos_cli.download_files(
        bucket=bucket,
        keys=keys,
        target_file_paths=[os.path.join(new_dir2, filename) for filename in keys],
    )
    assert len(os.listdir(new_dir2)) == checkout_file_number

    new_dir3 = os.path.join(tmp_path, "dirdownload3")
    tos_cli.download_files(
        tos_urls=["tos://" + bucket + "/" + key for key in keys],
        target_file_paths=[os.path.join(new_dir3, filename) for filename in keys],
    )
    assert len(os.listdir(new_dir3)) == checkout_file_number

    new_dir4 = os.path.join(tmp_path, "dirdownload4")
    tos_cli.download_files(
        tos_urls=["tos://" + bucket + "/" + key for key in keys],
        target_dir_path=new_dir4,
    )
    assert len(os.listdir(new_dir4)) == checkout_file_number


# pass test data path and dataset type to generate general test procedure
def test_dataset_download(
    tmp_path,
    data_path="./tests/testdata/origin.jpg",
    upload_file_number: int = 5,
    checkout_file_number: int = 5,
):

    bucket = bucket_prefix + genRandonString(20)
    file = Path(data_path)

    # upload resource
    tos_cli = TOSClient()
    if not tos_cli.bucket_exists(bucket):
        tos_cli.create_bucket(bucket)
    time.sleep(4)  # wait 3 seconds as server need time to create a bucket
    assert tos_cli.bucket_exists(bucket)

    keys = []
    for i in range(upload_file_number):
        key = f"origin{i}.jpg"
        tos_cli.upload_file(str(file), bucket, key)
        keys.append(key)
    # url = "tos://" + bucket

    inner_dataset_download(tmp_path, tos_cli, bucket, keys, checkout_file_number)

    # delete resource
    for t in range(3):
        try:
            clean_buckets()
            break
        except BaseException as e:
            print("Err:", e)
            continue
        finally:
            print("try %d times", t + 1)


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
    test_dataset_download(
        tmp_path="./testdata",
        upload_file_number=6,
        checkout_file_number=6,
    )
