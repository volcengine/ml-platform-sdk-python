import logging
import os
import uuid
from datetime import datetime
from six.moves import urllib

from ml_platform_sdk.tos import tos
from ml_platform_sdk.model.model_service import ModelService


class ModelClient(object):

    def __init__(self, ak, sk, region):
        self.ak = sk
        self.sk = sk
        self.region = region
        self.api_client = ModelService(region)
        self.api_client.set_ak(ak)
        self.api_client.set_sk(sk)
        self.tos_client = tos.TOSClient(region, ak, sk)

    @staticmethod
    def _default_bucket():
        return "models"

    @staticmethod
    def _default_prefix(model_name):
        date = datetime.now().strftime("%y-%m-%d")
        random_id = str(uuid.uuid4())[:13]
        return "{}/{}/{}/".format(model_name, date, random_id)

    def _upload_to_tos(self, local_path, bucket, prefix):
        if not os.path.exists(local_path):
            logging.error("Local path {} not exists.".format(local_path))

        # upload file
        if os.path.isfile(local_path):
            key = prefix + os.path.basename(local_path)
            self.tos_client.upload_file(local_path, bucket, key=key)

        # upload a model directory
        if os.path.isdir(local_path):
            # refactor prefix
            # if local path is /a/b/c, raw prefix is d/e/f/, then
            # new prefix is d/e/f/c/
            prefix = prefix + os.path.basename(local_path.rstrip('/')) + '/'
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, local_path)
                    if rel_path == '.':
                        key = prefix + file
                    else:
                        key = prefix + rel_path + '/' + file
                    self.tos_client.upload_file(file_path, bucket, key=key)
                # Todo: for empty directory, put an empty object to tos

        tos_path = "tos://{}/{}".format(bucket, prefix)
        return tos_path

    def _get_or_create_bucket(self, bucket_name, region):
        if not bucket_name:
            bucket_name = self._default_bucket()
        exists = self.tos_client.bucket_exists(bucket_name)
        if not self.tos_client.bucket_exists(bucket_name):
            self.tos_client.create_bucket(bucket_name, region)
        return bucket_name

    def _get_or_generate_prefix(self, prefix, model_name):
        if not prefix:
            prefix = self._default_prefix(model_name)
        else:
            # make sure prefix endswith /
            if not prefix.endswith('/'):
                prefix += '/'
        return prefix

    def upload_model(self,
                     model_name,
                     model_format,
                     model_type,
                     local_path,
                     description=None,
                     bucket_name=None,
                     prefix=None,
                     create_new_model=False):
        bucket_name = self._get_or_create_bucket(bucket_name, self.region)
        prefix = self._get_or_generate_prefix(prefix, model_name)
        tos_path = self._upload_to_tos(local_path, bucket_name, prefix)

        print(">>>tos_path:{}".format(tos_path))
        return self.api_client.create_model(
            model_name=model_name,
            model_format=model_format,
            model_type=model_type,
            path=tos_path,
            description=description,
            create_new_model=create_new_model,
        )

    def _download_dir(self, bucket, key, prefix, local_dir):
        marker = ''
        while True:
            res = self.tos_client.s3_client.list_objects(Bucket=bucket,
                                                         Delimiter="/",
                                                         EncodingType="",
                                                         Marker=marker,
                                                         MaxKeys=1000,
                                                         Prefix=key)
            keys = [content["Key"] for content in res.get("Contents", list())]
            dirs = [
                content["Prefix"]
                for content in res.get("CommonPrefixes", list())
            ]

            for d in dirs:
                print("processing dir: {}".format(d), flush=True)
                dest_pathname = os.path.join(local_dir,
                                             os.path.relpath(d, prefix) + '/')
                print("dest_pathname: {}".format(dest_pathname))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    print("make dir: {}".format(dest_pathname))
                self._download_dir(bucket, d, prefix, local_dir)

            for k in keys:
                print("processing file: {}".format(k), flush=True)
                dest_pathname = os.path.join(local_dir,
                                             os.path.relpath(k, prefix))
                print("dest_pathname: {}".format(dest_pathname))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    print("make dir: {}".format(dest_pathname))

                if not os.path.isdir(dest_pathname):
                    self.tos_client.s3_client.download_file(
                        bucket, k, dest_pathname)

            if res['IsTruncated']:
                marker = res['Contents'][-1]['Key']
                continue
            break

    def download_model(self, model_version_id, local_dir):
        resp = self.get_model_version(model_version_id=model_version_id)
        tos_path = resp["Result"]["Path"]
        parse_result = urllib.parse.urlparse(tos_path)
        bucket = parse_result.hostname
        key = parse_result.path.lstrip('/')

        self._download_dir(bucket, key, key, local_dir)
        return "Download model {} to {} success".format(model_version_id,
                                                        local_dir)

    def list_models(self,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend',
                    model_name_contains=None):
        return self.api_client.list_models(offset, page_size, sort_by,
                                           sort_order, model_name_contains)

    def delete_model(self, model_id):
        return self.api_client.delete_model(model_id)

    def list_model_versions(self, model_name=None, model_id=None):
        return self.api_client.list_model_versions(model_name, model_id)

    def get_model_version(self,
                          model_name=None,
                          model_version=None,
                          model_version_id=None):
        return self.api_client.get_model_version(model_name, model_version,
                                                 model_version_id)

    def delete_model_version(self,
                             model_name=None,
                             model_version=None,
                             model_version_id=None):
        return self.api_client.delete_model_version(model_name, model_version,
                                                    model_version_id)

    def update_model_version(self, model_version_id, description=None):
        return self.api_client.update_model_version(model_version_id,
                                                    description)
