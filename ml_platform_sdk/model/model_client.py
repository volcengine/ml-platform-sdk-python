import logging
import os
import uuid
from datetime import datetime
from typing import List
from six.moves import urllib
from _typeshed import StrPath

from ml_platform_sdk.tos import tos
from ml_platform_sdk.model.model_service import ModelRepoService
from ml_platform_sdk.model.model import Model


class ModelClient:

    def __init__(self, ak, sk, region):
        self.ak = sk
        self.sk = sk
        self.region = region
        self.api_client = ModelRepoService(region)
        self.api_client.set_ak(ak)
        self.api_client.set_sk(sk)
        self.tos_client = tos.TOSClient(region, ak, sk)

    @staticmethod
    def _default_bucket():
        return 'models'

    @staticmethod
    def _default_prefix(model_name):
        date = datetime.now().strftime('%y-%m-%d')
        random_id = str(uuid.uuid4())[:13]
        return '{}/{}/{}/'.format(model_name, date, random_id)

    def _upload_to_tos(self, local_path, bucket, prefix):
        if not os.path.exists(local_path):
            logging.error('Local path %s not exists.', local_path)

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

        tos_path = 'tos://{}/{}'.format(bucket, prefix)
        return tos_path

    def _get_or_create_bucket(self, bucket_name, region):
        if not bucket_name:
            bucket_name = self._default_bucket()
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

    def _download_dir(self, bucket, key, prefix, local_dir):
        marker = ''
        while True:
            res = self.tos_client.s3_client.list_objects(Bucket=bucket,
                                                         Delimiter='/',
                                                         EncodingType='',
                                                         Marker=marker,
                                                         MaxKeys=1000,
                                                         Prefix=key)
            keys = [content['Key'] for content in res.get('Contents', list())]
            dirs = [
                content['Prefix']
                for content in res.get('CommonPrefixes', list())
            ]

            for d in dirs:
                print('processing dir: {}'.format(d), flush=True)
                dest_pathname = os.path.join(local_dir,
                                             os.path.relpath(d, prefix) + '/')
                print('dest_pathname: {}'.format(dest_pathname))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    print('make dir: {}'.format(dest_pathname))
                self._download_dir(bucket, d, prefix, local_dir)

            for k in keys:
                print('processing file: {}'.format(k), flush=True)
                dest_pathname = os.path.join(local_dir,
                                             os.path.relpath(k, prefix))
                print('dest_pathname: {}'.format(dest_pathname))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                    print('make dir: {}'.format(dest_pathname))

                if not os.path.isdir(dest_pathname):
                    self.tos_client.s3_client.download_file(
                        bucket, k, dest_pathname)

            if res['IsTruncated']:
                marker = res['Contents'][-1]['Key']
                continue
            break

    def download_model(self, model_id: str, model_version_id: str,
                       local_dir: StrPath):
        """download model with version

        Args:
            model_id (str): model id
            model_version_id (str): model version id, a model can have multiple versions
            local_dir (StrPath): local directory to store model

        Returns:
            json response
        """
        resp = self.get_model_version(model_id=model_id,
                                      model_version_id=model_version_id)
        tos_path = resp.version_info.path
        parse_result = urllib.parse.urlparse(tos_path)
        bucket = parse_result.hostname
        key = parse_result.path.lstrip('/')

        self._download_dir(bucket, key, key, local_dir)
        return 'Download model {} to {} success'.format(model_version_id,
                                                        local_dir)

    def upload_model(
        self,
        model_name: str,
        model_format: str,
        model_type: str,
        bucket_name: str,
        prefix: str,
        local_path: StrPath,
        model_id=None,
        description=None,
    ) -> tuple(str, str):
        """upload local model to TOS and register with model repository service

        Args:
            model_name (str): model name
            model_format (str): model format, can be one of SavedModel', 'GraphDef','TorchScript','PTX',
                    'CaffeModel','NetDef','MXNetParams','Scikit_Learn','XGBoost','TensorRT','ONNX',or 'Custom'
            model_type (str): The type of the ModelVersion, examples: 'TensorFlow:2.0'
            bucket_name (str): tos bucket
            prefix (str): prefix for tos keys
            local_path (StrPath): local path of model files
            model_id (str, optional): model_id, a new model will be created if not given. Defaults to None.
            description (str, optional): description to the model. Defaults to None.

        Returns:
            model_id (str): example: model-20210624174426-x9nqh
            model_version_id (str): example: model-version-20210624180756-mdmq4
        """
        bucket_name = self._get_or_create_bucket(bucket_name, self.region)
        prefix = self._get_or_generate_prefix(prefix, model_name)
        tos_path = self._upload_to_tos(local_path, bucket_name, prefix)

        print('>>>tos_path:{}'.format(tos_path))
        resp = self.api_client.create_model(
            model_name=model_name,
            model_format=model_format,
            model_type=model_type,
            path=tos_path,
            model_id=model_id,
            description=description,
        )
        return resp['Result']['ModelID'], resp['Result']['ModelVersionID']

    def list_models(self,
                    model_name=None,
                    model_name_contains=None,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend') -> List[Model]:
        """list models

        Args:
            model_name (str, optional): model name
            model_name_contains (str, optional): filter option, check if
                                model name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Returns:
            list of models
        """
        resp = self.api_client.list_models(model_name, model_name_contains,
                                           offset, page_size, sort_by,
                                           sort_order)
        models = []
        for m in resp['Result']['List']:
            models.append(
                Model(model_name=m['ModelName'],
                      model_id=m['ModelId'],
                      version_id=m['VersionInfo']['ModelVersionID'],
                      version_index=m['VersionInfo']['ModelVersion'],
                      model_format=m['VersionInfo']['ModelFormat'],
                      model_type=m['VersionInfo']['ModelType'],
                      path=m['VersionInfo']['Path'],
                      description=m['VersionInfo']['Description'],
                      source_type=m['VersionInfo']['SourceType']))

    def delete_model(self, model_id):
        """delete model with given model id

        Args:
            model_id (str): model id

        Returns:
            json response
        """
        return self.api_client.delete_model(model_id)

    def list_model_versions(self, model_id: str) -> List[Model]:
        """list model versions with given model_id

        Args:
            model_id (str): model id
        Returns:
            list of Models with distinct versions
        """
        # request for list of versions info
        resp = self.api_client.list_model_versions(model_id)
        # request for model name
        model_name = self.api_client.get_model(model_id)['Result']['ModelName']
        models = []
        for m in resp['Result']['List']:
            models.append(
                Model(model_name=model_name,
                      model_id=model_id,
                      version_id=m['ModelVersionID'],
                      version_index=m['ModelVersion'],
                      model_format=m['ModelFormat'],
                      model_type=m['ModelType'],
                      path=m['Path'],
                      description=m['Description'],
                      source_type=m['SourceType']))
        return models

    def get_model_version(self, model_id: str, model_version_id: str) -> Model:
        """get certain version of a model

        Args:
            model_id (str): model id
            model_version_id (str): model version id

        Returns:
            Model
        """
        resp = self.api_client.get_model_version(model_id, model_version_id)
        m = resp['Result']
        model_name = self.api_client.get_model(model_id)['Result']['ModelName']
        return Model(model_name=model_name,
                     model_id=model_id,
                     version_id=m['ModelVersionID'],
                     version_index=m['ModelVersion'],
                     model_format=m['ModelFormat'],
                     model_type=m['ModelType'],
                     path=m['Path'],
                     description=m['Description'],
                     source_type=m['SourceType'])

    def delete_model_version(self, model_id: str, model_version_id: str):
        """delete certain version of a model

        Args:
            model_id (str): model id
            model_version_id (str): model version id

        Returns:
            json response
        """
        return self.api_client.delete_model_version(model_id, model_version_id)

    def update_model_version(self, model_version_id, description=None):
        """update model version description

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            description (str, optional): New Description of the ModelVersion. Defaults to None.

        Raises:
            Exception: update_model_version failed

        Returns:
            json response
        """
        return self.api_client.update_model_version(model_version_id,
                                                    description)
