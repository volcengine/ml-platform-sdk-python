import json
import logging
import math
import os
import shutil
from enum import Enum, auto
from urllib.parse import urlparse

import numpy as np
import requests
from PIL import Image
from tqdm import tqdm

from ml_platform_sdk.config import config
from ml_platform_sdk.tos import tos


class DataType(Enum):
    IMAGE = auto()
    VIDEO = auto()
    TEXT = auto()
    OTHER = auto()
    UNKNOWN = auto()


class Dataset:
    """
    dataset object
    """

    def __init__(self, ak, sk, region, remote_url, local_dir):
        self.ak = ak
        self.sk = sk
        self.region = region
        self.remote_url = remote_url
        self.local_dir = local_dir
        self.tos_client = tos.TOSClient(region=region, ak=ak, sk=sk)
        self.size = -1
        self.data_type = DataType.UNKNOWN

    def __manifest_path(self):
        return os.path.join(self.local_dir,
                            config.DATASET_LOCAL_METADATA_FILENAME)

    def __download_file(self, url, target_dir, chunk_size=8192):
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

    def __copy_file(self, metadata, input_dir, output_dir):
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

    def download(self, limit=-1):
        """download dataset from source

        Args:
            limit (int, optional): download size. Defaults to -1 (no limit).
        """
        # download manifest
        manifest_file_path = self.__download_file(self.remote_url,
                                                  self.local_dir)
        with open(self.__manifest_path(), 'w') as new_manifest_file:
            with open(manifest_file_path) as f:
                print('Downloading dataset ...')
                self.size = 0
                for line in tqdm(f):
                    manifest_line = json.loads(line)
                    if 'imageUrl' in manifest_line['data']:
                        manifest_line['data'][
                            'filePath'] = self.__download_file(
                                manifest_line['data']['imageUrl'],
                                self.local_dir)
                        self.data_type = DataType.IMAGE
                    elif 'videoUrl' in manifest_line['data']:
                        manifest_line['data'][
                            'filePath'] = self.__download_file(
                                manifest_line['data']['videoUrl'],
                                self.local_dir)
                        self.data_type = DataType.VIDEO
                    elif 'text' in manifest_line['data']:
                        self.data_type = DataType.TEXT
                    else:
                        manifest_line['data'][
                            'filePath'] = self.__download_file(
                                manifest_line['data']['otherUrl'],
                                self.local_dir)
                        self.data_type = DataType.OTHER

                    # create new local metadata file
                    json.dump(manifest_line, new_manifest_file)
                    new_manifest_file.write('\n')
                    self.size = self.size + 1

                    if self.size > limit and limit != -1:
                        break

    def split(self,
              training_dir: str,
              testing_dir: str,
              ratio=0.8,
              random_state=0):
        """split dataset and return two dataset objects

        Args:
            training_dir (str): [output directory of training data]
            testing_dir (str): [output directory of testing data]
            ratio (float, optional): [training set split ratio].
                                    Defaults to 0.8.
            random_state (int, optional): [random seed]. Defaults to 0.

        Returns:
            two datasets, first one is the training set
        """
        line_count = self.size
        if line_count == -1:
            raise Exception('dataset has not been downloaded yet')

        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(line_count,
                             math.floor(line_count * (1 - ratio)),
                             replace=False))
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

        train_dataset = Dataset(ak=self.ak,
                                sk=self.sk,
                                region=self.region,
                                remote_url=None,
                                local_dir=training_dir)
        test_dataset = Dataset(ak=self.ak,
                               sk=self.sk,
                               region=self.region,
                               remote_url=None,
                               local_dir=testing_dir)
        # set new dataset size
        test_dataset.size = math.floor(line_count * (1 - ratio))
        train_dataset.size = line_count - test_dataset.size
        # set new dataset type
        test_dataset.data_type = self.data_type
        train_dataset.data_type = self.data_type

        # generate training and testing dataset's manifest file
        train_metadata_path = os.path.join(
            training_dir, config.DATASET_LOCAL_METADATA_FILENAME)
        test_metadata_path = os.path.join(
            testing_dir, config.DATASET_LOCAL_METADATA_FILENAME)
        with open(test_metadata_path, 'w') as testing_manifest_file:
            with open(train_metadata_path, 'w') as training_manifest_file:
                index = 0
                with open(self.__manifest_path()) as f:
                    for line in f:
                        manifest_line = json.loads(line)
                        if index in test_index_set:
                            self.__copy_file(manifest_line, self.local_dir,
                                             testing_dir)
                            json.dump(manifest_line, testing_manifest_file)
                            testing_manifest_file.write('\n')
                        else:
                            self.__copy_file(manifest_line, self.local_dir,
                                             training_dir)
                            json.dump(manifest_line, training_manifest_file)
                            training_manifest_file.write('\n')
                        index = index + 1
        return train_dataset, test_dataset

    def get_dataset_type(self):
        if self.size == -1:
            raise Exception('dataset has not been downloaded yet')
        return self.data_type

    def load_images_np(self, offset=0, limit=-1):
        if self.get_dataset_type() != DataType.IMAGE:
            raise Exception('dataset is not image type')

        images = []
        annotations = []

        with open(self.__manifest_path()) as f:
            for i, line in enumerate(f):
                manifest_line = json.loads(line)
                if i < offset:
                    continue
                if limit != -1 and i >= offset + limit:
                    break
                file_path = manifest_line['data']['filePath']
                image = Image.open(file_path)
                images.append(np.asarray(image))
                annotations.append(manifest_line['annotation'])

        return np.array(images), annotations
