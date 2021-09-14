import json
import os

from volcengine import Credentials

from volcengine_ml_platform import constant


def init(
    ak=None,
    sk=None,
    region=constant.DEFAULT_REGION,
    env_name=None,
    init_aws_env=True,
):
    EnvHolder.init(ak, sk, region, env_name, init_aws_env)


def mark_stress(flag=None):
    EnvHolder.STRESS_FLAG = flag


def set_session_token(token):
    EnvHolder.SESSION_TOKEN = token


def get_tos_endpoint_url():
    return constant.TOS_REGION_ENDPOINT_URLS[get_env_name()][
        EnvHolder.get_credentials().region
    ]


def get_service_host():
    return constant.SERVICE_HOSTS[get_env_name()]


def get_service_name():
    return constant.SERVICE_NAME


def get_credentials():
    return EnvHolder.get_credentials()


def get_encrypted_key():
    return os.getenv(constant.ENCRYPTED_KEY_ENV_NAME)


def get_env_name():
    return EnvHolder.ENV_NAME.upper()


def get_stress_flag():
    return EnvHolder.STRESS_FLAG.upper()


def get_session_token():
    return EnvHolder.SESSION_TOKEN


class EnvHolder:
    ENV_NAME = constant.PROD_ENV
    STRESS_FLAG = os.environ.get("VOLC_ML_PLATFORM_STRESS", "")
    GLOBAL_CREDENTIALS = None
    SESSION_TOKEN: str = None

    @classmethod
    def init(cls, ak, sk, region, env_name, init_aws_env):
        conf = {}
        if os.environ.get("HOME", None) is not None:
            path = os.environ["HOME"] + "/.volc/config"
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    conf = json.load(f)

        final_ak = cls.pickup_non_blank_value(
            os.environ.get("VOLC_ACCESSKEY", None),
            conf.get("ak", None),
            ak,
        )
        final_sk = cls.pickup_non_blank_value(
            os.environ.get("VOLC_SECRETKEY", None),
            conf.get("sk", None),
            sk,
        )
        final_region = cls.pickup_non_blank_value(
            os.environ.get("VOLC_REGION", None),
            conf.get(
                "region",
                None,
            ),
            region,
        )
        ml_platform_conf = conf.get("ml_platform", {})
        final_env_name = cls.pickup_non_blank_value(
            os.environ.get("VOLC_ML_PLATFORM_ENV", None),
            ml_platform_conf.get("env", None),
            env_name,
        )

        if final_env_name is not None and len(final_env_name) > 0:
            EnvHolder.ENV_NAME = final_env_name
        cls.GLOBAL_CREDENTIALS = Credentials.Credentials(
            ak=final_ak,
            sk=final_sk,
            service=constant.SERVICE_NAME,
            region=final_region,
        )
        if init_aws_env is True:
            os.environ["AWS_REGION"] = final_region
            os.environ["AWS_ACCESS_KEY_ID"] = final_ak
            os.environ["AWS_SECRET_ACCESS_KEY"] = final_sk
            os.environ["S3_ENDPOINT"] = get_tos_endpoint_url()

    @classmethod
    def get_credentials(cls):
        if cls.GLOBAL_CREDENTIALS is None:
            cls.init(None, None, constant.DEFAULT_REGION, None, True)
        return cls.GLOBAL_CREDENTIALS

    @classmethod
    def pickup_non_blank_value(cls, *args):
        for arg in args:
            if arg is not None and len(arg.strip()) > 0:
                return arg.strip()
        return ""
