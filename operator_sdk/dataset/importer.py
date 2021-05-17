import json
import logging
import os
from urllib.parse import urlparse

import requests

from operator_sdk.base import tos
from operator_sdk.service.dataset_service import DatasetService


def download_file(url, target_dir, tos_client=None, chunk_size=8192):
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
        tos_client.download_file(file_path, bucket, key)
    else:
        logging.warning('Cannot handle url scheme: %s', url)
        raise requests.exceptions.InvalidURL

    return file_path


def download_dataset(dataset_id: str, output_dir: str):
    """download dataset with dataset id"""
    # get dataset info with TOP api
    try:
        client = DatasetService()
        resp = client.get_dataset(dataset_id=dataset_id)
    except Exception as e:
        logging.error('Failed to get dataset info, dataset_id: %s, error: %s',
                      dataset_id, e)
        raise Exception('Failed to get dataset info with dataset_id: {}'.format(
            dataset_id)) from e

    resp_json = json.loads(resp)
    storage_url = resp_json['Result']['StoragePath']

    tos_client = tos.TOSClient()

    manifest_file_path = download_file(storage_url,
                                       output_dir,
                                       tos_client=tos_client)
    manifest = list()
    with open(manifest_file_path) as f:
        for line in f:
            manifest_line = json.loads(line)
            data = manifest_line['data']
            meta_type = 'Unknown'
            if 'imageUrl' in data:
                file_path = download_file(data['imageUrl'],
                                          output_dir,
                                          tos_client=tos_client)
                data['filePath'] = file_path
                meta_type = 'image_meta'
            elif 'videoUrl' in data:
                file_path = download_file(data['videoUrl'],
                                          output_dir,
                                          tos_client=tos_client)
                data['filePath'] = file_path
                meta_type = 'video_meta'
            elif 'text' in data:
                meta_type = 'text_meta'
            else:
                raise ValueError('file type is not supported')
            manifest.append(data)
        # create new local metadata file
        with open(os.path.join(output_dir, 'metadata.json'), 'w+') as meta_file:
            json.dump({meta_type: manifest}, meta_file)
