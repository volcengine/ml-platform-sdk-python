import json
import math
import os
from collections.abc import Callable
from typing import Optional

import numpy as np
from PIL import Image
from tqdm import tqdm

from volcengine_ml_platform import constant
from volcengine_ml_platform.datasets.dataset import _Dataset, dataset_copy_file
from volcengine_ml_platform.io.tos_files_io import TorchTOSDataset


class ImageDataset(_Dataset):

    def download(self, local_path: Optional[str] = None, limit=-1):
        """download datasets from source

        Args:
            limit (int, optional): download size. Defaults to -1 (no limit).
        """
        # download manifest
        if local_path is not None:
            self.local_path = local_path
        self._get_detail()
        manifest_file_path = self._download_file(self._get_storage_path(),
                                                 self.local_path)
        with open(self._manifest_path(), 'w') as new_manifest_file:
            with open(manifest_file_path) as f:
                print('Downloading datasets ...')
                self.data_count = 0
                for line in tqdm(f):
                    manifest_line = json.loads(line)
                    if 'ImageURL' in manifest_line['Data']:
                        manifest_line['Data']['FilePath'] = self._download_file(
                            manifest_line['Data']['ImageURL'], self.local_path)

                    # create new local metadata file
                    json.dump(manifest_line, new_manifest_file)
                    new_manifest_file.write('\n')
                    self.data_count = self.data_count + 1

                    if self.data_count > limit != -1:
                        break
        self.created = True

    def split(self,
              training_dir: str,
              testing_dir: str,
              ratio=0.8,
              random_state=0):
        """split datasets and return two datasets objects

        Args:
            training_dir (str): [output directory of training data]
            testing_dir (str): [output directory of testing data]
            ratio (float, optional): [training set split ratio].
                                    Defaults to 0.8.
            random_state (int, optional): [random seed]. Defaults to 0.

        Returns:
            two datasets, first one is the training set
        """
        if not self.created:
            raise Exception('datasets has not been created')
        line_count = self.data_count

        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(line_count,
                             math.floor(line_count * (1 - ratio)),
                             replace=False))
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

        train_dataset = ImageDataset(local_path=training_dir)
        test_dataset = ImageDataset(local_path=testing_dir)
        # set new datasets size
        test_dataset.data_count = math.floor(line_count * (1 - ratio))
        train_dataset.data_count = line_count - test_dataset.data_count

        # generate training and testing datasets's manifest file
        train_metadata_path = os.path.join(
            training_dir, constant.DATASET_LOCAL_METADATA_FILENAME)
        test_metadata_path = os.path.join(
            testing_dir, constant.DATASET_LOCAL_METADATA_FILENAME)
        with open(test_metadata_path, 'w') as testing_manifest_file:
            with open(train_metadata_path, 'w') as training_manifest_file:
                index = 0
                with open(self._manifest_path()) as f:
                    for line in f:
                        manifest_line = json.loads(line)
                        if index in test_index_set:
                            dataset_copy_file(manifest_line, self.local_path,
                                              testing_dir)
                            json.dump(manifest_line, testing_manifest_file)
                            testing_manifest_file.write('\n')
                        else:
                            dataset_copy_file(manifest_line, self.local_path,
                                              training_dir)
                            json.dump(manifest_line, training_manifest_file)
                            training_manifest_file.write('\n')
                        index = index + 1

        train_dataset.created = True
        test_dataset.created = True
        return train_dataset, test_dataset

    def load_as_np(self, offset=0, limit=-1):
        """load images as numpy array

        Args:
            offset (int, optional): num of images to skip. Defaults to 0.
            limit (int, optional): num of images to load. Defaults to -1.

        Returns:
            np array of images
            list of annotations
        """
        images = []
        annotations = []

        with open(self._manifest_path()) as f:
            for i, line in enumerate(f):
                manifest_line = json.loads(line)
                if i < offset:
                    continue
                if limit != -1 and i >= offset + limit:
                    break
                file_path = manifest_line['Data']['FilePath']
                image = Image.open(file_path)
                images.append(np.asarray(image))
                annotations.append(manifest_line['Annotation'])

        return np.array(images), annotations

    def parse_image_manifest(self, manifest_file_path):
        # parse manifest
        manifest_info = {'buckets': [], 'keys': [], 'annotations': []}
        with open(manifest_file_path) as f:
            for _, line in enumerate(f):
                manifest_line = json.loads(line)
                url = manifest_line['Data']['ImageURL']
                bucket = url.split('//')[1].split('/')[0]
                key = url.split(f'{bucket}/')[1]
                manifest_info['buckets'].append(bucket)
                manifest_info['keys'].append(key)
                manifest_info['annotations'].append(manifest_line['Annotation'])
        return manifest_info

    def init_torch_dataset(self,
                           transform: Optional[Callable] = None,
                           target_transform: Optional[Callable] = None):
        manifest_info = self.get_manifest_info(self.parse_image_manifest)
        torch_dataset = TorchTOSDataset(manifest_info=manifest_info,
                                        transform=transform,
                                        target_transform=target_transform)

        return torch_dataset
