import json
import os

from volcengine_ml_platform.annotation import Annotation
from volcengine_ml_platform.openapi import dataset_client


class VeDataset():
    def __init__(self, root_dir, dataset_meta, loader, transformer_fn=None, annotation_fn=None):
        self.dataset_id = dataset_meta.get('DatasetId')
        self.annotation_id = dataset_meta.get('AnnotationId')
        self.annotation_fn = annotation_fn
        self.transformer_fn = transformer_fn
        self.loader_fn = loader
        self.root_dir = root_dir
        self.samples = []

        self.api_client = dataset_client.DataSetClient()
        self.load_meta_info()

    def load_meta_info(self):
        manifest_path = self.parse_index_path()
        self.annotation = Annotation(manifest_path)

    def parse_index_path(self):
        annotation_info = self.api_client.get_annotation_set(self.dataset_id, self.annotation_id)
        manifest_url = annotation_info.get('Result', {}).get('StoragePath')
        manifest_path = os.path.join(self.root_dir, manifest_url.replace("tos://", ''))
        return manifest_path

    def __len__(self):
        return len(self.annotation)

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        data = self.annotation.extract(index)
        s3url = data.get('content')
        annotation = data.get('annotation')
        file_path = os.path.join(self.root_dir, s3url.replace("tos://", ""))
        content = self.loader_fn(file_path)
        if self.transformer_fn is not None:
            content = self.transformer_fn(content)
        if self.annotation_fn is not None:
            annotation = self.annotation_fn(annotation)
        return (content, annotation)

