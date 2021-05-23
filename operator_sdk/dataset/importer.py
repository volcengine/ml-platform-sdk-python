import json
import logging
import os
from urllib.parse import urlparse

import requests

from operator_sdk.base import tos, env
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


def download_dataset(dataset_id: str, output_dir: str, region: str, ak: str,
                     sk: str):
    """download dataset with dataset id"""
    output_dir = os.path.join(output_dir, dataset_id)
    os.makedirs(output_dir, exist_ok=True)
    # get dataset info with TOP api
    try:
        client = DatasetService(region, ak, sk)
        resp = client.get_dataset(dataset_id=dataset_id)
    except Exception as e:
        logging.error('Failed to get dataset info, dataset_id: %s, error: %s',
                      dataset_id, e)
        raise Exception('Failed to get dataset info with dataset_id: {}'.format(
            dataset_id)) from e
    storage_url = resp['Result']['StoragePath']

    tos_client = tos.TOSClient(region, ak, sk)

    manifest_file_path = download_file(storage_url,
                                       output_dir,
                                       tos_client=tos_client)
    with open(os.path.join(output_dir, env.LOCAL_METADATA_FILENAME),
              'w+') as new_manifest_file:
        with open(manifest_file_path) as f:
            for line in f:
                manifest_line = json.loads(line)
                if 'imageUrl' in manifest_line['data']:
                    file_path = download_file(manifest_line['data']['imageUrl'],
                                              output_dir,
                                              tos_client=tos_client)
                    manifest_line['data']['filePath'] = file_path
                elif 'videoUrl' in manifest_line['data']:
                    file_path = download_file(manifest_line['data']['videoUrl'],
                                              output_dir,
                                              tos_client=tos_client)
                    manifest_line['data']['filePath'] = file_path
                elif 'text' in manifest_line['data']:
                    pass
                else:
                    raise ValueError('file type is not supported')

                # create new local metadata file
                json.dump(manifest_line, new_manifest_file)
                new_manifest_file.write('\n')
