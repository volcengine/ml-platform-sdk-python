import logging

from volcengine_ml_platform.innerapi.base_client import define_inner_api
from volcengine_ml_platform.innerapi.base_client import InnerApiBaseClient


define_inner_api("InnerGetDataset")
define_inner_api("InnerGetAnnotationSet")


class InnerDatasetClient(InnerApiBaseClient):
    def __init__(self):
        super().__init__()

    def get_dataset(self, dataset_id: str, token: str):
        try:
            body = {"DatasetID": dataset_id}
            res_json = self.common_json_handler(
                api="InnerGetDataset", body=body, token=token
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get datasets info, dataset_id: %s, error: %s",
                dataset_id,
                e,
            )
            raise Exception("get_dataset failed") from e

    def get_annotation_set(self, dataset_id: str, annotation_id: str, token: str):
        try:
            body = {"DatasetID": dataset_id, "AnnotationID": annotation_id}
            res_json = self.common_json_handler(
                api="InnerGetAnnotationSet", body=body, token=token
            )
            return res_json
        except Exception as e:
            logging.error(
                "Failed to get annotation set, dataset_id: %s, annotation_id: %s, error: %s",
                dataset_id,
                annotation_id,
                e,
            )
            raise Exception("get_annotation_set failed") from e
