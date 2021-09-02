"""提供对 TOS 储存的上传、下载、删除、查询功能"""
import math
import os
from logging import debug
from logging import error
from logging import warning
from multiprocessing.dummy import Pool
from multiprocessing.dummy import Process
from multiprocessing.dummy import Queue
from typing import List
from urllib.parse import urlparse

import boto3
import botocore
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from tqdm import tqdm

import volcengine_ml_platform


class TOSClient:
    """自动配置环境变量中的用户信息，与TOS 进行交互"""

    def __init__(self):
        """设置认证信息，初始化类变量"""

        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        credentials = volcengine_ml_platform.get_credentials()
        self.region_name = credentials.region
        self.s3_client = boto3.client(
            "s3",
            region_name=credentials.region,
            aws_access_key_id=credentials.ak,
            aws_secret_access_key=credentials.sk,
            endpoint_url=volcengine_ml_platform.get_tos_endpoint_url(),
        )
        self.dir_record = set()

    def bucket_exists(self, bucket_name):
        """查询用户的 bucket 是否存在

        Args:
            bucket_name(str): 用户创建bucket 对应的桶名

        Returns:
            返回一个 Bool 变量，代表桶是否存在

        Raises:
            ClientError: 创建时发生错误

        """
        """Check whether a bucket exists."""

        exists = True
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                exists = False
        return exists

    def create_bucket(self, bucket_name, region=""):
        """创建一个 bucket

        Args:
            bucket_name(str): 桶名
            region(str): 制定创建桶所在的地域

        Returns:
            返回 bool，表示创建是否成功

        Raises:
            ClientError: 创建时发生错误

        """

        """Create an S3 bucket in a specified region

        param bucket_name: Bucket to create
        param region: String region to create bucket in,
        return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region not in ("", self.region_name):
                location = {"LocationConstraint": region}
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location,
                )
            else:
                self.s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            error(e)
            return False
        return True

    def delete_bucket(self, bucket):
        """删除桶

        Args:
            bucket(str): 创建时的桶名

        Returns:
            返回一个 bool ，表示删除是否成功

        Raises:
            ClientError: 删除发生错误

        """

        """Delete a bucket, an error will be raised if it is not empty"""
        try:
            _ = self.s3_client.delete_bucket(Bucket=bucket)
            return True
        except ClientError as e:
            error(e)
            return False

    def list_buckets(self) -> list:
        """列出用户的所有桶

        Returns:
            返回一个 ``list[str]`` , 每个元素都是一个桶名。

        """

        """List S3 buckets

        return a list of Bucket infos
        Example: [{'Name': 'test', 'CreationDate':
        datetime.datetime(2021, 3, 19, 6, 37, 40, tzinfo=tzutc())}]
        """
        return self.s3_client.list_buckets()["Buckets"]

    def clear_bucket_objects(self, bucket):
        """删除桶的中所有内容

        Args:
            bucket(str): 创建时的桶名

        """

        """Delete all of object in the bucket"""
        while True:
            object_info = self.list_objects(
                bucket=bucket,
                encoding_type="url",
                delimiter=",",
                marker="",
                max_keys=1000,
                prefix="",
            )

            if (
                object_info is None
                or "Contents" not in object_info
                or len(
                    object_info["Contents"],
                )
                == 0
            ):
                break
            for item in object_info["Contents"]:
                key = item["Key"]
                self.s3_client.delete_object(
                    Bucket=bucket,
                    Key=key,
                )

    def delete_object(self, bucket, key):
        """删除桶的对象，或者说文件

        Args:
            bucket(str): 创建时的桶名
            key(str): 上传对象的 key

        """

        """Delete S3 objects with"""
        return self.s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )

    def list_objects(
        self,
        bucket,
        max_keys,
        marker="",
        delimiter="",
        encoding_type="url",
        prefix="",
    ):
        """列出桶里的对象, 最多一次列出 1000 个

        Args:
            bucket(str): 创建时的桶名
            delimiter(str): 分组 key 的 一个字符
            encoding_type(str): key 的编码形式，比如 encoding_type = "uft-8" 或者 "url"
            marker(str): 设置 key 的遍历起点，可用于大量对象的分段查询
            max_keys(int): 返回 key 数量上限
            prefix(str): 限制返回对象的 key 前缀

        Returns:
            返回一个 dict 对象，包含返回对象
            比如：::

                {
                    'IsTruncated': True|False,
                    'Marker': 'string',
                    'NextMarker': 'string',
                    'Contents': [
                        {
                            'Key': 'string',
                            'LastModified': datetime(2015, 1, 1),
                            'ETag': 'string',
                            'Size': 123,
                            'StorageClass': 'STANDARD'|'REDUCED_REDUNDANCY'|'GLACIER'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'DEEP_ARCHIVE'|'OUTPOSTS',
                            'Owner': {
                                'DisplayName': 'string',
                                'ID': 'string'
                            }
                        },
                    ],
                    'Name': 'string',
                    'Prefix': 'string',
                    'Delimiter': 'string',
                    'MaxKeys': 123,
                    'CommonPrefixes': [
                        {
                            'Prefix': 'string'
                        },
                    ],
                    'EncodingType': 'url'
                }

        """

        """List S3 objects with given object

            return a list of Object infos
        """
        return self.s3_client.list_objects(
            Bucket=bucket,
            Delimiter=delimiter,
            EncodingType=encoding_type,
            Marker=marker,
            MaxKeys=max_keys,
            Prefix=prefix,
        )

    def put_object(self, bucket, key, body):
        """上传对象到 bucket

        大小不应该超过 5MB；更推荐用 ``upload_file``

        Args:
            bucket(str): 上传 bucket 的名
            key(str): 上传 object 的 key，比如 key=``put/you/path/xxxx/yyy``
            body(str): file-like object, 比如 ``with open(flie, "rb") as f``

        Returns:
            返回一个上传结果的 dict

        """
        """Upload single object, object size should not exceed 5MB"""
        return self.s3_client.put_object(Bucket=bucket, Key=key, Body=body)

    def get_object(self, bucket, key):
        """获取 bucket 一个对象

        Args:
            bucket(str):  bucket 名
            key(str):  对应 object 的 key

        Returns:
            返回一个下载结果的 dict

        """
        """Download single object"""
        return self.s3_client.get_object(Bucket=bucket, Key=key)["Body"]

    def upload_file_low_level(
        self,
        file_path,
        bucket,
        key=None,
        part_size=20971520,
    ):
        """相比 upload_file，更精细化的上传文件方式

        Args:
            file_path(str): 上传文件的路径
            bucket(str): 上传 bucket 名
            key(str): 上传 object 的 key
            part_size(str): 切片上传的 size

        """
        """Implemented with low level S3 API, edit for desired info"""
        file_size = os.path.getsize(file_path)
        threshold = 5242880
        # if the key is not set, use file_path instead
        if key is None:
            key = file_path
        # if file size <= 25MB, upload single file
        if file_size <= part_size + threshold:
            with open(file_path, mode="rb", encoding="utf-8") as file:
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
            rsp = self.s3_client.create_multipart_upload(
                Bucket=bucket,
                Key=key,
            )
            debug("Multipart upload initiated: %s", rsp)

            upload_id = rsp["UploadId"]
            uploaded_parts = {"Parts": []}
            with open(file_path, mode="rb", encoding="utf-8") as file:
                # upload parts
                for i in range(1, part_number + 1):
                    read_size = min(part_size, file_size - (i - 1) * part_size)
                    read_size = max(-1, read_size)
                    body = file.read(read_size)  # 20MiB
                    if body == b"":
                        break
                    rsp = self.s3_client.upload_part(
                        Bucket=bucket,
                        Key=key,
                        PartNumber=i,
                        UploadId=upload_id,
                        Body=body,
                    )

                    uploaded_parts["Parts"].append(
                        {
                            "PartNumber": i,
                            "ETag": rsp["ETag"],
                        },
                    )
            # upload complete
            rsp = self.s3_client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload=uploaded_parts,
            )
            debug("Multipart upload completed: %s", rsp)

    def upload_file(self, file_path, bucket, key=None, part_size=20971520):
        """上传文件到 bucket

        Args:
            file_path(str): 上传文件的路径
            bucket(str): 上传 bucket 名
            key(str): 上传 object 的 key，比如 key="put/you/path/xxxx/yyy"
            part_size(str): 切片上传的 size

        """
        if key is None:
            key = file_path
        # Set the desired multipart threshold value (20MB)
        transfer_config = TransferConfig(multipart_threshold=part_size)

        # Perform the transfer
        self.s3_client.upload_file(
            file_path,
            bucket,
            key,
            Config=transfer_config,
        )

    def download_file(
        self,
        bucket: str = "",
        key: str = "",
        file_path: str = "",
        dir_path: str = "",
        tos_url: str = "",
        max_concurrence: int = 10,
        que: Queue = None,
    ) -> str:
        """从 bucket 下载对象

        推荐两种使用方式：
        - 通过 ``bucket + key`` 下载：::

            download_file(bucket="xxx", key="xxx",
                            file_path="./dataset/a.csv")

        - 通过 ``tos_url`` 下载：::

            download_file(tos_url="tos://bucket.[xxxxx]/key",
                            dir_path="./input/your/target/dir")


            其中，``dir_path`` 和 ``file_path`` 可以互换。

        Args:
            bucket(str): bucket 名
            key(str): object 的 key，比如 key=``put/you/path/xxxx/yyy``
            file_path(str): 下载文件的路径
            dir_path(str): 下载文件的目
            tos_url(str): 对象的 tos 链接
            max_concurrence(int): 最大并发数量，控制下载速度

        Returns:
            返回下载文件路径

        Raises:
            ValueError: 参数填写错误

        """
        """download dataset by bucket
        You call the function as follow:
            download_file(bucket="xxx", key="xxx", file_path="./dataset/a.csv"), or
            download_file(tos_url="tos://bucket.[xxxxx]/key", dir_path="./input/your/target/dir").

        1. you must pass file_path or dir_path as target file or target folder.
        2. you can only download object by a tos-url, or a key in the bucket

        param bucket: bucket name
        param keys: list keys of objects which will be deleted in the same bucket
        param file_path: the mapped file path of downloaded objects
        param dir_path: if file_paths is None, the object will download into dir_path
        param tos_url: if bucket or keys is none, urls will be used for downloaded
        param parallelism: the number threads which download files.
        return: the download filepath
        """

        # To consume less downstream bandwidth, decrease the maximum concurrency
        transfer_config = TransferConfig(max_concurrency=max_concurrence)

        if (not bucket or not key) and not tos_url:
            raise ValueError("Please assign a set of value as non-None")

        if not file_path and not dir_path:
            raise ValueError("Please set a correct dir_path or file_path")

        if tos_url:
            parse_result = urlparse(tos_url)
            if parse_result.scheme != "tos":
                raise ValueError("invalid scheme. url: " + tos_url)
            bucket = parse_result.netloc.split(".")[0]
            key = parse_result.path[1:]

            if not file_path:
                file_path = os.path.join(dir_path, key)
                dir_path = os.path.dirname(file_path)
            self._create_dir(dir_path)

        debug("download file: bucket %s, key %s", bucket, key)
        # Download an S3 object
        self.s3_client.download_file(
            bucket,
            key,
            file_path,
            Config=transfer_config,
        )

        if que:
            que.put(file_path)
        return file_path

    def _create_dir(self, dir_path):
        """创建路径缓冲

            可不用，用于频繁下载时的，减少系统调用开销
        Args:
            dir_path(str): 下载路径
        """
        if dir_path not in self.dir_record:
            self.dir_record.add(dir_path)
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError:
                warning("Cannot create download directory: %s", dir_path)
        return dir_path

    def download_files(
        self,
        bucket: str = "",
        keys: list = [],
        file_paths: list = [],
        dir_path: str = "",
        tos_urls: List[str] = [],
        parallelism=1,
    ) -> List[str]:
        """并行下载 objects

        推荐两种使用方式：
        - 通过 ``bucket + key`` 下载：::

            download_files(bucket="xxx",
                            keys=["xxx","yyy"],
                            file_paths=["./dataset/a.csv",
                                        "./dataset/b.csv"])


        - 通过 ``tos_url`` 下载：::

            download_files(tos_url=["tos://bucket.[xxxxx]/key", ....],
                            dir_path="./input/your/target/dir")


            其中， ``dir_path`` 和 ``file_path`` **不** 可以互换。

        Args:
            bucket(str): bucket 名
            key(str): object 的 key，比如 key="put/you/path/xxxx/yyy"
            file_paths(str): 下载多个文件对应的路径
            dir_path(str): 下载文件的目
            tos_urls(str): 对象的 tos 链接集合
            parallelism(int): 并发数量，控制下载速度

        Returns:
            返回下载文件集路径的 list

        Raises:
            ValueError: 参数填写错误

        """
        """download files by parallelism
        You only can call the function as follow:
           1. download_files(bucket="xxx", keys=["xxx","yyy"], file_paths=["./dataset/a.csv", "./dataset/b.csv"]),
           2. download_files(tos_url="tos://bucket.[xxxxx]/key", dir_path="./input/your/target/dir").
        In the first way, you must generation a file list, which is mapped by keys.

        param bucket: bucket name
        param keys: list keys of objects which will be deleted in the same bucket
        param file_paths: the mapped file paths of downloaded objects
        param dir_paths: if file_paths is None, objects will download into dir_path
        param urls: if bucket or keys is none, urls will be used for downloaded
        param parallelism: the number threads which download files.
        return: the list of download filepaths
        """

        if (not bucket or not keys) and not tos_urls:
            raise ValueError("Please assign a set of value as non-None")

        if not tos_urls and not dir_path:
            raise ValueError("Please set a correct dir_path or file_path")

        self.dir_record = set()
        que: Queue = Queue()
        async_res = []

        pool = Pool(processes=parallelism)
        data_count = 0
        if tos_urls:
            data_count = len(tos_urls)
            for url in tos_urls:
                async_res.append(
                    pool.apply_async(
                        self.download_file,
                        kwds={
                            "tos_url": url,
                            "dir_path": dir_path,
                            "que": que,
                        },
                    ),
                )
        elif bucket and keys:
            data_count = len(keys)
            for file_path, key in zip(file_paths, keys):
                async_res.append(
                    pool.apply_async(
                        self.download_file,
                        kwds={
                            "bucket": bucket,
                            "key": key,
                            "file_path": file_path,
                            "que": que,
                        },
                    ),
                )
        else:
            raise ValueError("Please set correct urls or (buckets + keys)")

        counter = Process(target=self._download_counter, args=(data_count, que))
        counter.start()

        pool.close()
        pool.join()
        counter.join()
        return [res.get() for res in async_res]

    def _download_counter(self, times, q):
        """下载进度提示

            请勿调用
        Args:
            times(int): 下载总量
            q(queue): 下载成功消息队列

        """
        with tqdm(total=times) as pbar:
            for _ in range(times):
                q.get()
                pbar.update(1)
