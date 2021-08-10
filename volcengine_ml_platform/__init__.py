# -*- coding: utf-8 -*-

from volcengine_ml_platform import initializer
from volcengine_ml_platform.modelrepo.models import Model
from volcengine_ml_platform.datasets import (
    VideoDataset,
    ImageDataset,
    TextDataset,
    TabularDataset,
)

init = initializer.global_config.init

__all__ = (
    'init',
    'Model',
    'VideoDataset',
    'ImageDataset',
    'TextDataset',
    'TabularDataset',
)
