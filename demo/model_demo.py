from ml_platform_sdk.models import Model
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    model = Model(model_id='model-20210716170042-whj22')

    # model.register(model_name='wangchen-test-model1',
    #                model_format='SavedModel',
    #                model_type='TensorFlow:1.14',
    #                description='Test')

    # model.download(local_path='download_model')
    model.explain()

    inference_service = model.deploy()

    # model.explain()
    #
    # model.unregister()
    # model.explain()
    #
    # model.unregister_all_versions()
