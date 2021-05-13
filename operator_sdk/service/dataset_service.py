import logging

from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service

from operator_sdk.base import env


class DatasetService(Service):

    def __init__(self, action, name, method):
        config = env.Config()
        self.host = config.get_service_host()
        self.region = config.get_service_region()
        self.service = config.get_service_name()
        self.version = config.get_service_version()
        self.action = action
        self.name = name
        self.method = method
        self.ak = config.get_access_key_id()
        self.sk = config.get_secret_access_key()

        self.service_info = ServiceInfo(
            self.host, {'Accept': 'application/json'},
            Credentials('', '', self.service, self.region), 5, 5)
        self.api_info = {
            self.name:
                ApiInfo(self.method, "/", {
                    "Action": self.action,
                    "Version": self.version
                }, {}, {})
        }
        super(DatasetService, self).__init__(self.service_info,
                                                self.api_info)

    def update(self, action, name, method):
        self.action = action
        self.name = name
        self.method = method

        self.service_info = ServiceInfo(
            self.host, {'Accept': 'application/json'},
            Credentials('', '', self.service, self.region), 5, 5)
        self.api_info = {
            self.name:
                ApiInfo(self.method, "/", {
                    "Action": self.action,
                    "Version": self.version
                }, {}, {})
        }
        super(DatasetService, self).__init__(self.service_info,
                                                self.api_info)

        self.set_ak(self.ak)
        self.set_sk(self.sk)