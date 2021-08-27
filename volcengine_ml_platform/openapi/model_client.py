import logging

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api('DeleteModel')
define_api('ListModels')
define_api('GetModel')
define_api('CreateModel')
define_api('GetModelNextVersion')
define_api('DeleteModelVersion')
define_api('ListModelVersions')
define_api('UpdateModelVersion')
define_api('GetModelVersion')
define_api('UpdateModel')
define_api('CreatePerfJob')
define_api('ListPerfJobs')
define_api('CreatePerfJob')
define_api('ListPerfTasks')
define_api('UpdatePerfTask')
define_api('CancelPerfTask')


class ModelClient(BaseClient):
    def __init__(self):
        super().__init__()

    def create_model(
        self,
        model_name: str,
        model_format: str,
        model_type: str,
        path: str,
        model_id=None,
        description=None,
        tensor_config=None,
        model_metrics=None,
        source_type='TOS',
    ):
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
                    'SourceType': source_type,
                },
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
            res_json = self.common_json_handler(
                api='GetModelNextVersion', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get models next version, model_id: %s, error: %s',
                model_id,
                e,
            )
            raise Exception('get_model_next_version failed') from e

    def list_models(
        self,
        model_name=None,
        model_name_contains=None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
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
            logging.error(
                'Failed to delete models, model_id: %s, error: %s', model_id, e,
            )
            raise Exception('delete_model failed') from e

    def get_model(self, model_id: str):
        """get models with given models id

        Args:
            model_id (str): The unique ID of the Model

        Raises:
            Exception: raise on get model failed

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
            logging.error(
                'Failed to get models, model_id: %s, error: %s', model_id, e,
            )
            raise Exception('Get model failed') from e

    def list_model_versions(
        self,
        model_id: str,
        model_version: int = None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
        """list models versions with given model_id

        Args:
            model_id (str): The unique ID of the Model
            model_version: filter option, the certain ModelVersion of Model. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: raise on list model versions failed

        Returns:
            json response
        """
        body = {
            'ModelID': model_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if model_version:
            body.update({'ModelVersion': model_version})

        try:
            res_json = self.common_json_handler(
                api='ListModelVersions', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to list models versions, model_id: %s, error: %s', model_id, e,
            )
            raise Exception('List model versions failed') from e

    def get_model_version(self, model_version_id: str):
        """get certain version of a models

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: raise on get model version failed

        Returns:
            json response
        """
        body = {'ModelVersionID': model_version_id}

        try:
            res_json = self.common_json_handler(
                api='GetModelVersion', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get models version, model_version_id: %s, error: %s',
                model_version_id,
                e,
            )
            raise Exception('Get model version failed') from e

    def delete_model_version(self, model_version_id: str):
        """delete certain version of a models

        Args:
            model_version_id (str): The unique ID of the ModelVersion

        Raises:
            Exception: raise on delete model version failed

        Returns:
            json response
        """
        body = {'ModelVersionID': model_version_id}

        try:
            res_json = self.common_json_handler(
                api='DeleteModelVersion', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to delete models version, model_version_id: %s, error: %s',
                model_version_id,
                e,
            )
            raise Exception('Delete model version failed') from e

    def update_model_version(
        self,
        model_version_id: str,
        description=None,
        tensor_config=None,
        model_metrics=None,
    ):
        """update models version

        Args:
            model_version_id (str): The unique ID of the ModelVersion
            description (str, optional): New Description of the ModelVersion. Defaults to None.
            tensor_config (dict, optional): tensor config of the model.
            model_metrics (list, optional): list of models metrics.

        Raises:
            Exception: raise on update model version failed

        Returns:
            json response
        """
        body = {
            'ModelVersionID': model_version_id,
        }
        if description is not None:
            body.update({'Description': description})

        if tensor_config is not None:
            body.update({'TensorConfig': tensor_config})

        if model_metrics is not None:
            body.update({'MetricsList': model_metrics})
        try:
            res_json = self.common_json_handler(
                api='UpdateModelVersion', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to update model version, model_version_id: %s, error: %s',
                model_version_id,
                e,
            )
            raise Exception('Update model version failed') from e

    def update_model(self, model_id: str, model_name=None):
        """update model_name with given model_id

        Args:
            model_id (str, required): The unique ID of the Model
            model_name(str, optional): New ModelName of the Model. Defaults to None.

        Raises:
            Exception: raise on update model failed

        Returns:
            json response
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
            logging.error(
                'Failed to update models, model_id: %s, error: %s', model_id, e,
            )
            raise Exception('Update model failed') from e

    def create_perf_job(
        self,
        model_version_id: str,
        tensor_config: dict,
        job_type: str,
        job_params: list,
    ):
        """create perf job

        Args:
            model_version_id (str, required): The unique ID of the model version
            tensor_config (dict, required): tensor config of the perf job
            job_type (str, required): type of the job, e.g., PERF_ONLY, CONVERT_PERF
            job_params (list, required): parameters to run the job

        Raises:
            Exception: raise on create perf job failed

        Returns:
            json response
        """
        body = {
            'ModelVersionID': model_version_id,
            'TensorConfig': tensor_config,
            'JobType': job_type,
            'JobParamsList': job_params,
        }

        try:
            res_json = self.common_json_handler(api='CreatePerfJob', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to create perf job, model_version_id: %s, error: %s',
                model_version_id,
                e,
            )
            raise Exception('Create perf job failed') from e

    def list_perf_jobs(
        self,
        model_version_id=None,
        job_id=None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
        """list perf jobs

        Args:
            model_version_id (str, optional): The unique ID of the model version.
            job_id (str, optional): The unique ID of the perf job.
            offset (int, optional): offset of database. Defaults to None.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: raise on list perf jobs failed

        Returns:
            json response
        """
        body = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if model_version_id:
            body.update({'ModelVersionID': model_version_id})

        if job_id:
            body.update({'JobID': job_id})

        try:
            res_json = self.common_json_handler(api='ListPerfJobs', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list perf jobs, error: %s', e)
            raise Exception('List perf jobs failed') from e

    def cancel_perf_job(self, job_id: str):
        """cancel a perf job, including all of its tasks

        Args:
            job_id (str, required): The unique ID of the perf job.

        Raises:
            Exception: raise on cancel perf job failed

        Returns:
            json response
        """
        body = {
            'JobID': job_id,
        }

        try:
            res_json = self.common_json_handler(api='CancelPerfJob', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to cancel perf job, error: %s', e)
            raise Exception('Cancel perf job failed') from e

    def list_perf_tasks(
        self,
        task_id=None,
        job_id=None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
        """list perf tasks

        Args:
            task_id (str, optional): The unique ID of the perf task.
            job_id (str, optional): The unique ID of the perf job.
            offset (int, optional): offset of database. Defaults to None.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: raise on list perf tasks failed

        Returns:
            json response
        """
        body = {
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }
        if task_id:
            body.update({'TaskID': task_id})

        if job_id:
            body.update({'JobID': job_id})

        try:
            res_json = self.common_json_handler(api='ListPerfTasks', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list perf tasks, error: %s', e)
            raise Exception('List perf tasks failed') from e

    def update_perf_task(self, task_id: str, task_status=None):
        """update perf task

        Args:
            task_id (str, required): The unique ID of the task
            task_status(str, optional): Status to update. Defaults to None.

        Raises:
            Exception: raise on update perf task failed

        Returns:
            json response
        """
        body = {
            'TaskID': task_id,
        }
        if task_status is not None:
            body.update({'Status': task_status})
        try:
            res_json = self.common_json_handler(
                api='UpdatePerfTask', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to update task, task_id: %s, error: %s', task_id, e,
            )
            raise Exception('Update perf task failed') from e

    def cancel_perf_task(self, task_id: str):
        """cancel a perf task
        Args:
            task_id (str, required): The unique ID of the perf job.

        Raises:
            Exception: raise on cancel perf task failed

        Returns:
            json response
        """
        body = {
            'TaskID': task_id,
        }

        try:
            res_json = self.common_json_handler(
                api='CancelPerfTask', body=body,
            )
            return res_json
        except Exception as e:
            logging.error('Failed to cancel perf task, error: %s', e)
            raise Exception('Cancel perf task failed') from e
