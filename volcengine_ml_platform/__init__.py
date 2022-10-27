import configparser
import os
from typing import Optional

from volcengine import Credentials

from volcengine_ml_platform import constant


def init(
    ak=None,
    sk=None,
    region=None,
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

def get_inner_api_token():
    return EnvHolder.get_inner_api_token()


def get_encrypted_key():
    return os.getenv(constant.ENCRYPTED_KEY_ENV_NAME)


def get_env_name():
    return EnvHolder.ENV_NAME.upper()


def get_stress_env():
    return EnvHolder.STRESS_ENV


def get_mlplatform_env():
    return EnvHolder.MLPLATFORM_ENV


def get_session_token():
    return EnvHolder.SESSION_TOKEN

def get_inner_api_service_host():
    return os.getenv(constant.INNER_API_SERVICE_HOST_ENV_NAME)



class EnvHolder:
    ENV_NAME = constant.PROD_ENV
    STRESS_ENV = os.environ.get("x-mlplatform-stress", "")
    MLPLATFORM_ENV = os.environ.get("x-mlplatform-env", "")
    GLOBAL_CREDENTIALS = None
    INNER_API_TOKEN = None
    SESSION_TOKEN: Optional[str] = None

    @classmethod
    def init(cls, ak, sk, region, env_name, init_aws_env):
        config = configparser.ConfigParser()
        credentials = configparser.ConfigParser()
        if os.environ.get("HOME", None) is not None:
            config_path = os.environ["HOME"] + "/.volc/config"
            credentials_path = os.environ["HOME"] + "/.volc/credentials"
            # config 和 credentials 为 ini 格式
            if os.path.isfile(config_path):
                config = configparser.ConfigParser()
                config.read(config_path)
            if os.path.isfile(credentials_path):
                credentials = configparser.ConfigParser()
                credentials.read(credentials_path)

        default_section, ml_platform_section = "default", "ml_platform"
        ak_option, sk_option, region_option, env_option = (
            "access_key_id",
            "secret_access_key",
            "region",
            "env",
        )
        conf_ak, conf_sk, conf_region = None, None, None
        if config.has_section(default_section):
            if config.has_option(default_section, region_option):
                conf_region = config.get(default_section, region_option)
        if credentials.has_section(default_section):
            if credentials.has_option(default_section, ak_option):
                conf_ak = credentials.get(default_section, ak_option)
            if credentials.has_option(default_section, sk_option):
                conf_sk = credentials.get(default_section, sk_option)

        final_ak = cls.pickup_non_blank_value(
            ak,
            os.environ.get("VOLC_ACCESSKEY", None),
            conf_ak,
        )
        final_sk = cls.pickup_non_blank_value(
            sk,
            os.environ.get("VOLC_SECRETKEY", None),
            conf_sk,
        )
        final_region = cls.pickup_non_blank_value(
            region,
            os.environ.get("VOLC_REGION", None),
            conf_region,
        )
        ml_platform_conf_env = None
        if config.has_section(ml_platform_section):
            if config.has_option(ml_platform_section, env_option):
                ml_platform_conf_env = config.get(
                    ml_platform_section, env_option)
        final_env_name = cls.pickup_non_blank_value(
            env_name,
            os.environ.get("VOLC_ML_PLATFORM_ENV", None),
            ml_platform_conf_env,
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
    def init_inner_token(cls):
        token_path = "/root/.volc/access_token"
        if os.path.isfile(token_path):
            with open(token_path,"r") as f:
                cls.INNER_API_TOKEN = f.read()
    
    @classmethod
    def get_credentials(cls):
        if cls.GLOBAL_CREDENTIALS is None:
            cls.init(None, None, None, None, True)
        return cls.GLOBAL_CREDENTIALS
    
    @classmethod
    def get_inner_api_token(cls):
        if cls.INNER_API_TOKEN is None:
            cls.init_inner_token()
        return cls.INNER_API_TOKEN

    @classmethod
    def pickup_non_blank_value(cls, *args):
        for arg in args:
            if arg is not None and len(arg.strip()) > 0:
                return arg.strip()
        return ""
