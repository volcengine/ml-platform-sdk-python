"""提供对 TOS 储存的上传、下载、删除、查询功能"""
import math
import os
from logging import debug
from logging import error
from logging import warning
from multiprocessing.dummy import Pool
from typing import List
from urllib.parse import urlparse

import boto3
import botocore
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from tqdm import tqdm

import volcengine_ml_platform


class TOSClient:
    """自动配置环境变量中的用户信息，与TOS 进行交互"""

    def __init__(self, credentials=None, session_token=None):
        """设置认证信息，初始化类变量"""

        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        if credentials is None:
            credentials = volcengine_ml_platform.get_credentials()
        self.region_name = credentials.region
        config = {
            "region_name": credentials.region,
            "aws_access_key_id": credentials.ak,
            "aws_secret_access_key": credentials.sk,
            "endpoint_url": volcengine_ml_platform.get_tos_endpoint_url(),
        }
        if session_token is None:
            session_token = volcengine_ml_platform.get_session_token()
        if session_token is not None and len(session_token.strip()) > 0:
            config["aws_session_token"] = session_token
        self.s3_client = boto3.client("s3", config=Config(
            s3={'addressing_style': 'virtual'}), **config)
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

            if (object_info is None or "Contents" not in object_info or len(object_info["Contents"],) == 0):
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

                    uploaded_parts["Parts"].append({
                        "PartNumber": i,
                        "ETag": rsp["ETag"],
                    },)
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
        tos_url: str = "",
        target_file_path: str = "",
        target_dir_path: str = "",
        max_concurrence: int = 10,
    ) -> str:
        """下载TOS对象到本地

        要下载对象的目标地址，两种方式选择其一：
        - 通过 ``bucket + key`` 下载：::

            download_file(bucket="xxx", key="xxx", ...)

        - 通过 ``tos_url`` 下载：::

            download_file(tos_url="tos://bucket.[xxxxx]/key", ...)


        下载的文件保存到本地目标路径有两种方式： target_file_path 或

        - 通过 ``target_file_path`` 指定

        - 通过 ``target_dir_path`` 指定，实际保存的文件名为key 或者 tos_url.substringAfterLast("/")

        Args:
            bucket(str): bucket 名
            key(str): object 的 key，比如 key=``put/you/path/xxxx/yyy``
            tos_url(str): 对象的 tos 链接
            file_path(str): 本地保存的目标文件路径
            dir_path(str): 本地保存的目标目录路径
            max_concurrence(int): 最大并发数量，控制下载速度
        Returns:
            返回下载文件路径

        Raises:
            ValueError: 参数填写错误

        """

        # To consume less downstream bandwidth, decrease the maximum concurrency
        transfer_config = TransferConfig(max_concurrency=max_concurrence)

        if (not bucket or not key) and not tos_url:
            raise ValueError("Please assign a set of value as non-None")

        if not target_file_path and not target_dir_path:
            raise ValueError("Please set a correct dir_path or file_path")

        if tos_url:
            parse_result = urlparse(tos_url)
            if parse_result.scheme != "tos":
                raise ValueError("invalid scheme. url: " + tos_url)
            bucket = parse_result.netloc.split(".")[0]
            key = parse_result.path[1:]

        if not target_file_path:
            target_file_path = os.path.join(target_dir_path, key)
        else:
            target_dir_path = os.path.dirname(target_file_path)
        self._create_dir(os.path.dirname(target_file_path))

        debug("download file: bucket %s, key %s", bucket, key)
        self.s3_client.download_file(
            bucket,
            key,
            target_file_path,
            Config=transfer_config,
        )
        return target_file_path

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
        tos_urls: list = [],
        target_file_paths: list = [],
        target_dir_path: str = "",
        parallelism=1,
    ) -> List[str]:
        """下载多个TOS对象到本地

        要下载的源文件有两种指定方式：
        - 通过 ``bucket + keys`` 指定：::

            download_files(bucket="your_bucket_name", keys=["xxx","yyy", ...], ...)


        - 通过 ``tos_urls`` 指定：::

            download_files(tos_urls=["tos://you_bucket_name]/xxx", "tos://you_bucket_name]/yyy", ....], ...)


        下载的文件保存到本地目标路径有两种方式：

        - 通过 `target_file_paths`` 指定，需要和要下载的源对象列表长度一致

        - 通过 ``target_dir_path`` 指定，所有文件保存到该目录下，，实际保存的文件名为对应的key 或者 对应的tos_url.substringAfterLast("/")

        Args:
            bucket(str): bucket 名
            keys(list): object 的 key，比如 key="put/you/path/xxxx/yyy"
            tos_urls(list): 对象的 tos 链接集合
            target_file_paths(list): 本地保存的目标路径的列表，与 keys 或者 tos_urls 一一对应
            target_dir_path(str): 本地保存的目标目录
            parallelism(int): 并发数量，控制下载速度

        Returns:
            返回下载文件集路径的 list

        Raises:
            ValueError: 参数填写错误

        """

        if (not bucket or not keys) and not tos_urls:
            raise ValueError("Please assign a set of value as non-None")

        if not target_file_paths and not target_dir_path:
            raise ValueError("Please set a correct dir_path or file_path")

        self.dir_record = set()
        async_res = []

        pool = Pool(processes=parallelism)

        data_count = len(keys) if keys else len(tos_urls)
        download_dicts: list = [{} for _ in range(data_count)]

        if tos_urls:
            for idx, url in enumerate(tos_urls):
                download_dicts[idx]["tos_url"] = url
        else:
            for idx, key in enumerate(keys):
                download_dicts[idx]["bucket"] = bucket
                download_dicts[idx]["key"] = key

        if target_dir_path:
            for dict in download_dicts:
                dict["target_dir_path"] = target_dir_path
        else:
            for idx, target_file_path in enumerate(target_file_paths):
                download_dicts[idx]["target_file_path"] = target_file_path

        for idx in range(data_count):
            async_res.append(pool.apply_async(
                self.download_file,
                kwds=download_dicts[idx],
            ),)

        pool.close()
        ret = [res.get() for res in tqdm(async_res)]
        pool.join()
        return ret

    def download_dir(self, bucket, key, prefix, local_dir):
        marker = ""
        while True:
            res = self.s3_client.list_objects(
                Bucket=bucket,
                Delimiter="/",
                EncodingType="",
                Marker=marker,
                MaxKeys=1000,
                Prefix=key,
            )
            keys = [content["Key"] for content in res.get("Contents", list())]
            dirs = [content["Prefix"]
                    for content in res.get("CommonPrefixes", list())]

            for d in dirs:
                debug(f"processing dir: {d}")
                dest_pathname = os.path.join(
                    local_dir, os.path.relpath(d, prefix) + "/")
                debug(f"dest_pathname: {dest_pathname}")
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    debug(f"make dir: {dest_pathname}")
                self.download_dir(bucket, d, prefix, local_dir)

            for k in keys:
                debug(f"processing file: {k}")
                dest_pathname = os.path.join(
                    local_dir, os.path.relpath(k, prefix))
                debug(f"dest_pathname: {dest_pathname}")
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    debug(f"make dir: {dest_pathname}")

                if not os.path.isdir(dest_pathname):
                    self.s3_client.download_file(bucket, k, dest_pathname)

            if res["IsTruncated"]:
                marker = res["Contents"][-1]["Key"]
                continue
            break

    def upload(self, local_path, bucket, prefix):
        if os.path.isfile(local_path):
            key = f"{prefix}{os.path.basename(local_path)}"
            self.upload_file(local_path, bucket, key=key)

        if os.path.isdir(local_path):
            self_prefix = os.path.basename(local_path.rstrip("/"))
            if self_prefix != ".":
                prefix = f"{prefix}{self_prefix}/"

            for root, _, files in os.walk(local_path):
                for file in tqdm(files):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, local_path)
                    if rel_path == ".":
                        key = f"{prefix}{file}"
                    else:
                        key = f"{prefix}{rel_path}/{file}"
                    self.upload_file(file_path, bucket, key=key)
        return f"tos://{bucket}/{prefix}"
