import logging
import math
import os
import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from operator_sdk.base import env


class TOSClient:

    def __init__(self):
        self.s3_client = self._init_boto3_client()

    def _init_boto3_client(self):
        # custom config
        # pylint: disable=C0301
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        config = env.Config()
        client = boto3.client(
            's3',
            region_name=config.get_tos_region(),
            endpoint_url=config.get_tos_endpoint_url(),
            aws_access_key_id=config.get_access_key_id(),
            aws_secret_access_key=config.get_secret_access_key(),
        )
        return client

    def create_bucket(self, bucket_name, region):
        """Create an S3 bucket in a specified region

        param bucket_name: Bucket to create
        param region: String region to create bucket in,
        return: True if bucket created, else False
        """

        # Create bucket
        try:
            location = {'LocationConstraint': region}
            self.s3_client.create_bucket(Bucket=bucket_name,
                                         CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def delete_bucket(self, bucket):
        """Delete a bucket, an error will be raised if it is not empty"""
        try:
            response = self.s3_client.delete_bucket(Bucket=bucket)
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def list_buckets(self) -> list:
        """List S3 buckets

        return a list of Bucket infos
        Example: [{'Name': 'test', 'CreationDate':
        datetime.datetime(2021, 3, 19, 6, 37, 40, tzinfo=tzutc())}]
        """
        return self.s3_client.list_buckets()['Buckets']

    def list_objects(self, bucket) -> list:
        """List S3 objects with given object

        return a list of Object infos
        """
        return self.s3_client.list_objects(Bucket=bucket)

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
            with open(file_path, 'rb') as file:
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
            logging.debug('Multipart upload initiated: %s', rsp)

            upload_id = rsp["UploadId"]
            uploaded_parts = {'Parts': []}
            with open(file_path, 'rb') as file:
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
            logging.debug('Multipart upload completed: %s', rsp)

    def upload_file(self, file_path, bucket, key=None, part_size=20971520):
        if key is None:
            key = file_path
        # Set the desired multipart threshold value (20MB)
        config = TransferConfig(multipart_threshold=part_size)

        # Perform the transfer
        self.s3_client.upload_file(file_path, bucket, key, Config=config)

    def download_file(self, file_path, bucket, key, max_concurrence=10):
        # To consume less downstream bandwidth, decrease the maximum concurrency
        config = TransferConfig(max_concurrency=max_concurrence)

        # Download an S3 object
        self.s3_client.download_file(bucket, key, file_path, Config=config)
