import json
import logging
import os
import heapq
import time

from multiprocessing.dummy import Queue, Value, Process
from multiprocessing.pool import ThreadPool as Pool
import shutil
from typing import Optional, Tuple, List
from urllib.parse import urlparse
import requests
from tqdm import tqdm

from volcengine_ml_platform import constant
from volcengine_ml_platform.openapi import dataset_client
from volcengine_ml_platform.tos import tos

CONCURENCY_NUM = 10
QUEUE_TIMEOUT_SECONDS = 4


def dataset_copy_file(metadata, source_dir, destination_dir):
    file_path = metadata['Data']['FilePath']
    file_dir, file_name = os.path.split(file_path)
    target_dir = os.path.join(destination_dir,
                              os.path.relpath(file_dir, start=source_dir))

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
                 tos_source: Optional[str] = None):
        self.dataset_id = dataset_id
        self.annotation_id = annotation_id
        self.local_path = local_path
        self.tabular_path = None
        self.dir_record = set()
        self.concurrency_num = CONCURENCY_NUM
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
                            constant.DATASET_LOCAL_METADATA_FILENAME)

    def _create_dir(self, dir_path):
        if dir_path not in self.dir_record:
            self.dir_record.add(dir_path)
            try:
                os.makedirs(dir_path, exist_ok=True)
            except OSError:
                logging.warning('Cannot create download directory: %s',
                                dir_path)
            logging.info('create download directory: %s', dir_path)

        return dir_path

    def _download_file(self, url, target_dir, chunk_size=8192):
        parse_result = urlparse(url)
        file_path = os.path.join(target_dir, parse_result.path[1:])
        dir_path, _ = os.path.split(file_path)

        self._create_dir(dir_path)

        if parse_result.scheme == 'https' or parse_result.scheme == 'http':
            # write response chunks in file
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, mode='wb+', encoding='utf-8') as f:
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

    def _download_producer(self, manifest_line, url, target_dir, seqNum,
                           res_que):
        file = self._download_file(url, target_dir)
        manifest_line["Data"]["FilePath"] = file
        res_que.put((seqNum, manifest_line))

    def _update_local_mainfest_consumer(self, que, done):
        mainfest_str = ""
        heaplist = []
        orderNum = 0
        # consume items even producer processes has done
        with tqdm(total=self.data_count) as pbar:
            while not que.empty() or done.value == 0:
                if que.empty():
                    time.sleep(0.1)
                    continue
                try:
                    heapq.heappush(heaplist,
                                   que.get(timeout=QUEUE_TIMEOUT_SECONDS))
                    pbar.update(1)
                except TimeoutError:
                    logging.waning(
                        "fail to catch all files in the mainfest file")
                while len(heaplist) >= 1 and orderNum == heaplist[0][0]:
                    orderNum += 1
                    mainfest_str += json.dumps(heaplist[0][1]) + "\n"
                    heapq.heappop(heaplist)

        with open(self._manifest_path(), mode='w',
                  encoding='utf-8') as new_manifest_file:
            new_manifest_file.write(mainfest_str)
        print("Update the local mainfest file successful")

    def _create_mainfest_dataset(self,
                                 local_path: Optional[str] = None,
                                 manifest_keyword: Optional[str] = None,
                                 limit=-1):

        if local_path is not None:
            self.local_path = local_path
        print('Downloading the mainfest file ...')
        self._get_detail()
        manifest_file_path = self._download_file(self._get_storage_path(),
                                                 self.local_path)

        print('Downloading datasets ...')
        self.data_count = 0
        res_que = Queue()
        done = Value("i", 0)
        # use pool to download file and produce new mainfest lines
        p = Pool(self.concurrency_num)
        with open(manifest_file_path, encoding='utf-8') as f:
            for seqNum, line in enumerate(f):
                manifest_line = json.loads(line)
                if manifest_keyword in manifest_line['Data']:
                    p.apply_async(
                        self._download_producer,
                        (manifest_line, manifest_line['Data'][manifest_keyword],
                         self.local_path, seqNum, res_que))
                self.data_count = self.data_count + 1
                if limit != -1 and self.data_count > limit:
                    break
        p.close()

        # create a new thread to consume new local maifest file
        print('Generating the local mainfest file...')
        update = Process(target=self._update_local_mainfest_consumer,
                         args=(res_que, done))
        update.start()
        p.join()
        done.value = 1
        update.join()
        self.created = True

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

        with open(self._manifest_path(), encoding='utf-8') as f:
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
