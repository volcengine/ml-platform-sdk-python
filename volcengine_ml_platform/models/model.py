# -*- coding: utf-8 -*-

import logging
import os
from typing import Optional, Tuple
from urllib.parse import urlparse

from prettytable import PrettyTable
from tqdm import tqdm

from volcengine_ml_platform.inferences.inference import InferenceService
from volcengine_ml_platform.models import validation
from volcengine_ml_platform.openapi import model_client, resource_client
from volcengine_ml_platform.tos import tos


# TODO 去掉model_version_id
class Model:

    def __init__(self,
                 model_id: Optional[str] = None,
                 local_path: Optional[str] = None):
        self.model_id = model_id
        self.model_version = None
        self.model_version_id = None
        self.model_name = None
        self.model_format = None
        self.model_type = None
        self.local_path = local_path
        self.remote_path = None
        self.tensor_config = None
        self.model_metrics = None
        self.tos_client = tos.TOSClient()
        self.model_client = model_client.ModelClient()
        self.resource_client = resource_client.ResourceClient()
        self.inference_services = dict()
        if self.model_id is None and self.local_path is None:
            logging.warning('Model init need model_id or local_path')
            raise ValueError

    def _sync(self):
        if self.model_version is None:
            response = self.model_client.get_model(model_id=self.model_id)
            self.model_version = response['Result']['VersionInfo'][
                'ModelVersion']
            self.model_version_id = response['Result']['VersionInfo'][
                'ModelVersionID']
            self.remote_path = response['Result']['VersionInfo']['Path']
            self.model_name = response['Result']['ModelName']
            self.model_format = response['Result']['VersionInfo']['ModelFormat']
            self.model_type = response['Result']['VersionInfo']['ModelType']
        else:
            response = self.model_client.list_model_versions(
                model_id=self.model_id, model_version=self.model_version)
            if response['Result']['Total'] == 0:
                logging.warning('Model selected version is not exists')
                raise ValueError
            self.model_version = response['Result']['List'][0]['ModelVersion']
            self.model_version_id = response['Result']['List'][0][
                'ModelVersionID']
            self.remote_path = response['Result']['List'][0]['Path']
            self.model_name = self.model_client.get_model(
                model_id=self.model_id)['Result']['ModelName']
            self.model_format = response['Result']['List'][0]['ModelFormat']
            self.model_type = response['Result']['List'][0]['ModelType']

    def _clear(self):
        self.model_version = None
        self.model_version_id = None
        self.remote_path = None

    def _restore(self):
        self._clear()
        self.model_id = None

    def _register_validate_and_preprocess(self,
                                          model_name: Optional[str] = None,
                                          model_format: Optional[str] = None,
                                          model_type: Optional[str] = None,
                                          tensor_config: Optional[dict] = None,
                                          model_metrics: Optional[list] = None):
        if self.local_path is None:
            logging.warning('Model local_path is empty')
            raise ValueError
        if not os.path.exists(self.local_path):
            logging.warning('Model local_path is not exists %s',
                            self.local_path)
            raise ValueError
        if self.model_id is None:
            if model_name is None or model_format is None or model_type is None:
                logging.warning(
                    'Model register new models need model_name/model_format/model_type'
                )
                raise ValueError
            self.model_version = self.model_client.get_model_next_version(
                model_id=self.model_id)['Result']['ModelVersion']
        else:
            self.model_version = self.model_client.get_model_next_version(
                model_id=self.model_id)['Result']['ModelVersion']
            self.model_name = self.model_client.get_model(
                model_id=self.model_id)['Result']['ModelName']
            if model_name != self.model_name:
                logging.warning(
                    'models name is diff from origin, use old model_name')
        try:
            validation.validate_tensor_config(tensor_config)
        except Exception as e:
            raise Exception('Invalid tensor config.') from e

        try:
            validation.validate_metrics(model_metrics)
        except Exception as e:
            raise Exception('Invalid models metrics.') from e

    def _require_model_tos_storage(self) -> Tuple[str, str]:
        response = self.model_client.get_tos_upload_path(
            service_name='modelrepo', path=['from-sdk-repo'])
        return response['Result']['Bucket'], response['Result']['KeyPrefix']

    def _upload_tos(self):
        bucket, prefix = self._require_model_tos_storage()

        if os.path.isfile(self.local_path):
            key = '{}{}'.format(prefix, os.path.basename(self.local_path))
            self.tos_client.upload_file(self.local_path, bucket, key=key)

        if os.path.isdir(self.local_path):
            self_prefix = os.path.basename(self.local_path.rstrip('/'))
            if self_prefix != '.':
                prefix = '{}{}/'.format(prefix, self_prefix)

            for root, dirs, files in os.walk(self.local_path):
                for file in tqdm(files):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, self.local_path)
                    if rel_path == '.':
                        key = '{}{}'.format(prefix, file)
                    else:
                        key = '{}{}/{}'.format(prefix, rel_path, file)
                    self.tos_client.upload_file(file_path, bucket, key=key)
        self.remote_path = 'tos://{}/{}'.format(bucket, prefix)

    def _download_tos(self, bucket, key, prefix):
        marker = ''
        while True:
            result = self.tos_client.list_objects(bucket=bucket,
                                                  delimiter='/',
                                                  encoding_type='',
                                                  marker=marker,
                                                  max_keys=1000,
                                                  prefix=key)
            keys = [
                content['Key'] for content in result.get('Contents', list())
            ]
            dirs = [
                content['Prefix']
                for content in result.get('CommonPrefixes', list())
            ]

            for d in tqdm(dirs):
                dest_pathname = os.path.join(self.local_path,
                                             os.path.relpath(d, prefix) + '/')
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                self._download_tos(bucket, d, prefix)

            for file in tqdm(keys):
                dest_pathname = os.path.join(self.local_path,
                                             os.path.relpath(file, prefix))
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))

                if not os.path.isdir(dest_pathname):
                    self.tos_client.s3_client.download_file(
                        bucket, file, dest_pathname)

            if result['IsTruncated']:
                marker = result['Contents'][-1]['Key']
                continue
            break

    def _download_model(self):
        if self.remote_path is None or self.model_version is None:
            logging.info('Model remote_path is empty, need sync')
            self._sync()

        parse_url = urlparse(self.remote_path)
        scheme = parse_url.scheme
        if scheme == 'tos':
            bucket = parse_url.hostname
            key = parse_url.path.lstrip('/')
            self._download_tos(bucket, key, key)
        else:
            logging.warning('unsupported remote_path, %s', self.remote_path)

    def register(self,
                 model_name: Optional[str] = None,
                 model_format: Optional[str] = None,
                 model_type: Optional[str] = None,
                 description: Optional[str] = None,
                 tensor_config: Optional[dict] = None,
                 model_metrics: Optional[list] = None):
        self.model_name = model_name
        self.model_format = model_format
        self.model_type = model_type
        self.tensor_config = tensor_config
        self.model_metrics = model_metrics
        try:
            self._register_validate_and_preprocess(model_name, model_format,
                                                   model_type, tensor_config,
                                                   model_metrics)
            self._upload_tos()
            response = self.model_client.create_model(
                model_name=self.model_name,
                model_format=self.model_format,
                model_type=self.model_type,
                model_id=self.model_id,
                path=self.remote_path,
                description=description,
                tensor_config=tensor_config,
                model_metrics=model_metrics)
            self.model_version = response['Result']['ModelVersion']
            self.model_id = response['Result']['ModelID']
        except Exception as e:
            logging.warning('Model failed to register')
            raise Exception('Model is invalid') from e

    def download(self,
                 model_version: Optional[int] = None,
                 local_path: Optional[str] = None):
        if local_path:
            self.local_path = local_path
        if model_version:
            self.model_version = model_version
        if self.model_id is None:
            logging.warning('Model can not be download, model_id is empty')
            raise ValueError
        self._sync()

        try:
            self._download_model()
        except Exception as e:
            logging.warning('Model failed to download')
            raise Exception('Model is invalid') from e

    def unregister(self):
        if self.model_id is None:
            logging.warning('Model has not been registered')
            return

        self._sync()
        try:
            self.model_client.delete_model_version(
                model_version_id=self.model_version_id)
        except Exception as e:
            logging.warning('Model failed to unregister')
            raise Exception('Model is invalid') from e
        self._clear()

    def unregister_all_versions(self):
        if self.model_id is None:
            logging.warning('Model has been registered')
            return
        try:
            self.model_client.delete_model(model_id=self.model_id)
        except Exception as e:
            logging.warning('Model failed to unregister all versions')
            raise Exception('Model is invalid') from e
        self._restore()

    def print(self):
        if self.model_id is None:
            logging.warning('Model has not been registered')
            raise ValueError

        try:
            response = self.model_client.list_model_versions(
                model_id=self.model_id, page_size=20)
            table = PrettyTable([
                'ID', 'Version', 'Format', 'Type', 'RemotePath', 'Description',
                'CreateTime'
            ])
            for model in response['Result']['List']:
                table.add_row([
                    model['ModelVersionID'], model['ModelVersion'],
                    model['ModelFormat'], model['ModelType'], model['Path'],
                    model['Description'], model['CreateTime']
                ])
            print(table)
        except Exception as e:
            logging.warning('Model failed to explain')
            raise Exception('Model is invalid') from e

    def deploy(
            self,
            force: Optional[bool] = False,
            flavor: Optional[str] = 'ml.highcpu.large',
            image_id:
        Optional[
            str] = 'machinelearning/cuda10:1.0.10',
            model_version: Optional[int] = None,
            envs=None,
            replica: Optional[int] = 1,
            description: Optional[str] = None) -> InferenceService:
        if model_version:
            self.model_version = model_version
        self._sync()

        if self.model_version in self.inference_services.keys():
            if not force:
                logging.warning('models has been deployed')
                return self.inference_services[self.model_version]
            logging.warning(
                'models deploy force, the old inference_service will lost')

        inference_service = InferenceService(
            service_name=self.model_name,
            image_id=image_id,
            flavor_id=self.model_client.get_unique_flavor(
                self.resource_client.list_resource(name=flavor,
                                                   sort_by='vCPU')),
            model_id=self.model_id,
            model_version_id=self.model_version_id,
            envs=envs,
            replica=replica,
            description=description)
        inference_service.create()
        self.inference_services.update({self.model_version: inference_service})
        return inference_service

    def undeploy(self):
        if self.model_version in self.inference_services.keys():
            self.inference_services[self.model_version].stop()
        else:
            logging.warning('models has not been deployed')
