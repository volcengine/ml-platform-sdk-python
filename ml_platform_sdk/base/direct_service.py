import json
from collections import OrderedDict

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from ml_platform_sdk.base.direct_request import DirectRequest


class DirectServiceInfo:

    def __init__(self,
                 host,
                 header,
                 connection_timeout,
                 socket_timeout,
                 scheme='http'):
        self.host = host
        self.header = header
        self.connection_timeout = connection_timeout
        self.socket_timeout = socket_timeout
        self.scheme = scheme


class DirectService:

    def __init__(self, service_info, api_info):
        self.service_info = service_info
        self.api_info = api_info
        self.session = requests.session()

    def set_host(self, host):
        self.service_info.host = host

    def set_scheme(self, scheme):
        self.service_info.scheme = scheme

    def get(self, api, params, doseq=0):
        if api not in self.api_info:
            raise Exception('no such api')
        api_info = self.api_info[api]

        r = self.prepare_request(api_info, params, doseq)

        url = r.build(doseq)
        resp = self.session.get(url,
                                headers=r.headers,
                                timeout=(self.service_info.connection_timeout,
                                         self.service_info.socket_timeout))
        if resp.status_code == 200:
            return resp.text
        raise Exception(resp.text)

    def post(self, api, params, form):
        if api not in self.api_info:
            raise Exception('no such api')
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r.form = self.merge(api_info.form, form)
        r.body = urlencode(r.form, True)

        url = r.build()

        resp = self.session.post(url,
                                 headers=r.headers,
                                 data=r.form,
                                 timeout=(self.service_info.connection_timeout,
                                          self.service_info.socket_timeout))
        if resp.status_code == 200:
            return resp.text
        raise Exception(resp.text)

    def json(self, api, params, body):
        if api not in self.api_info:
            raise Exception('no such api')
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        url = r.build()
        resp = self.session.post(url,
                                 headers=r.headers,
                                 data=r.body,
                                 timeout=(self.service_info.connection_timeout,
                                          self.service_info.socket_timeout))
        if resp.status_code == 200:
            return json.dumps(resp.json())
        raise Exception(resp.text)

    def put(self, url, file_path, headers):
        with open(file_path, 'rb') as f:
            resp = self.session.put(url, headers=headers, data=f)
            if resp.status_code == 200:
                return True, resp.text
            return False, resp.text

    def put_data(self, url, data, headers):
        resp = self.session.put(url, headers=headers, data=data)
        if resp.status_code == 200:
            return True, resp.text
        return False, resp.text

    def prepare_request(self, api_info, params, doseq=0):
        for key in params:
            if isinstance(params[key], (float, int)):
                params[key] = str(params[key])
            elif isinstance(params[key], list):
                if not doseq:
                    params[key] = ','.join(params[key])

        connection_timeout = self.service_info.connection_timeout
        socket_timeout = self.service_info.socket_timeout

        r = DirectRequest()
        r.set_schema(self.service_info.scheme)
        r.set_method(api_info.method)
        r.set_connection_timeout(connection_timeout)
        r.set_socket_timeout(socket_timeout)

        mheaders = self.merge(api_info.header, self.service_info.header)
        mheaders['Host'] = self.service_info.host
        mheaders['User-Agent'] = 'mlplatform-sdk-python'
        r.set_headers(mheaders)

        mquery = self.merge(api_info.query, params)
        r.set_query(mquery)

        r.set_host(self.service_info.host)
        r.set_path(api_info.path)

        return r

    @staticmethod
    def merge(param1, param2):
        od = OrderedDict()
        for key in param1:
            od[key] = param1[key]

        for key in param2:
            od[key] = param2[key]

        return od
