# -*- coding: utf-8 -*-
import logging
from typing import Optional

from volcengine_ml_platform.openapi.base_client import define_api, BaseClient

define_api("UpdateService")
define_api("CreateService")
define_api("UpdateServiceVersionDescription")
define_api("ListServiceImages")
define_api("ListServices")
define_api("StopService")
define_api("ListServiceVersions")
define_api("StartService")
define_api("DeleteService")
define_api("GetService")
define_api("RollbackServiceVersion")
define_api("ListModelServiceInstances")
define_api("GetModelServiceInstanceStatus")
define_api("ModifyService")


class InferenceServiceClient(BaseClient):

    def __init__(self):
        super(InferenceServiceClient, self).__init__()

    def create_service(self,
                       service_name: str,
                       model_name: str,
                       model_id: str,
                       model_version_id: str,
                       image_url: str,
                       flavor_id: str,
                       envs: list,
                       model_version: Optional[int] = None,
                       model_path: Optional[str] = None,
                       model_type: Optional[str] = None,
                       replica: Optional[int] = 1,
                       cluster_id: Optional[str] = 'cc3gpncvqtofppg3tqam0',
                       description: Optional[str] = None) -> dict:
        """create inference service for models

        Args:
            service_name (str): service name
            models (Model): Model object
            image_url (str): container image url
            flavor_id (str): hardward standard id
            envs (list): environment variables
            replica (int, optional): replica number. Defaults to 1.
            description (str, optional): description of service. Defaults to None.

        Raises:
            Exception: create_service failed

        Returns:
            json response
        """
        try:
            body = {
                'ServiceName': service_name,
                'ClusterID': cluster_id,
                'ServiceDeployment': {
                    'Replicas': replica,
                    'FlavorID': flavor_id,
                    'Model': {
                        'ModelID': model_id,
                        'ModelVersionID': model_version_id,
                        'Name': model_name,
                        'Version': model_version,
                        'Path': model_path,
                        'Type': model_type,
                    },
                    'Image': {
                        'URL': image_url,
                    },
                    'Envs': envs
                }
            }
            if description is not None:
                body['ServiceDeployment'].update({'Description': description})
            res_json = self.common_json_handler(api='CreateService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to create service, error: %s', e)
            raise Exception('create_service failed') from e

    def modify_service(self, service_name: str, service_id: str,
                       cluster_id: str):
        """Modify ServiceName with given ServiceID and ClusterID

        Args:
            service_name(str, required): New Name of the Service
            service_id (str, required): The unique ID of the Service
            cluster_id (str, required): The unique ID of the Cluster

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            'ServiceName': service_name,
            'ServiceID': service_id,
            'ClusterID': cluster_id
        }
        try:
            res_json = self.common_json_handler("ModifyService", body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to modify service, service_id: %s, cluster_id: %s, error: %s',
                service_id, cluster_id, e)
            raise Exception('modify_service failed') from e

    def delete_service(self, service_id: str) -> dict:
        """delete service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: delete_service failed

        Returns:
            json response
        """
        body = {'ServiceID': service_id}
        try:
            res_json = self.common_json_handler(api='DeleteService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to delete service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('delete_service failed') from e

    def start_service(self, service_id: str) -> dict:
        """start service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: start_service failed

        Returns:
            json response
        """
        body = {'ServiceID': service_id}
        try:
            res_json = self.common_json_handler(api='StartService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to start service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('start_service failed') from e

    def stop_service(self, service_id: str) -> dict:
        """stop service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: stop_service failed

        Returns:
            json response
        """
        body = {'ServiceID': service_id}
        try:
            res_json = self.common_json_handler(api='StopService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to stop service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('stop_service failed') from e

    def scale_service(self, service_id: str, replicas: int,
                      flavor_id: str) -> dict:
        """scale service by changing the number of replicas

        Args:
            service_id (str): service id
            replicas (int): number of replicas
            flavor_id (str): hardware standard

        Raises:
            Exception: scale_service failed

        Returns:
            json response
        """
        change_type = 'ScalingService'

        try:
            body = {
                'ServiceID': service_id,
                'Replicas': replicas,
                'FlavorID': flavor_id,
                'ChangeType': change_type
            }

            res_json = self.common_json_handler(api='UpdateService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to scale service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('scale_service failed') from e

    def update_service(
        self,
        service_id: str,
        replicas: int,
        flavor_id: str,
        model_id: str,
        model_version_id: str,
        img_url: str,
        envs: list,
        change_type: str,
        img_description: str = None,
        img_version: str = None,
        img_type: str = None,
        service_description: str = None,
        model_name: str = None,
        model_version: int = None,
        model_type: str = None,
        model_path: str = None,
    ):
        body = {
            'ServiceID': service_id,
            'Replicas': replicas,
            'FlavorID': flavor_id,
            'Model': {
                'ModelID': model_id,
                'ModelVersionID': model_version_id,
            },
            'Image': {
                'URL': img_url,
            },
            'Envs': envs,
            'ChangeType': change_type
        }
        if service_description:
            body.update({'Description': service_description})
        if model_name:
            body['Model'].update({'Name': model_name})
        if model_version:
            body['Model'].update({'Version': model_version})
        if model_type:
            body['Model'].update({'Type': model_type})
        if model_path:
            body['Model'].update({'Path': model_path})

        if img_description:
            body['Image'].update({'Description': img_description})
        if img_version:
            body['Image'].update({'Version': img_version})
        if img_type:
            body['Image'].update({'Type': img_type})
        try:
            res_json = self.common_json_handler(api='UpdateService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to update service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('update_service failed') from e

    # TODO
    def update_service_version_description(self):
        pass

    def get_service(self, service_id: str):
        """get service with given service_id

        Args:
            service_id (str): The unique ID of the Service

        Raises:
            Exception: raise on get_service failed

        Returns:
            json response
        """
        body = {'ServiceID': service_id}
        try:
            res_json = self.common_json_handler(api='GetService', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to get service, service_id: %s, error: %s',
                          service_id, e)
            raise Exception('get_service failed') from e

    def list_service_images(self,
                            model_id: str,
                            model_version_id: str,
                            name: str = None,
                            version: int = None,
                            service_type: str = None,
                            path: str = None):
        body = {'ModelID': model_id, 'ModelVersionID': model_version_id}
        if name:
            body.update({'Name': name})
        if version:
            body.update({'Version': version})
        if service_type:
            body.update({'Type': service_type})
        if path:
            body.update({'Path': path})

        try:
            res_json = self.common_json_handler(api='ListServiceImages',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list service images, error: %s', e)
            raise Exception('list_service_images failed') from e

    def list_services(self,
                      service_name: str = None,
                      service_name_contains: str = None,
                      offset=0,
                      page_size=10,
                      sort_by='CreateTime',
                      sort_order='Descend'):
        """list services

        Args:
            service_name (str, optional): service name
            service_name_contains (str, optional): filter option, check if
                                service name contains given string. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServicelName' or 'CreateTime'. Defaults to 'CreateTime'.
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
        if service_name:
            body.update({'ServiceName': service_name})
        if service_name_contains:
            body.update({'ServiceNameContains': service_name_contains})

        try:
            res_json = self.common_json_handler(api='ListServices', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list services, error: %s', e)
            raise Exception('list_services failed') from e

    def list_service_versions(self,
                              service_id: str,
                              offset=0,
                              page_size=10,
                              sort_by='CreateTime',
                              sort_order='Descend'):
        """list service versions with given service_id

        Args:
            service_id (str): The unique ID of the Service
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ServiceVersion' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_service_versions failed

        Returns:
            json response
        """
        body = {
            'ServiceID': service_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }

        try:
            res_json = self.common_json_handler(api='ListServiceVersions',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to list service versions, service_id: %s, error: %s',
                service_id, e)
            raise Exception('list_service_versions failed') from e

    def rollback_service_version(self, service_id: str,
                                 service_version_id: str):
        """Rollback a ServiceVersion with ServiceID and ServiceVersionID

        Args:
            service_id (str, required): The unique ID of the Service
            service_version_id(str, required): The unique ID of the ServiceVersion

        Raises:
            Exception: failed to rollback service version

        Returns:
            Dataset: json response
        """
        body = {'ServiceID': service_id, 'ServiceVersionID': service_version_id}
        try:
            res_json = self.common_json_handler(api='RollbackServiceVersion',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to rollback service version, service_id: %s, service_version_id: %s, error: %s',
                service_id, service_version_id, e)
            raise Exception('rollback_service_version failed') from e

    def list_model_service_instances(self,
                                     service_id: str,
                                     offset=0,
                                     page_size=10,
                                     sort_by='CreateTime',
                                     sort_order='Descend'):
        """list models service instances

        Args:
            service_id (str, optional): The unique ID of Service
            offset (int, optional): offset of service. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ModelServiceInstanceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list datasets exception

        Returns:
            json response
        """
        body = {
            'ServiceID': service_id,
            'Offset': offset,
            'Limit': page_size,
            'SortBy': sort_by,
            'SortOrder': sort_order,
        }

        try:
            res_json = self.common_json_handler(api='ListModelServiceInstances',
                                                body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to list models service instances, service_id: %s, error: %s',
                service_id, e)
            raise Exception('list_model_service_instances failed') from e

    def get_model_service_instance_status(self, service_id: str,
                                          instance_id_list: list):
        """get the status of models service instance

        Args:
            service_id (str, required): The unique ID of Service
            offset (list, required): instance id list

        Raises:
            Exception: get models service instance status exception

        Returns:
            json response
        """
        body = {'ServiceID': service_id, 'InstanceIDList': instance_id_list}

        try:
            res_json = self.common_json_handler(
                api='GetModelServiceInstanceStatus', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get models service instance status, service_id: %s, error: %s',
                service_id, e)
            raise Exception('get_model_service_instance_status failed') from e
