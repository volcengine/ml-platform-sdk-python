import json
import threading

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from ml_platform_sdk.config import config
from ml_platform_sdk.model.model import Model


class InferenceService(Service):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, region='cn-beijing'):
        self.conf = config.Config(region)
        self.service_info = self.get_service_info()
        self.api_info = self.get_api_info()
        self.domain_cache = {}
        self.fallback_domain_weights = {}
        self.update_interval = 10
        self.lock = threading.Lock()
        super(InferenceService, self).__init__(self.service_info, self.api_info)

    def set_ak(self, ak):
        self.conf.set_ak(ak)
        self.service_info.credentials.set_ak(ak)

    def set_sk(self, sk):
        self.conf.set_sk(sk)
        self.service_info.credentials.set_sk(sk)

    def get_service_info(self):
        return ServiceInfo(
            self.conf.get_service_host(), {'Accept': 'application/json'},
            Credentials('', '', self.conf.get_service_name(),
                        self.conf.get_service_region()), 10, 10, 'https')

    def get_api_info(self):
        api_info = {
            'UpdateService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'CreateService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'CreateService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'UpdateServiceVersionDescription':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'UpdateServiceVersionDescription',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListServiceImages':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServiceImages',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListServices':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServices',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'StopService':
                ApiInfo(
                    'POST', '/', {
                        'Action': 'StopService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListServiceVersions':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'ListServiceVersions',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'StartService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'StartService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'DeleteService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'DeleteService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'GetService':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'GetService',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'RollbackServiceVersion':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'ListModelServiceInstances':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
            'GetModelServiceInstanceStatus':
                ApiInfo(
                    'GET', '/', {
                        'Action': 'RollbackServiceVersion',
                        'Version': self.conf.get_service_version()
                    }, {}, {}),
        }
        return api_info

    def create_service(self,
                       service_name: str,
                       model: Model,
                       image_url: str,
                       flavor_id: str,
                       env: list,
                       replica=1,
                       description=None) -> dict:
        """create inference service for model

        Args:
            service_name (str): service name
            model (Model): Model object
            image_url (str): container image url
            flavor_id (str): hardward standard id
            env (list): environment variables
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
                'ServiceDeployment': {
                    'Replicas': replica,
                    'FlavorID': flavor_id,
                    'Model': {
                        'Name': model.model_name,
                        'Version': model.version_info.version_index,
                        'Type': model.version_info.type,
                        'Path': model.version_info.path,
                    },
                    'Image': {
                        'URL': image_url,
                    },
                    'Envs': env
                }
            }
            if description is not None:
                body['ServiceDeployment'].update({'Description': description})

            res = self.json(api='CreateService',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('create_service failed') from e

    def delete_service(self, service_id: str) -> dict:
        """delete service with service id

        Args:
            service_id (str): service unique id

        Raises:
            Exception: delete_service failed

        Returns:
            json response
        """
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='DeleteService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
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
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='StartService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
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
        params = {'ServiceID': service_id}
        try:
            res = self.get(api='StopService', params=params)
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('start_service failed') from e

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

            res = self.json(api='UpdateService',
                            params=dict(),
                            body=json.dumps(body))
            res_json = json.loads(res)
            return res_json
        except Exception as e:
            raise Exception('scale_service failed') from e

    # TODO
    def update_service(self):
        pass

    def update_service_version_description(self):
        pass
