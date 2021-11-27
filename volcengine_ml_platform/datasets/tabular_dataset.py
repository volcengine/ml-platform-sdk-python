import math
import os

import numpy as np

from volcengine_ml_platform.datasets.dataset import _Dataset


class TabularDataset(_Dataset):
    """
    TabularDataset创建函数同 ``ImageDataset``

    """

    def download(self, local_path: str = "TabularDataset"):
        """把数据集从 TOS 下载到本地

        Args:
            local_path(str): 设置下载目录
        """

        if local_path:
            self.local_path = local_path
        self._create_non_manifest_dataset()

    def split_init(self, training_dir: str, testing_dir: str):
        if not self.created:
            raise Exception("dataset has not been created")

        if training_dir == testing_dir:
            raise ValueError(
                "training directory can not be the same as testing directory",
            )
        if not self.tabular_path:
            raise ValueError("Empty value(tabular_path)")
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

    def split_tabular(
        self, training_dir: str, testing_dir: str, ratio=0.8, random_state=0
    ):
        line_count = self.data_count
        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(
                line_count,
                math.floor(line_count * (1 - ratio)),
                replace=False,
            ),
        )
        csv_name = os.path.basename(self.tabular_path)
        train_csv_path = os.path.join(training_dir, csv_name)
        test_csv_path = os.path.join(testing_dir, csv_name)
        with open(test_csv_path, mode="w", encoding="utf-8") as test_file:
            with open(
                train_csv_path,
                mode="w",
                encoding="utf-8",
            ) as train_file:
                index = -1
                if not self.tabular_path:
                    raise ValueError("Empty Value(tabular_path)")
                with open(self.tabular_path, encoding="utf-8") as input_file:
                    for line in input_file:
                        # write header
                        if index == -1:
                            test_file.write(line)
                            train_file.write(line)
                            index = index + 1
                            continue

                        if index in test_index_set:
                            test_file.write(line)
                        else:
                            train_file.write(line)

                        index = index + 1

    def split(
        self,
        training_dir: str,
        testing_dir: str,
        ratio=0.8,
        random_state=0,
    ):
        """把数据集分割成两个数据集对象（测试集合训练集）

        Args:
            training_dir (str): 训练集输出目录
            testing_dir (str): 测试集输出目录
            ratio (float, optional): 训练集数据所占比例，默认为 0.8
            random_state (int, optional): 随机数种子

        Returns:
            返回两个数据集，第一个是训练集
        """

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
        self.split_init(training_dir, testing_dir)

        train_dataset = TabularDataset(local_path=training_dir)
        test_dataset = TabularDataset(local_path=testing_dir)
        # set tabular_path
        csv_name = os.path.basename(self.tabular_path)
        train_dataset.tabular_path = os.path.join(training_dir, csv_name)
        test_dataset.tabular_path = os.path.join(testing_dir, csv_name)
        # set new dataset size
        line_count = self.data_count
        test_dataset.data_count = math.floor(line_count * (1 - ratio))
        train_dataset.data_count = line_count - test_dataset.data_count

        self.split_tabular(training_dir, testing_dir, ratio, random_state)

        train_dataset.created = True
        test_dataset.created = True
        return train_dataset, test_dataset
