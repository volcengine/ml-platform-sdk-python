# -*- coding: utf-8 -*-

import logging

from volcengine_ml_platform.openapi.base_client import define_api, BaseClient

define_api("DeleteModel")
define_api("ListModels")
define_api("GetModel")
define_api("CreateModel")
define_api("GetModelNextVersion")
define_api("DeleteModelVersion")
define_api("ListModelVersions")
define_api("UpdateModelVersion")
define_api("GetModelVersion")
define_api("UpdateModel")


class ModelClient(BaseClient):

    def __init__(self):
        super(ModelClient, self).__init__()

    def create_model(self,
                     model_name: str,
                     model_format: str,
                     model_type: str,
                     path: str,
                     model_id=None,
                     description=None,
                     tensor_config=None,
                     model_metrics=None,
                     source_type='TOS'):
        """create models

        Args:
            model_name (str): models's name
            model_format (str): models's format, can be 'SavedModel', 'GraphDef','TorchScript','PTX',
                    'CaffeModel','NetDef','MXNetParams','Scikit_Learn','XGBoost','TensorRT','ONNX',or 'Custom'
            model_type (str): The type of the ModelVersion, examples: 'TensorFlow:2.0'
            path (str): source storage path
            model_id (str, optional): model_id, a new models will be created if not given. Defaults to None.
            description (str, optional): description to the models. Defaults to None.
            tensor_config (dict, optional): tensor config of the models.
            model_metrics (list, optional): list of models metrics.
            source_type (str, optional): storage type. Defaults to 'TOS'.

        Raises:
            Exception: failed to create models

        Returns:
            json response
        """
        try:
            body = {
                'ModelName': model_name,
                'VersionInfo': {
                    'ModelFormat': model_format,
                    'ModelType': model_type,
                    'Path': path,
                    'SourceType': source_type
                }
            }
            if description is not None:
                body['VersionInfo'].update({'Description': description})

            if model_id is not None:
                body.update({'ModelID': model_id})

            if tensor_config is not None:
                body['VersionInfo'].update({'TensorConfig': tensor_config})

            if model_metrics is not None:
                body['VersionInfo'].update({'MetricsList': model_metrics})

            res_json = self.common_json_handler(api='CreateModel', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to create models, error: %s', e)
            raise Exception('create_model failed') from e

    def get_model_next_version(self, model_id=None):
        """get next models version with given model_id

        Args:
            model_id (str, required): The unique ID of the Model. 1 will return if not given

        Returns:
            next_version(int): The next version of the Model
        """

        body = {}
        if model_id:
            body.update({'ModelID': model_id})

        try:
            res_json = self.common_json_handler(api='GetModelNextVersion',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get models next version, model_id: %s, error: %s',
                model_id, e)
            raise Exception('get_model_next_version failed') from e

    def list_models(self,
                    model_name=None,
                    model_name_contains=None,
                    offset=0,
                    page_size=10,
                    sort_by='CreateTime',
                    sort_order='Descend'):
        """list models

        Args:
            model_name (str, optional): certern models with return if given models name. Defaults to None.
            model_name_contains (str, optional): filter option, check if
                                models name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to None.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list models exception

        Returns:
            json response
        """
        body = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if model_name:
            body.update({'ModelName': model_name})

        if model_name_contains:
            body.update({'ModelNameContains': model_name_contains})

        try:
            res_json = self.common_json_handler(api='ListModels', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list models, error: %s', e)
            raise Exception('list_models failed') from e

    def delete_model(self, model_id: str):
        """delete models with given models id

        Args:
            model_id (str): The unique ID of the Model

        Raises:
            Exception: raise on delete_model failed

        Returns:
            json response
        """
        body = {
            'ModelID': model_id,
        }
        try:
            res_json = self.common_json_handler(api='DeleteModel', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to delete models, model_id: %s, error: %s',
                          model_id, e)
            raise Exception('delete_model failed') from e

    def get_model(self, model_id: str):
        """get models with given models id

        Args:
            model_id (str): The unique ID of the Model

        Raises:
            Exception: raise on get_model failed

        Returns:
            json response
        """
        body = {
            'ModelID': model_id,
        }
        try:
            res_json = self.common_json_handler(api='GetModel', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to get models, model_id: %s, error: %s',
                          model_id, e)
            raise Exception('get_model failed') from e

    def list_model_versions(self,
                            model_id: str,
                            model_version: int = None,
                            offset=0,
                            page_size=10,
                            sort_by='CreateTime',
                            sort_order='Descend'):
        """list models versions with given model_id

        Args:
            model_id (str): The unique ID of the Model
            model_version: filter option, the certain ModelVersion of Model. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_model_versions failed

        Returns:
            json response
        """
        body = {
            'ModelID': model_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order
        }
        if model_version:
            body.update({'ModelVersion': model_version})

        try:
            res_json = self.common_json_handler(api='ListModelVersions',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to list models versions, model_id: %s, error: %s',
                model_id, e)
            raise Exception('list_model_versions failed') from e

    def get_model_version(self, model_version_id: str):
        """get certain version of a models

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: get_model_version failed

        Returns:
            json response
        """
        body = {'ModelVersionID': model_version_id}

        try:
            res_json = self.common_json_handler(api='GetModelVersion',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get models version, model_version_id: %s, error: %s',
                model_version_id, e)
            raise Exception('get_model_version failed') from e

    def delete_model_version(self, model_version_id: str):
        """delete certain version of a models

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: delete_model_version failed

        Returns:
            json response
        """
        body = {'ModelVersionID': model_version_id}

        try:
            res_json = self.common_json_handler(api='DeleteModelVersion',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to delete models version, model_version_id: %s, error: %s',
                model_version_id, e)
            raise Exception('delete_model_version failed') from e

    def update_model_version(self, model_version_id, description=None):
        """update models version description

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            description (str, optional): New Description of the ModelVersion. Defaults to None.

        Raises:
            Exception: update_model_version failed

        Returns:
            json response
        """
        body = {
            'ModelVersionID': model_version_id,
        }
        if description is not None:
            body.update({'Description': description})
        try:
            res_json = self.common_json_handler(api='UpdateModelVersion',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to update models version, model_version_id: %s, error: %s',
                model_version_id, e)
            raise Exception('update_model_version failed') from e

    def update_model(self, model_id, model_name=None):
        """update model_name with given model_id

        Args:
            model_id (str, required): The unique ID of the Model
            model_name(str, optional): New ModelName of the Model. Defaults to None.

        Raises:
            Exception: failed to update models

        Returns:
            Dataset: json response
        """
        body = {
            'ModelID': model_id,
        }
        if model_name is not None:
            body.update({'ModelName': model_name})
        try:
            res_json = self.common_json_handler(api='UpdateModel', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to update models, model_id: %s, error: %s',
                          model_id, e)
            raise Exception('update_model failed') from e
