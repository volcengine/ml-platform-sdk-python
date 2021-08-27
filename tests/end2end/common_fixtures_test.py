import pytest

from samples.mnist import tf_mnist
from volcengine_ml_platform.models import model


@pytest.fixture(scope='session')
def tf_mnist_model():
    tf_mnist.main()
    tf_model = model.Model()
    resp = tf_model.register(
        model_name='tensorflow-minist-model1',
        model_format='SavedModel',
        model_type='TensorFlow:2.4',
        description='tensorflow-minist-model_description',
        local_path=tf_mnist.get_saved_path(),
    )
    yield resp['Result']
    # tf_model.unregister()
    tf_mnist.CACHE_DIR.clear()


def get_tensor_config():
    config = {
        'Inputs': [
            {
                'TensorName': 'serving_default_flatten_input:0',
                'DType': 'FP32',
                'Shape': {
                    'MaxShape': [32, 28, 28],
                    'MinShape': [1, 28, 28],
                },
            },
        ],
        'Outputs': [
            {
                'TensorName': 'StatefulPartitionedCall:0',
                'DType': 'FP32',
                'Shape': {
                    'MaxShape': [32, 10],
                    'MinShape': [1, 10],
                },
            },
        ],
    }
    return config


def get_model_metrics():
    metrics = [
        {
            'MetricsType': 'ImageClassification',
            'Params': '{"hardware": "ml.standard.xlarge"}',
            'MetricsData': '{"qps": 10, "latency": 0.3}',
        },
    ]
    return metrics
