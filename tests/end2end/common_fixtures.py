# -*- coding: utf-8 -*-
import json

import pytest

from samples.mnist import tf_mnist
from volcengine_ml_platform.models import model


@pytest.fixture(scope="session")
def tf_mnist_model():
    tf_mnist.main()
    tf_model = model.Model(local_path=tf_mnist.get_saved_path())
    tf_model.register(model_name='tensorflow-minist-model1',
                      model_format='SavedModel',
                      model_type='TensorFlow:2.4',
                      description='tensorflow-minist-model_description')
    yield tf_model
    # tf_model.unregister()
    tf_mnist.CACHE_DIR.clear()


def get_tensor_config():
    config = {
        "Inputs": [{
            "TensorName": "input_ids_1:0",
            "Dtype": "INT32",
            "Shape": {
                "MaxShape": [8, 256],
                "MinShape": [1, 256]
            }
        }, {
            "TensorName": "input_mask_1:0",
            "Dtype": "INT32",
            "Shape": {
                "MaxShape": [8, 256],
                "MinShape": [1, 256]
            }
        }, {
            "TensorName": "segment_ids_1:0",
            "Dtype": "INT32",
            "Shape": {
                "MaxShape": [8, 256],
                "MinShape": [1, 256]
            }
        }]
    }
    return json.dumps(config)
