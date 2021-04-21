import logging
import boto3
from s3_config import region_name, aws_access_key_id, aws_secret_access_key, endpoint_url
from botocore.exceptions import ClientError
from botocore.config import Config


class TOSClient:

    def __init__(self):
        self.s3_client = self._init_boto3_client()

    def _init_boto3_client(self):
        # custom config
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        client = boto3.client(
            's3',
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,)
        return client


    def create_bucket(bucket_name, region):
        """Create an S3 bucket in a specified region

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in,
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            s3_client = boto3.client('s3', region_name= "<tosRegionName>", 
                                    endpoint_url="<tosDomainName>",
                                    aws_access_key_id="<yourAccessKey>",
                                    aws_secret_access_key="<yourSecretKey>", )
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def delete_bucket(self, bucket_name):
        """Delete a bucket, an error will be raised if it is not empty"""
        try:
            response = s3.delete_bucket(Bucket="examplebucket")
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def list_buckets(self) -> list:
        """List S3 buckets

        return a list of Bucket infos
        Example: [{'Name': 'test', 'CreationDate': datetime.datetime(2021, 3, 19, 6, 37, 40, tzinfo=tzutc())}]
        """
        return self.s3_client.list_buckets()['Buckets']

    def list_objects(self, bucket) -> list:
        """List S3 objects

        return a list of Object infos
        """
        return self.s3_client.list_objects(Bucket=bucket)['Contents']

    def put_object(self, bucket, key, body):
        """Upload single object, object size should not exceed 5MB"""
        return self.s3_client.put_object(Bucket=bucket, Key=key, Body=body)

    def get_object(self, bucket, key):
        """Download single object"""
        return self.s3_client.get_object(Bucket=bucket, Key=key)['Body']



