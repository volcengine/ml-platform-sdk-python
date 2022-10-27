
import logging
from volcengine_ml_platform.io.tos import TOSClient
from volcengine_ml_platform.innerapi.tracking.client import Client


__version__ = '0.0.1'

# globals
experiment = None
trial = None
config = None  # trial config
summary = None  # trial summary

tk_cli = Client()
tos_cli = TOSClient()
logger = logging.getLogger('tracking')

tos_bucket, tos_prefix = "", ""


def get_tos_path():
    global tos_bucket, tos_prefix
    if not tos_bucket or not tos_prefix:
        tos_bucket, tos_prefix = tk_cli.get_tos_upload_path(
            [experiment.sid, trial.sid])
    return tos_bucket, tos_prefix


# method
from volcengine_ml_platform.tracking.init import init  # NOQA: E402


def log(*args, **kwargs):
    trial.log(*args, **kwargs)


def define_metric(*args, **kwargs):
    trial.define_metric(*args, **kwargs)


def finish(*args, **kwargs):
    trial.finish(*args, **kwargs)


# data type
from volcengine_ml_platform.tracking.data_types import Image, Table  # NOQA: E402

__all__ = [
    '__version__',
    'init,'
    'config',
    'summary',
    'log',
    'define_metric',
    # data type
    'Image',
    'Table',
]
