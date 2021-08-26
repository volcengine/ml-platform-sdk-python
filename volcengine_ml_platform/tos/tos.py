import math
import os

from logging import warning, error, debug
from urllib.parse import urlparse
from multiprocessing.dummy import Pool, Process, Queue
from typing import Optional
from tqdm import tqdm

import boto3
import botocore
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
import volcengine_ml_platform


class TOSClient:

    def __init__(self):
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        credentials = volcengine_ml_platform.get_credentials()
        self.region_name = credentials.region
        self.s3_client = boto3.client(
            's3',
            region_name=credentials.region,
            aws_access_key_id=credentials.ak,
            aws_secret_access_key=credentials.sk,
            endpoint_url=volcengine_ml_platform.get_tos_endpoint_url())
        self.dir_record = set()

    def bucket_exists(self, bucket_name):
        """Check whether a bucket exists."""

        exists = True
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        return exists

    def create_bucket(self, bucket_name, region=""):
        """Create an S3 bucket in a specified region

        param bucket_name: Bucket to create
        param region: String region to create bucket in,
        return: True if bucket created, else False
        """

        # Create bucket
        try:
            # location = {'LocationConstraint': region}
            # self.s3_client.create_bucket(Bucket=bucket_name,
            #                              CreateBucketConfiguration=location)
            if region not in ("", self.region_name):
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration=location)
            else:
                self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            error(e)
            return False
        return True

    def delete_bucket(self, bucket):
        """Delete a bucket, an error will be raised if it is not empty"""
        try:
            response = self.s3_client.delete_bucket(Bucket=bucket)
            return True
        except ClientError as e:
            error(e)
            return False

    def list_buckets(self) -> list:
        """List S3 buckets

        return a list of Bucket infos
        Example: [{'Name': 'test', 'CreationDate':
        datetime.datetime(2021, 3, 19, 6, 37, 40, tzinfo=tzutc())}]
        """
        return self.s3_client.list_buckets()['Buckets']

    def clear_bucket_objects(self, bucket):
        """Delete all of object in the bucket
        """
        while True:
            object_info = self.list_objects(
                bucket=bucket,
                encoding_type='url',
                delimiter=',',
                marker='',
                max_keys=1000,
                prefix='',
            )

            if object_info is None or 'Contents' not in object_info or len(
                    object_info['Contents']) == 0:
                break
            for item in object_info['Contents']:
                key = item['Key']
                self.s3_client.delete_object(
                    Bucket=bucket,
                    Key=key,
                )

    def delete_object(self, bucket, key):
        """Delete S3 objects with"""
        return self.s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )

    def list_objects(self, bucket, delimiter, encoding_type, marker, max_keys,
                     prefix):
        """List S3 objects with given object

        return a list of Object infos
        """
        return self.s3_client.list_objects(Bucket=bucket,
                                           Delimiter=delimiter,
                                           EncodingType=encoding_type,
                                           Marker=marker,
                                           MaxKeys=max_keys,
                                           Prefix=prefix)

    def put_object(self, bucket, key, body):
        """Upload single object, object size should not exceed 5MB"""
        return self.s3_client.put_object(Bucket=bucket, Key=key, Body=body)

    def get_object(self, bucket, key):
        """Download single object"""
        return self.s3_client.get_object(Bucket=bucket, Key=key)['Body']

    def upload_file_low_level(self,
                              file_path,
                              bucket,
                              key=None,
                              part_size=20971520):
        """Implemented with low level S3 API, edit for desired info"""
        file_size = os.path.getsize(file_path)
        threshold = 5242880
        # if the key is not set, use file_path instead
        if key is None:
            key = file_path
        # if file size <= 25MB, upload single file
        if file_size <= part_size + threshold:
            with open(file_path, mode='rb', encoding='utf-8') as file:
                self.s3_client.upload_fileobj(file, bucket, key)
        # otherwise
        else:
            # if the last part is smaller than 5MB
            # combine it with previous part
            part_number = 0
            if file_size % part_size <= threshold:
                part_number = math.floor(float(file_size) % float(part_size))
            else:
                part_number = math.ceil(float(file_size) % float(part_size))

            # start multipart upload
            rsp = self.s3_client.create_multipart_upload(Bucket=bucket, Key=key)
            debug('Multipart upload initiated: %s', rsp)

            upload_id = rsp["UploadId"]
            uploaded_parts = {'Parts': []}
            with open(file_path, mode='rb', encoding='utf-8') as file:
                # upload parts
                for i in range(1, part_number + 1):
                    read_size = min(part_size, file_size - (i - 1) * part_size)
                    read_size = max(-1, read_size)
                    body = file.read(read_size)  # 20MiB
                    if body == b'':
                        break
                    rsp = self.s3_client.upload_part(Bucket=bucket,
                                                     Key=key,
                                                     PartNumber=i,
                                                     UploadId=upload_id,
                                                     Body=body)

                    uploaded_parts['Parts'].append({
                        'PartNumber': i,
                        'ETag': rsp['ETag']
                    })
            # upload complete
            rsp = self.s3_client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload=uploaded_parts)
            debug('Multipart upload completed: %s', rsp)

    def upload_file(self, file_path, bucket, key=None, part_size=20971520):
        if key is None:
            key = file_path
        # Set the desired multipart threshold value (20MB)
        transfer_config = TransferConfig(multipart_threshold=part_size)

        # Perform the transfer
        self.s3_client.upload_file(file_path,
                                   bucket,
                                   key,
                                   Config=transfer_config)

    def download_file(
        self,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        file_path: Optional[str] = None,
        dir_path: Optional[str] = None,
        tos_url: Optional[str] = None,
        max_concurrence=10,
        que=None,
    ):
        """download dataset by bucket
        You call the function as follow:
            download_file(bucket="xxx", key="xxx", file_path="./dataset/a.csv"), or
            download_file(tos_url="tos://bucket.[xxxxx]/key", dir_path="./input/your/target/dir").

        1. you must pass file_path or dir_path as target file or target folder.
        2. you can only download object by a tos-url, or a key in the bucket

        param bucket: bucket name
        param keys: list keys of objects which will be deleted in the same bucket
        param file_paths: the mapped file paths of downloaded objects
        param dir_paths: if file_paths is None, objects will download into dir_path
        param urls: if bucket or keys is none, urls will be used for downloaded
        param parallelism: the number threads which download files.
        return: the list of download filepaths
        """

        # To consume less downstream bandwidth, decrease the maximum concurrency
        transfer_config = TransferConfig(max_concurrency=max_concurrence)

        if tos_url is not None:
            parse_result = urlparse(tos_url)
            if parse_result.scheme != "tos":
                raise "invalid scheme. url: " + tos_url
            bucket = parse_result.netloc.split(".")[0]
            key = parse_result.path[1:]

            if file_path is None:
                file_path = os.path.join(dir_path, key)
            self._create_dir(dir_path)

        debug("download file: bucket %s, key %s", bucket, key)
        # Download an S3 object
        self.s3_client.download_file(bucket,
                                     key,
                                     file_path,
                                     Config=transfer_config)

        if que:
            que.put(file_path)
        return file_path

    def _create_dir(self, dir_path):
        if dir_path not in self.dir_record:
            self.dir_record.add(dir_path)
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError:
                warning('Cannot create download directory: %s', dir_path)
        return dir_path

    def download_files(self,
                       bucket: str = None,
                       keys: Optional[list] = None,
                       file_paths: Optional[list] = None,
                       dir_path: Optional[str] = None,
                       tos_urls: Optional[list] = None,
                       parallelism=1):
        """download files by parallelism
        You only can call the function as follow:
           1. download_file(bucket="xxx", keys=["xxx","yyy"], file_paths=["./dataset/a.csv", "./dataset/b.csv"]),
           2. download_file(tos_url="tos://bucket.[xxxxx]/key", dir_path="./input/your/target/dir").
        In the first way, you must generation a file list, which is mapped by keys.

        param bucket: bucket name
        param keys: list keys of objects which will be deleted in the same bucket
        param file_paths: the mapped file paths of downloaded objects
        param dir_paths: if file_paths is None, objects will download into dir_path
        param urls: if bucket or keys is none, urls will be used for downloaded
        param parallelism: the number threads which download files.
        return: the list of download filepaths
        """

        if file_paths is None and dir_path is None:
            raise ValueError("Please set a correct dir_path or file_path")

        self.dir_record = set()
        que = Queue()
        async_res = []

        pool = Pool(processes=parallelism)
        data_count = 0
        if bucket is None or keys is None:
            data_count = len(tos_urls)
            for url in tos_urls:
                async_res.append(
                    pool.apply_async(self.download_file,
                                     kwds={
                                         "tos_url": url,
                                         "dir_path": dir_path,
                                         "que": que
                                     }))
        elif tos_urls:
            data_count = len(keys)
            for file_path, key in zip(file_paths, keys):
                async_res.append(
                    pool.apply_async(self.download_file,
                                     kwds={
                                         "bucket": bucket,
                                         "key": key,
                                         "file_path": file_path,
                                         "que": que
                                     }))
        else:
            raise ValueError("Please set correct urls or (buckets + keys)")

        counter = Process(target=self.download_counter, args=(data_count, que))
        counter.start()

        pool.close()
        pool.join()
        counter.join()
        return [res.get() for res in async_res]

    def download_counter(self, times, q):
        with tqdm(total=times) as pbar:
            for _ in range(times):
                q.get()
                pbar.update(1)
