import json
import logging
import math
import os
import shutil
from urllib.parse import urlparse

import numpy as np
import requests

from ml_platform_sdk.config import config
from ml_platform_sdk.tos import tos


def copy_file(metadata, input_dir, output_dir):
    file_path = metadata['data']['filePath']
    file_dir, file_name = os.path.split(file_path)
    target_dir = os.path.join(output_dir,
                              os.path.relpath(file_dir, start=input_dir))

    # create output file directory
    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError:
        logging.warning('Cannot create directory: %s', target_dir)

    target_file = os.path.join(target_dir, file_name)
    shutil.copy(file_path, target_file)
    metadata['data']['filePath'] = target_file


class Dataset:

    def __init__(self, ak, sk, region, remote_url, local_dir):
        self.ak = ak
        self.sk = sk
        self.region = region
        self.remote_url = remote_url
        self.local_dir = local_dir
        self.tos_client = tos.TOSClient(region=region, ak=ak, sk=sk)

    def __download_file(self, url, target_dir, chunk_size=8192):
        parse_result = urlparse(url)
        file_path = os.path.join(target_dir, parse_result.path[1:])
        dir_path, file_name = os.path.split(file_path)

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

    def download(self):
        manifest_file_path = self.__download_file(self.remote_url,
                                                  self.local_dir)
        with open(
                os.path.join(self.local_dir,
                             config.DATASET_LOCAL_METADATA_FILENAME),
                'w') as new_manifest_file:
            with open(manifest_file_path) as f:
                for line in f:
                    manifest_line = json.loads(line)
                    if 'imageUrl' in manifest_line['data']:
                        manifest_line['data'][
                            'filePath'] = self.__download_file(
                                manifest_line['data']['imageUrl'],
                                self.local_dir)
                    elif 'videoUrl' in manifest_line['data']:
                        manifest_line['data'][
                            'filePath'] = self.__download_file(
                                manifest_line['data']['videoUrl'],
                                self.local_dir)
                    elif 'text' in manifest_line['data']:
                        pass
                    else:
                        raise ValueError('file type is not supported')

                    # create new local metadata file
                    json.dump(manifest_line, new_manifest_file)
                    new_manifest_file.write('\n')

    def split(self, training_dir, testing_dir, ratio=0.8, random_state=0):
        line_count = 0
        with open(
                os.path.join(self.local_dir,
                             config.DATASET_LOCAL_METADATA_FILENAME)) as f:
            for line in f:
                line_count = line_count + 1

        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(line_count,
                             math.floor(line_count * (1 - ratio)),
                             replace=False))
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

        # generate training and testing dataset's manifest file
        train_metadata_path = os.path.join(
            training_dir, config.DATASET_LOCAL_METADATA_FILENAME)
        test_metadata_path = os.path.join(
            testing_dir, config.DATASET_LOCAL_METADATA_FILENAME)

        train_dataset = Dataset(ak=self.ak,
                                sk=self.sk,
                                region=self.region,
                                remote_url=None,
                                local_dir=train_metadata_path)
        test_dataset = Dataset(ak=self.ak,
                               sk=self.sk,
                               region=self.region,
                               remote_url=None,
                               local_dir=train_metadata_path)
        with open(test_metadata_path, 'w') as testing_manifest_file:
            with open(train_metadata_path, 'w') as training_manifest_file:
                index = 0
                with open(
                        os.path.join(
                            self.local_dir,
                            config.DATASET_LOCAL_METADATA_FILENAME)) as f:
                    for line in f:
                        manifest_line = json.loads(line)
                        if index in test_index_set:
                            copy_file(manifest_line, self.local_dir,
                                      testing_dir)
                            json.dump(manifest_line, testing_manifest_file)
                            testing_manifest_file.write('\n')
                        else:
                            copy_file(manifest_line, self.local_dir,
                                      training_dir)
                            json.dump(manifest_line, training_manifest_file)
                            training_manifest_file.write('\n')
                        index = index + 1
        return train_dataset, test_dataset
