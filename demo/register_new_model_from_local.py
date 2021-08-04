import json

from ml_platform_sdk.modelrepo.models import Model
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

# # online account id ak/sk
# ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
# sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='

# boe account id ak/sk
ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    # initialize sdk
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    # use local_model
    model = Model(local_path='./demo_model/1')

    # register to mlplatform.model_repo
    metrics = [{
        "MetricsType": "ImageClassification",
        "Params": '{"hardware": "ml.standard.xlarge"}',
        "MetricsData": '{"qps": 10, "latency": 0.3}'
    }]

    tensor_config = None
    with open("tensor_config.json") as f:
        tensor_config = json.loads(f.read())

    model.register(model_name='wangchen-test-model1',
                   model_format='SavedModel',
                   model_type='TensorFlow:1.14',
                   description='SDK_Test',
                   tensor_config=tensor_config,
                   model_metrics=metrics)

    # get model detail
    model.print()

    # deploy the model
    inference_service = model.deploy(flavor='ml.highcpu.large', replica=3)
