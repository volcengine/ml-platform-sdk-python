# coding:utf-8

DATASET_LOCAL_METADATA_FILENAME = 'local_metadata.manifest'
ENCRYPTED_KEY_ENV_NAME = 'ENCRYPTED_KEY'
SERVICE_DIRECT_HOST = '10.228.109.27:30008'

SERVICE_NAME = 'ml_platform'
SERVICE_VERSION = '2021-10-01'
# SERVICE_HOST = 'volcengineapi-boe.byted.org'        # online top
SERVICE_HOST = 'volcengineapi-boe-escape.byted.org'  # boe top
# SERVICE_HOST = 'open.volcengineapi.com'

TOS_REGION_ENDPOINT_URL = {
    'cn-north-1': 'http://boe-s3-official-test.volces.com',
}

ONLINE_TOS_REGION_ENDPOINT_URL = {
    'cn-qingdao': 'http://tos-s3-cn-qingdao.volces.com',
    'cn-north-1': 'http://tos-s3-cn-qingdao.volces.com',
    'cn-beijing': 'http://tos-s3-cn-beijing.volces.com',
    'cn-north-4': 'http://boe-s3-official-test.volces.com'
}
