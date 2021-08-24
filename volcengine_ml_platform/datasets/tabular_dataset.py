# -*- coding: utf-8 -*-

import math
import os
from typing import Optional
import numpy as np

from volcengine_ml_platform.datasets.dataset import _Dataset


class TabularDataset(_Dataset):

    def download(self, local_path: Optional[str] = None):
        if local_path is not None:
            self.local_path = local_path
        self.tabular_path = self._download_file(
            self._get_storage_path(),  # TODO tabular file hasn't storage_path()
            self.local_path)
        self.created = True

        # count number of lines, not including header line
        with open(self.tabular_path, encoding='utf-8') as f:
            self.data_count = sum(1 for line in f) - 1

    def split(self,
              training_dir: str,
              testing_dir: str,
              ratio=0.8,
              random_state=0):
        """split dataset and return two dataset objects

        Args:
            training_dir (str): output directory of training data
            testing_dir (str): output directory of testing data
            ratio (float, optional): training set split ratio.
                                    Defaults to 0.8.
            random_state (int, optional): random seed. Defaults to 0.

        Returns:
            two datasets, first one is the training set
        """
        if not self.created:
            raise Exception('dataset has not been created')

        if training_dir == testing_dir:
            raise ValueError(
                'training directory can not be the same as testing directory')

        csv_name = os.path.basename(self.tabular_path)
        train_csv_path = os.path.join(training_dir, csv_name)
        test_csv_path = os.path.join(testing_dir, csv_name)

        line_count = self.data_count
        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(line_count,
                             math.floor(line_count * (1 - ratio)),
                             replace=False))
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

        train_dataset = TabularDataset(local_path=training_dir)
        test_dataset = TabularDataset(local_path=testing_dir)
        # set new dataset size
        test_dataset.data_count = math.floor(line_count * (1 - ratio))
        train_dataset.data_count = line_count - test_dataset.data_count

        with open(test_csv_path, mode='w', encoding='utf-8') as test_file:
            with open(train_csv_path, mode='w', encoding='utf-8') as train_file:
                index = -1
                with open(self.tabular_path, encoding='utf-8') as input_file:
                    for line in input_file:
                        # write header
                        if index == -1:
                            test_file.write(line)
                            train_file.write(line)

                        if index in test_index_set:
                            test_file.write(line)
                        else:
                            train_file.write(line)

                        index = index + 1

        train_dataset.created = True
        test_dataset.created = True
        return train_dataset, test_dataset
