"""提供数据集下载，分裂操作

"""
import json
import logging
import math
import os
import shutil
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

from volcengine_ml_platform import constant
from volcengine_ml_platform.io import tos
from volcengine_ml_platform.openapi import dataset_client

QUEUE_TIMEOUT_SECONDS = 4


def dataset_copy_file(metadata, source_dir, destination_dir):
    """复制文件夹

    Args:
        metadata(dict): 一个 manifest 文件读取的 dict
        source_dir(str): 源文件夹
        destination_dir(str): 目标文件夹

    """
    file_path = metadata["Data"]["FilePath"]
    file_dir, file_name = os.path.split(file_path)
    target_dir = os.path.join(
        destination_dir,
        os.path.relpath(file_dir, start=source_dir),
    )

    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError:
        logging.warning("Cannot create directory: %s", target_dir)

    target_file = os.path.join(target_dir, file_name)
    shutil.copy(file_path, target_file)
    metadata["Data"]["FilePath"] = target_file


class _Dataset:
    def __init__(
        self,
        dataset_id: str = "",
        annotation_id: Optional[str] = None,
        local_path: str = ".",
        tos_source: Optional[str] = None,
    ):
        self.dataset_id = dataset_id
        self.annotation_id = annotation_id
        self.local_path = local_path
        self.tabular_path = ""
        self.tos_source = tos_source
        self.created = False
        self.data_count = 0
        self.detail = None
        self.annotation_detail = None
        self.tos_client = tos.TOSClient()
        self.api_client = dataset_client.DataSetClient()

    def _get_detail(self):
        self._get_dataset_detail()
        self._get_annotation_detail()

    def _get_dataset_detail(self):
        if not self.dataset_id:
            logging.warning(
                "data which don't have dataset id can't get dataset detail",
            )
            return
        try:
            self.detail = self.api_client.get_dataset(
                self.dataset_id,
            )["Result"]
            self.data_count = self.detail["NonTabularDataCount"]
        except Exception as e:
            logging.error("get datasets detail failed, error: %s", e)
            raise Exception("invalid datasets") from e

    def _get_annotation_detail(self):
        if self.annotation_id is None:
            logging.warning(
                "data which don't have annotation dataset id can't get annotation dataset detail",
            )
            return
        try:
            resp = self.api_client.get_annotation_set(
                self.dataset_id,
                self.annotation_id,
            )
            self.annotation_detail = resp["Result"]
        except Exception as e:
            logging.error("get annotation detail failed, error: %s", e)
            raise Exception("invalid annotation") from e

    def _get_storage_path(self) -> str:
        if not self.detail:
            return ""
        if self.annotation_id:
            return self.annotation_detail["StoragePath"]
        return self.detail["StoragePath"]

    def _get_source_path(self) -> str:
        if not self.detail:
            return ""
        return self.detail["SourcePath"]

    def _manifest_path(self):
        return os.path.join(
            self.local_path,
            constant.DATASET_LOCAL_METADATA_FILENAME,
        )

    def _download_file(self, tos_url: str, file_path: str):
        return self.tos_client.download_file(
            tos_url=tos_url, target_file_path=file_path
        )

    def _create_non_manifest_dataset(self):
        print("Downloading the csv file ...")
        self._get_detail()
        print(self.detail)
        assert self._get_storage_path() != ""
        self.tabular_path = self.tos_client.download_file(
            tos_url=self._get_storage_path(),
            target_dir_path=self.local_path,
        )

        if not self.tabular_path:
            raise ValueError("Empty value(self.tabular_path)")
        # count number of lines, not including header line
        with open(self.tabular_path, encoding="utf-8") as f:
            self.data_count = sum(1 for line in f) - 1
        self.created = True

    def _create_manifest_dataset(
        self,
        manifest_keyword: str,
        limit=-1,
    ):

        print("Downloading the mainfest file ...")
        self._get_detail()

        manifest_file_path = self.tos_client.download_file(
            tos_url=self._get_storage_path(),
            target_dir_path=self.local_path,
        )
        manifest_line = []
        urls = []
        with open(manifest_file_path, encoding="utf-8") as f:
            for seqNum, line in enumerate(f.readlines()):
                manifest_line.append(json.loads(line))
                urls.append(manifest_line[seqNum]["Data"][manifest_keyword])
                if limit != -1 and seqNum + 1 >= limit:
                    break

        print("Downloading datasets ...")
        paths = self.tos_client.download_files(
            tos_urls=urls,
            target_dir_path=self.local_path,
            parallelism=10,
        )

        # create a new thread to consume new local maifest file
        print("Generating the local mainfest file...")
        manifest_str = ""
        for idx, path in enumerate(paths):
            manifest_line[idx]["Data"]["FilePath"] = path
            manifest_str += json.dumps(manifest_line[idx]) + "\n"
        with open(
            self._manifest_path(),
            "w",
            encoding="utf-8",
        ) as new_manifest_file:
            new_manifest_file.write(manifest_str)
        print("Update the local mainfest file successful")
        self.created = True

    def split_dataset(
        self,
        dataset_type,
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
            raise Exception("datasets has not been created")
        line_count = self.data_count

        np.random.seed(random_state)
        test_index_set = set(
            np.random.choice(
                line_count,
                math.floor(line_count * (1 - ratio)),
                replace=False,
            ),
        )
        os.makedirs(testing_dir, exist_ok=True)
        os.makedirs(training_dir, exist_ok=True)

        train_dataset = dataset_type(local_path=training_dir)
        test_dataset = dataset_type(local_path=testing_dir)
        # set new datasets size
        test_dataset.data_count = math.floor(line_count * (1 - ratio))
        train_dataset.data_count = line_count - test_dataset.data_count

        # generate training and testing datasets's manifest file
        train_metadata_path = os.path.join(
            training_dir,
            constant.DATASET_LOCAL_METADATA_FILENAME,
        )
        test_metadata_path = os.path.join(
            testing_dir,
            constant.DATASET_LOCAL_METADATA_FILENAME,
        )
        with open(
            test_metadata_path,
            mode="w",
            encoding="utf-8",
        ) as testing_manifest_file:
            with open(
                train_metadata_path,
                mode="w",
                encoding="utf-8",
            ) as training_manifest_file:
                index = 0
                with open(self._manifest_path(), encoding="utf-8") as f:
                    for line in f:
                        manifest_line = json.loads(line)
                        if index in test_index_set:
                            dataset_copy_file(
                                manifest_line,
                                self.local_path,
                                testing_dir,
                            )
                            json.dump(manifest_line, testing_manifest_file)
                            testing_manifest_file.write("\n")
                        else:
                            dataset_copy_file(
                                manifest_line,
                                self.local_path,
                                training_dir,
                            )
                            json.dump(manifest_line, training_manifest_file)
                            training_manifest_file.write("\n")
                        index = index + 1

        train_dataset.created = True
        test_dataset.created = True
        return train_dataset, test_dataset

    def get_paths(self, offset=0, limit=-1) -> Optional[Tuple[List, Optional[List]]]:
        """get filepaths of dataset files

        Args:
            offset (int, optional): num of images to skip. Defaults to 0.
            limit (int, optional): num of images to load. Defaults to -1.

        Returns:
            list of paths. Single tabular_path will be returned if it is a Tabular Dataset
            list of annotations. No annotations for TabularDataset
        """
        if self.tabular_path:
            return [self.tabular_path], None
        paths = []
        annotations = []

        with open(self._manifest_path(), encoding="utf-8") as f:
            for i, line in enumerate(f):
                manifest_line = json.loads(line)
                if i < offset:
                    continue
                if limit != -1 and i >= offset + limit:
                    break
                file_path = manifest_line["data"]["FilePath"]
                paths.append(file_path)
                annotations.append(manifest_line["annotation"])

        return paths, annotations

    def get_manifest_info(self, parse_func):
        # download manifest
        assert self.tos_source is not None and self.local_path is not None
        manifest_file_path = self._download_file(
            self.tos_source,
            self.local_path,
        )
        return parse_func(manifest_file_path)
