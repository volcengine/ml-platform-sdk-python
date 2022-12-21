import logging
import json
import os

from volcengine_ml_platform.openapi import dataset_client
from volcengine_ml_platform.dataloader.dataset import VeDataset
from volcengine_ml_platform.dataloader.point_cloud_dataset import PointCloudDataset


def GetDatasets(root_dir, loader_fn, meta_datas=None, transformer_fn=None, annotation_fn=None):
    api_client = dataset_client.DataSetClient()
    try:
        if meta_datas is None:
            meta_info_str = os.getenv("DATASET_META")
            meta_datas = json.loads(meta_info_str)
        datasets = []
        for i in range(len(meta_datas)):
            meta_data = meta_datas[i]
            dataset_id = meta_data.get('DatasetId')
            dataset_type = api_client.get_dataset(dataset_id).get('Result', {}).get('DataType')
            if dataset_type is not None:
                if dataset_type == 'DotCloud':
                    datasets.append(PointCloudDataset(root_dir, meta_data, loader_fn, transformer_fn=transformer_fn, annotation_fn=annotation_fn))
                else:
                    datasets.append(VeDataset(root_dir, meta_data, loader_fn, transformer_fn=transformer_fn, annotation_fn=annotation_fn))
        return datasets
    except Exception as e:
        logging.error("GetDatasets error:", e)
    return []
