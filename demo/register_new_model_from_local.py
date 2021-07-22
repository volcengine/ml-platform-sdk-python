from ml_platform_sdk.models import Model
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    # initialize sdk
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    # use local_model
    model = Model(local_path='./demo_model')

    # register to mlplatform.model_repo
    model.register(model_name='wangchen-test-model1',
                   model_format='SavedModel',
                   model_type='TensorFlow:1.14',
                   description='SDK_Test')

    # get model detail
    model.print()

    # deploy the model
    inference_service = model.deploy(flavor='ml.highcpu.large', replica=3)
