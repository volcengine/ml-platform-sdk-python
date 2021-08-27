BOE_ENV = 'BOE'
PROD_ENV = 'PROD'

DEFAULT_REGION = 'cn-beijing'
SERVICE_NAME = 'ml_platform'
SERVICE_VERSION = '2021-10-01'

SERVICE_HOSTS = {
    BOE_ENV: 'volcengineapi-boe-escape.byted.org',
    PROD_ENV: 'open.volcengineapi.com',
}

SERVICE_DIRECT_HOSTS = {
    BOE_ENV: '10.228.109.27:30008',
    PROD_ENV: '10.228.109.27:30018',
}

TOS_REGION_ENDPOINT_URLS = {
    BOE_ENV: {
        'cn-north-1': 'http://boe-s3-official-test.volces.com',
        'cn-north-4': 'http://boe-s3-official-test.volces.com',
    },
    PROD_ENV: {
        'cn-qingdao': 'http://tos-s3-cn-qingdao.volces.com',
        'cn-north-1': 'http://tos-s3-cn-qingdao.volces.com',
        'cn-beijing': 'http://tos-s3-cn-beijing.volces.com',
    },
}

PUBLIC_EXAMPLES_TOS_REGION = 'cn-beijing'
PUBLIC_EXAMPLES_TOS_BUCKET = 'mlplatform-public-examples-{}'.format(
    PUBLIC_EXAMPLES_TOS_REGION,
)

DATASET_LOCAL_METADATA_FILENAME = 'local_metadata.manifest'
ENCRYPTED_KEY_ENV_NAME = 'ENCRYPTED_KEY'


def get_public_examples_readonly_bucket():
    return PUBLIC_EXAMPLES_TOS_BUCKET
