import logging
from typing import Dict
from typing import Union

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api('CreateDataset')
define_api('UpdateDataset')
define_api('GetDataset')
define_api('DeleteDataset')
define_api('ListDatasets')
define_api('ListAnnotationSets')
define_api('UpdateAnnotationLabel')
define_api('GetAnnotationSet')
define_api('DeleteAnnotationSet')
define_api('CreateAnnotaionSet')
define_api('UpdateAnnotationData')
define_api('ListAnnotationDatas')
define_api('TryDeleteAnnotationLabel')
define_api('ListAnnotationLabel')


class DataSetClient(BaseClient):
    def __init__(self):
        super().__init__()

    def create_dataset(self, body):
        try:
            res_json = self.common_json_handler('CreateDataset', body)
            return res_json
        except Exception as e:
            logging.error('Failed to create datasets, error: %s', e)
            raise Exception('create_dataset failed') from e

    def update_dataset(self, body):
        try:
            res_json = self.common_json_handler('UpdateDataset', body)
            return res_json
        except Exception as e:
            logging.error('Failed to update datasets, error: %s', e)
            raise Exception('update_dataset failed') from e

    def get_dataset(self, dataset_id):
        """Get a Dataset.

        Args:
            dataset_id (str, required): The unique ID of the Dataset
        Raises:
            Exception: failed to get dataset
        Returns:
            Dataset: json response

        """
        body = {'DatasetID': dataset_id}
        try:
            res_json = self.common_json_handler(api='GetDataset', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get datasets info, dataset_id: %s, error: %s', dataset_id, e,
            )
            raise Exception('get_dataset failed') from e

    def delete_dataset(self, dataset_id: str):
        """Delete a Dataset.

        Args:
            dataset_id (str, required): The unique ID of the Dataset
        Raises:
            Exception: failed to delete dataset
        Returns:
            Dataset: json response

        """
        body = {'DatasetID': dataset_id}
        try:
            res_json = self.common_json_handler(api='DeleteDataset', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to delete dataset, dataset_id: %s, error: %s', dataset_id, e,
            )
            raise Exception('delete_dataset failed') from e

    def list_datasets(
        self,
        name=None,
        name_contains=None,
        status=None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
        """list datasets

        Args:
            name (str, optional): dataset name
            name_contains (str, optional): filter option, check if
                                dataset name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'DatasetlName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if name:
            body.update({'Name': name})
        if name_contains:
            body.update({'NameContains': name_contains})
        if status:
            body.update({'Status': status})

        try:
            res_json = self.common_json_handler(api='ListDatasets', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list datasets, error: %s', e)
            raise Exception('list_datasets failed') from e

    def list_annotation_sets(self, dataset_id: str):
        """list annotation set with given dataset_id

        Args:
            dataset_id (str): The unique ID of Dataset

        Raises:
            Exception: list annotation sets exception

        Returns:
            json response
        """
        body = {'DatasetID': dataset_id}

        try:
            res_json = self.common_json_handler(
                api='ListAnnotationSets', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to list annotation sets, dataset_id: %s, error: %s',
                dataset_id,
                e,
            )
            raise Exception('list_annotation_sets failed') from e

    def update_annotation_label(
        self, annotation_id: str, labels: list, default_label=None,
    ):
        body = {
            'AnnotationID': annotation_id,
            'Labels': labels,
        }
        if default_label:
            body.update({'DefaultLabel': default_label})

        try:
            res_json = self.common_json_handler('UpdateAnnotationLabel', body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to update annotation label, annotation_id: %s, error: %s',
                annotation_id,
                e,
            )
            raise Exception('update_annotation_label failed') from e

    def get_annotation_set(self, dataset_id: str, annotation_id: str):
        """get annotation with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: failed to get annotation

        Returns:
            json response
        """
        body = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res_json = self.common_json_handler(
                api='GetAnnotationSet', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get annotation set, dataset_id: %s, annotation_id: %s, error: %s',
                dataset_id,
                annotation_id,
                e,
            )
            raise Exception('get_annotation_set failed') from e

    def delete_annotation_set(self, dataset_id: str, annotation_id: str):
        """delete annotation set with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: delete_annotation_set failed

        Returns:
            json response
        """
        body = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res_json = self.common_json_handler(
                api='DeleteAnnotationSet', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to delete annotation set, dataset_id: %s, annotation_id: %s, error: %s',
                dataset_id,
                annotation_id,
                e,
            )
            raise Exception('delete_annotation_set failed') from e

    def create_annotation_set(
        self,
        dataset_id: str,
        annotation_type: str,
        annotation_name: str,
        default_label: str = None,
        labels: list = None,
    ):
        """create annotation for dataset

        Args:
            dataset_id (str): The unique ID of Dataset
            annotation_type (Model): annotation type
            annotation_name (str): annotation name
            default_label (str, optional): default label of annotataion. Defaults fo None
            labels (list): labels of annotataion. Defaults fo None

        Raises:
            Exception: create_annotation_set failed

        Returns:
            json response
        """
        body: Dict[str, Union[str, int, list]] = {
            'DatasetID': dataset_id,
            'AnnotationType': annotation_type,
            'AnnotationName': annotation_name,
        }
        if default_label:
            body.update({'DefaultLabel': default_label})
        if labels:
            body.update({'Labels': labels})

        try:
            res_json = self.common_json_handler('CreateAnnotataionSet', body)
            return res_json
        except Exception as e:
            logging.error('Failed to create annotation set, error: %s', e)
            raise Exception('create_annotation_set failed') from e

    def update_annotation_data(self, annotation_id: str, datas: list):
        """update annotation_data with given annotation_id

        Args:
            annotation_id (str, required): The unique ID of the Annotation
            datas(str, required): New datas of the Annotation.

        Raises:
            Exception: failed to update annotataion_data

        Returns:
            Dataset: json response

        """
        body = {'AnnotationID': annotation_id, 'Datas': datas}

        try:
            res_json = self.common_json_handler('UpdateAnnotationData', body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to update annotation data, annotation_id: %s, error: %s',
                annotation_id,
                e,
            )
            raise Exception('update_annotation_data failed') from e

    def list_annotation_datas(
        self,
        annotation_id: str,
        label_names: list = None,
        status: int = None,
        offset=0,
        page_size=10,
    ):
        """list annotation datas with given annotation_id

        Args:
            annotation_id (str): The unique ID of annotation
            label_names (list, optional): filter option, label_names. Defaults to None.
            status (str, optional): filter option, status.Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.

        Raises:
            Exception: list_annotation_datas failed

        Returns:
            json response
        """
        body = {
            'AnnotationID': annotation_id,
            'Offset': offset,
            'Limit': page_size,
        }
        if status:
            body.update({'Status': status})
        if label_names:
            body.update({'LabelNames': label_names})

        try:
            res_json = self.common_json_handler(
                api='ListAnnotationDatas', body=body,
            )
            return res_json
        except Exception as e:
            logging.error('Failed to list annotation datas, error: %s', e)
            raise Exception('list_annotation_datas failed') from e

    def try_delete_annotation_label(self, annotation_id: str, label: object):
        body = {'AnnotationID': annotation_id, 'Label': label}

        try:
            res_json = self.common_json_handler(
                'TryDeleteAnnotationLabel', body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to try delete annotation label, annotation_id: %s, error: %s',
                annotation_id,
                e,
            )
            raise Exception('try_delete_annotation_label failed') from e

    def list_annotation_label(self, dataset_id: str, annotation_id: str):
        """list annotation label set with given dataset_id and annotation_id

        Args:
            dataset_id (str, required): The unique ID of the Dataset.
            annotation_id (str, required): The unique ID of the Annotation.

        Raises:
            Exception: list_annotation_label failed

        Returns:
            json response

        """
        body = {'DatasetID': dataset_id, 'AnnotationID': annotation_id}

        try:
            res_json = self.common_json_handler(
                api='ListAnnotationLabel', body=body,
            )
            return res_json
        except Exception as e:
            logging.error('Failed to list annotation label, error: %s', e)
            raise Exception('list_annotation_label failed') from e
