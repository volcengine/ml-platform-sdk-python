import logging

from volcengine_ml_platform.openapi.base_client import BaseClient
from volcengine_ml_platform.openapi.base_client import define_api

define_api('CreateResource')
define_api('GetResource')
define_api('DeleteResource')
define_api('ListResource')


class ResourceClient(BaseClient):
    def __init__(self):
        super().__init__()

    def create_resource(
        self,
        name: str,
        resource_type: str,
        v_cpu: float,
        memory: str,
        gpu_type: str,
        gpu_num: float,
        price: float,
        region: str,
    ):
        """create resource

        Args:
            name (str): resource name
            resource_type : The type of resource
            v_cpu (str): The cpu num of resource
            memory (str): resource memory
            gpu_type (str): The gpu type of resource
            gpu_num (float): The gpu num of resource
            price (float): resource price
            region (str): The region of resource

        Raises:
            Exception: create_resource failed

        Returns:
            json response
        """
        body = {
            'Name': name,
            'Type': resource_type,
            'vCPU': v_cpu,
            'Memory': memory,
            'GPUType': gpu_type,
            'GPUNum': gpu_num,
            'Price': price,
            'Region': region,
        }

        try:
            res_json = self.common_json_handler('CreateResource', body)
            return res_json
        except Exception as e:
            logging.error('Failed to create resource, error: %s', e)
            raise Exception('create_resource failed') from e

    def get_resource(self, flavor_id: str):
        """get resource with given flavor_id

        Args:
            flavor_id (str): The unique ID of the Resource

        Raises:
            Exception: raise on get_resource failed

        Returns:
            json response
        """
        body = {'FlavorID': flavor_id}

        try:
            res_json = self.common_json_handler(api='GetResource', body=body)
            return res_json
        except Exception as e:
            logging.error(
                'Failed to get resource info, flavor_id: %s, error: %s', flavor_id, e,
            )
            raise Exception('get_resource failed') from e

    def delete_resource(self, flavor_id: str):
        """delete resource with given flavor id

        Args:
            flavor_id (str): The unique ID of the Resource

        Raises:
            Exception: raise on delete_resource failed

        Returns:
            json response
        """
        body = {'FlavorID': flavor_id}

        try:
            res_json = self.common_json_handler(
                api='DeleteResource', body=body,
            )
            return res_json
        except Exception as e:
            logging.error(
                'Failed to delete resource, flavor_id: %s, error: %s', flavor_id, e,
            )
            raise Exception('delete_resource failed') from e

    def list_resource(
        self,
        name=None,
        name_contains=None,
        resource_type=None,
        tag: list = None,
        offset=0,
        page_size=10,
        sort_by='CreateTime',
        sort_order='Descend',
    ):
        """list resource with given service_id

        Args:
            name (str, optional): resource name
            name_contains (str, optional): filter option, check if
                                resource name contains given string. Defaults to None.
            resource_type (str, optional): filter option, check if
                                resource type equals to given string. Defaults to None.
            tag (list, optional): filter option, check if
                                resource tag in given list. Defaults to None.
            offset (int, optional): offset of database. Defaults to 0.
            page_size (int, optional): number of results to fetch. Defaults to 10.
            sort_by (str, optional): sort by 'ResourceName' or 'CreateTime'. Defaults to 'CreateTime'.
            sort_order (str, optional): 'Ascend' or 'Descend'. Defaults to 'Descend'.

        Raises:
            Exception: list_resource failed

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
        if resource_type:
            body.update({'Type': resource_type})
        if tag:
            body.update({'Tag': tag})

        try:
            res_json = self.common_json_handler(api='ListResource', body=body)
            return res_json
        except Exception as e:
            logging.error('Failed to list resource, error: %s', e)
            raise Exception('list_resource failed') from e
