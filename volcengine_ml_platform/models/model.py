# -*- coding: utf-8 -*-

import functools
import logging
import os
from threading import local
from typing import Optional, Tuple
from urllib.parse import urlparse

from prettytable import PrettyTable
from tqdm import tqdm

from volcengine_ml_platform.inferences.inference import InferenceService
from volcengine_ml_platform.models import validation
from volcengine_ml_platform.openapi import model_client, resource_client
from volcengine_ml_platform.tos import tos


class Model:

    def __init__(self):
        self.tos_client = tos.TOSClient()
        self.model_client = model_client.ModelClient()
        self.resource_client = resource_client.ResourceClient()

    def _register_validate_and_preprocess(self,
                                          local_path: str,
                                          model_id: Optional[str] = None,
                                          model_name: Optional[str] = None,
                                          model_format: Optional[str] = None,
                                          model_type: Optional[str] = None,
                                          tensor_config: Optional[dict] = None,
                                          model_metrics: Optional[list] = None):
        if local_path is None:
            logging.warning('Model local_path is empty')
            raise ValueError
        if not os.path.exists(local_path):
            logging.warning('Model local_path not exists %s', local_path)
            raise ValueError
        if model_id is None:
            if model_name is None or model_format is None or model_type is None:
                logging.warning(
                    'Model register new model need model_name/model_format/model_type'
                )
                raise ValueError
        else:
            raw_model_name = self.model_client.get_model(
                model_id=model_id)['Result']['ModelName']
            if raw_model_name != model_name:
                logging.warning(
                    'model name is diff from origin, use old model_name')
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

    def _upload_tos(self, local_path) -> str:
        bucket, prefix = self._require_model_tos_storage()

        if os.path.isfile(local_path):
            key = '{}{}'.format(prefix, os.path.basename(local_path))
            self.tos_client.upload_file(local_path, bucket, key=key)

        if os.path.isdir(local_path):
            self_prefix = os.path.basename(local_path.rstrip('/'))
            if self_prefix != '.':
                prefix = '{}{}/'.format(prefix, self_prefix)

            for root, _, files in os.walk(local_path):
                for file in tqdm(files):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, local_path)
                    if rel_path == '.':
                        key = '{}{}'.format(prefix, file)
                    else:
                        key = '{}{}/{}'.format(prefix, rel_path, file)
                    self.tos_client.upload_file(file_path, bucket, key=key)
        return 'tos://{}/{}'.format(bucket, prefix)

    def _download_tos(self, bucket, key, prefix, local_path):
        marker = ''
        while True:
            result = self.tos_client.list_objects(bucket=bucket,
                                                  delimiter='/',
                                                  encoding_type='',
                                                  marker=marker,
                                                  max_keys=1000,
                                                  prefix=key)
            keys = [content['Key'] for content in result.get('Contents', [])]
            dirs = [
                content['Prefix']
                for content in result.get('CommonPrefixes', [])
            ]

            for d in tqdm(dirs):
                dest_pathname = os.path.join(local_path,
                                             os.path.relpath(d, prefix) + '/')
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                self._download_tos(bucket, d, prefix)

            for file in tqdm(keys):
                dest_pathname = os.path.join(local_path,
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

    def _download_model(self, remote_path, local_path):
        parse_url = urlparse(remote_path)
        scheme = parse_url.scheme
        if scheme == 'tos':
            bucket = parse_url.hostname
            key = parse_url.path.lstrip('/')
            self._download_tos(bucket, key, key, local_path)
        else:
            logging.warning('unsupported remote_path, %s', remote_path)

    def register(self,
                 local_path: str,
                 model_id: Optional[str] = None,
                 model_name: Optional[str] = None,
                 model_format: Optional[str] = None,
                 model_type: Optional[str] = None,
                 description: Optional[str] = None,
                 tensor_config: Optional[dict] = None,
                 model_metrics: Optional[list] = None):

        self._register_validate_and_preprocess(local_path, model_id, model_name,
                                               model_format, model_type,
                                               tensor_config, model_metrics)
        tos_path = self._upload_tos(local_path)
        return self.model_client.create_model(model_name=model_name,
                                              model_format=model_format,
                                              model_type=model_type,
                                              model_id=model_id,
                                              path=tos_path,
                                              description=description,
                                              tensor_config=tensor_config,
                                              model_metrics=model_metrics)

    def download(self,
                 model_id: str,
                 model_version: int,
                 local_path: Optional[str] = None):
        if not model_id:
            logging.warning('Model can not be download, model_id is empty')
            raise ValueError

        response = self.model_client.get_model_version("{}-{}".format(
            model_id, model_version))
        remote_path = response['Result']['VersionInfo']['Path']

        self._download_model(remote_path, local_path)
        logging.info("model {}:{} download finished to {}".format(
            model_id, model_version, local_path))

    def unregister(self, model_id: str, model_version: int):
        self.model_client.delete_model_version("{}-{}".format(
            model_id, model_version))

    def unregister_all_versions(self, model_id: str):
        if not model_id:
            logging.warning('model_id is empty')
            return

        self.model_client.delete_model(model_id=model_id)

    def list_models(self,
                    model_name_contains=None,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend'):
        return self.model_client.list_models(
            model_name_contains=model_name_contains,
            offset=offset,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order)

    def get_model_versions(self,
                           model_id: str,
                           model_version: int = None,
                           offset=0,
                           page_size=10,
                           sort_by='CreateTime',
                           sort_order='Descend'):
        if not model_id:
            logging.warning('model_id is empty')
            return

        response = self.model_client.list_model_versions(
            model_id=model_id,
            model_version=model_version,
            offset=offset,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order)
        table = PrettyTable([
            'ModelID', 'Version', 'Format', 'Type', 'RemotePath', 'Description',
            'CreateTime'
        ])
        for model in response['Result']['List']:
            table.add_row([
                model_id, model['ModelVersion'], model['ModelFormat'],
                model['ModelType'], model['Path'], model['Description'],
                model['CreateTime']
            ])
        print(table)
        return response

    def update_model(
        self,
        model_id: str,
        model_name: str = None,
    ):
        return self.model_client.update_model(model_id=model_id,
                                              model_name=model_name)

    def update_model_version(self,
                             model_id: str,
                             model_version: int,
                             description: Optional[str] = None,
                             tensor_config: Optional[dict] = None,
                             model_metrics: Optional[list] = None):
        try:
            validation.validate_tensor_config(tensor_config)
        except Exception as e:
            raise Exception('Invalid tensor config.') from e

        try:
            validation.validate_metrics(model_metrics)
        except Exception as e:
            raise Exception('Invalid models metrics.') from e

        return self.model_client.update_model_version(
            model_version_id="{}-{}".format(model_id, model_version),
            description=description,
            tensor_config=tensor_config,
            model_metrics=model_metrics)

    def deploy(
            self,
            model_id: str,
            model_version: int,
            service_name: str,
            flavor: Optional[str] = 'ml.highcpu.large',
            image_url: Optional[str] = 'machinelearning/tfserving:tf-cuda10.1',
            envs=None,
            replica: Optional[int] = 1,
            description: Optional[str] = None) -> InferenceService:

        inference_service = InferenceService(
            service_name=service_name,
            image_url=image_url,
            flavor_id=self.model_client.get_unique_flavor(
                self.resource_client.list_resource(name=flavor,
                                                   sort_by='vCPU')),
            model_id=model_id,
            model_version_id="{}-{}".format(model_id, model_version),
            envs=envs,
            replica=replica,
            description=description)
        inference_service.create()
        return inference_service

    def create_perf_job(self, model_id: str, model_version: int,
                        tensor_config: dict, job_type: str, job_params: list):

        return self.model_client.create_perf_job(
            model_version_id="{}-{}".format(model_id, model_version),
            tensor_config=tensor_config,
            job_type=job_type,
            job_params=job_params)

    def list_perf_jobs(self,
                       model_id=None,
                       model_version=None,
                       job_id=None,
                       offset=0,
                       page_size=10,
                       sort_by='CreateTime',
                       sort_order='Descend'):
        model_version_id = "{}-{}".format(model_id, model_version)
        return self.model_client.list_perf_jobs(
            model_version_id=model_version_id,
            job_id=job_id,
            offset=offset,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order)

    def cancel_perf_job(self, job_id: str):
        return self.model_client.cancel_perf_job(job_id=job_id)

    def list_perf_tasks(self,
                        task_id=None,
                        job_id=None,
                        offset=0,
                        page_size=10,
                        sort_by='CreateTime',
                        sort_order='Descend'):
        return self.model_client.list_perf_tasks(task_id=task_id,
                                                 job_id=job_id,
                                                 offset=offset,
                                                 page_size=page_size,
                                                 sort_by=sort_by,
                                                 sort_order=sort_order)

    def update_perf_task(self, task_id: str, task_status=None):
        return self.model_client.update_perf_task(task_id=task_id,
                                                  task_status=task_status)

    def calcel_perf_task(self, task_id: str):
        return self.model_client.cancel_perf_task(task_id=task_id)