import logging
import math
import os
from typing import Optional

import boto3
import botocore
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from ml_platform_sdk import initializer
from ml_platform_sdk.config import credential as auth_credential, constants


def _init_boto3_client(credential: Optional[auth_credential.Credential] = None):
    # custom config
    # pylint: disable=C0301
    # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    if credential is None:
        credential = initializer.global_config.get_credential()

    # client = boto3.client(
    #     's3',
    #     region_name=credential.get_region(),
    #     endpoint_url=constants.TOS_REGION_ENDPOINT_URL[credential.get_region()],
    #     aws_access_key_id=credential.get_access_key_id(),
    #     aws_secret_access_key=credential.get_secret_access_key())

    # TODO: tos doesn't have boe env
    client = boto3.client(
        's3',
        region_name=credential.get_region(),
        endpoint_url=constants.TOS_REGION_ENDPOINT_URL[credential.get_region()],
        aws_access_key_id='AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q',
        aws_secret_access_key=
        'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ==')
    return client


class TOSClient:

    def __init__(self, credential: auth_credential.Credential):
        self.s3_client = _init_boto3_client(credential)

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

    def list_objects(self,
                     bucket,
                     delimiter=None,
                     encoding_type=None,
                     marker=None,
                     max_keys=None,
                     prefix=None):
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
        transfer_config = TransferConfig(multipart_threshold=part_size)

        # Perform the transfer
        self.s3_client.upload_file(file_path,
                                   bucket,
                                   key,
                                   Config=transfer_config)

    def download_file(self, file_path, bucket, key, max_concurrence=10):
        # To consume less downstream bandwidth, decrease the maximum concurrency
        transfer_config = TransferConfig(max_concurrency=max_concurrence)

        # Download an S3 object
        self.s3_client.download_file(bucket,
                                     key,
                                     file_path,
                                     Config=transfer_config)
