import os

from volcengine_ml_platform.util import volce_util

BOE_ENV = "BOE"
PROD_ENV = "PROD"
ONLINE_ENV = "ONLINE"

DEFAULT_REGION = "cn-beijing"
SERVICE_NAME = "ml_platform"
SERVICE_VERSION = "2021-10-01"

SERVICE_HOSTS = {
    BOE_ENV: os.getenv("VOLC_SERVICE_HOST_BOE", "open-boe-stable.volcengineapi.com"),
    PROD_ENV: "open.volcengineapi.com",
    ONLINE_ENV: "open.volcengineapi.com",
}

TOS_REGION_ENDPOINT_URLS = {
    BOE_ENV: {
        "cn-north-1": "http://boe-s3-official-test.volces.com",
        "cn-north-4": "http://boe-s3-official-test.volces.com",
        "cn-guilin-boe": "http://tos-s3-cn-boe.volces.com",
    },
    PROD_ENV: {
        "cn-qingdao": volce_util.get_tos_endpoint("cn-qingdao"),
        "cn-north-1": volce_util.get_tos_endpoint("cn-qingdao"),
        "cn-beijing": volce_util.get_tos_endpoint("cn-beijing"),
    },
    ONLINE_ENV: {
        "cn-qingdao": volce_util.get_tos_endpoint("cn-qingdao"),
        "cn-north-1": volce_util.get_tos_endpoint("cn-qingdao"),
        "cn-beijing": volce_util.get_tos_endpoint("cn-beijing"),
    },
}

PUBLIC_EXAMPLES_TOS_REGION = "cn-beijing"
PUBLIC_EXAMPLES_TOS_BUCKET = "ml-platform-public-examples-{}".format(
    PUBLIC_EXAMPLES_TOS_REGION,
)

DATASET_LOCAL_METADATA_FILENAME = "local_metadata.manifest"
ENCRYPTED_KEY_ENV_NAME = "ENCRYPTED_KEY"

INNER_API_SERVICE_HOST_ENV_NAME = "ML_PLATFORM_HOST"
ACCOUNT_ID_ENV_NAME = "VOLC_ACCOUNT_ID"
USER_ID_ENV_NAME = "VOLC_USER_ID"

MODULE_MODEL_REPO = "modelrepo"
MODULE_DATASET = "dataset"


def get_public_examples_readonly_bucket():
    return PUBLIC_EXAMPLES_TOS_BUCKET
