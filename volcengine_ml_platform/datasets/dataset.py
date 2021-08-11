import logging
import os
import shutil
from typing import Optional, Tuple, List
from urllib.parse import urlparse
import json
import requests

from volcengine_ml_platform import initializer
from volcengine_ml_platform.config import credential as auth_credential, constants
from volcengine_ml_platform.tos import tos
from volcengine_ml_platform.openapi import client


def dataset_copy_file(metadata, source_dir, destination_dir):
    file_path = metadata['Data']['FilePath']
    file_dir, file_name = os.path.split(file_path)
    target_dir = os.path.join(destination_dir,
                              os.path.relpath(file_dir, start=source_dir))

    # create output file directory
    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError:
        logging.warning('Cannot create directory: %s', target_dir)

    target_file = os.path.join(target_dir, file_name)
    shutil.copy(file_path, target_file)
    metadata['Data']['FilePath'] = target_file


class _Dataset:
    """
    datasets object
    """

    def __init__(self,
                 dataset_id: Optional[str] = None,
                 annotation_id: Optional[str] = None,
                 local_path: Optional[str] = None,
                 tos_source: Optional[str] = None,
                 credential: Optional[auth_credential.Credential] = None):
        self.dataset_id = dataset_id
        self.annotation_id = annotation_id
        self.local_path = local_path
        self.tabular_path = None
        self.tos_source = tos_source
        self.created = False
        self.data_count = 0
        self.detail = None
        self.annotation_detail = None
        self.credential = credential or initializer.global_config.get_credential(
        )
        self.tos_client = tos.TOSClient(credential)
        self.api_client = client.APIClient(credential)

    def _get_detail(self):
        self._get_dataset_detail()
        self._get_annotation_detail()

    def _get_dataset_detail(self):
        if self.dataset_id is None:
            return
        try:
            self.detail = self.api_client.get_dataset(self.dataset_id)['Result']
        except Exception as e:
            logging.error('get datasets detail failed, error: %s', e)
            raise Exception('invalid datasets') from e

    def _get_annotation_detail(self):
        if self.annotation_id is None:
            return
        try:
            resp = self.api_client.get_annotation_set(self.dataset_id,
                                                      self.annotation_id)
            self.annotation_detail = resp['Result']
        except Exception as e:
            logging.error('get annotation detail failed, error: %s', e)
            raise Exception('invalid annotation') from e

    def _get_storage_path(self) -> str:
        if self.detail is None:
            return ""
        if self.annotation_id is not None:
            return self.annotation_detail['StoragePath']
        return self.detail['StoragePath']

    def _manifest_path(self):
        return os.path.join(self.local_path,
                            constants.DATASET_LOCAL_METADATA_FILENAME)

    def _download_file(self, url, target_dir, chunk_size=8192):
        parse_result = urlparse(url)
        file_path = os.path.join(target_dir, parse_result.path[1:])
        dir_path, _ = os.path.split(file_path)

        # create file directory
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            logging.warning('Cannot create download directory: %s', dir_path)

        # download file base on url schemes
        if parse_result.scheme == 'https' or parse_result.scheme == 'http':
            # write response chunks in file
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb+') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        f.write(chunk)
        elif parse_result.scheme == 'tos':
            bucket = parse_result.netloc.split('.')[0]
            key = parse_result.path[1:]
            self.tos_client.download_file(file_path, bucket, key)
        else:
            logging.warning('Cannot handle url scheme: %s', url)
            raise requests.exceptions.InvalidURL

        return file_path

    def get_paths(self, offset=0, limit=-1) -> Tuple[List, List]:
        """get filepaths of dataset files

        Args:
            offset (int, optional): num of images to skip. Defaults to 0.
            limit (int, optional): num of images to load. Defaults to -1.

        Returns:
            list of paths. Single tabular_path will be returned if it is a TabularDataset
            list of annotations. No annotations for TabularDataset
        """
        if not self.tabular_path:
            return [self.tabular_path], None
        paths = []
        annotations = []

        with open(self._manifest_path()) as f:
            for i, line in enumerate(f):
                manifest_line = json.loads(line)
                if i < offset:
                    continue
                if limit != -1 and i >= offset + limit:
                    break
                file_path = manifest_line['data']['FilePath']
                paths.append(file_path)
                annotations.append(manifest_line['annotation'])

        return paths, annotations

    def get_manifest_info(self, parse_func):
        # download manifest
        assert self.tos_source is not None and self.local_path is not None
        manifest_file_path = self._download_file(self.tos_source,
                                                 self.local_path)
        return parse_func(manifest_file_path)
