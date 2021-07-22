import time

from ml_platform_sdk.models import Model
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTMTFjMzZlNmY5MWZkNDc4NmJjZWM1NDJjMWMwZThmMWE'
sk = 'WTJSbU1HWm1PR1ZpWTJNME5EZGhZamxtTkdVeE1EUm1NMlkyT0dJNVlUSQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    # initialize sdk
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    # import model_id from mlplatform.model_repo
    model = Model(model_id='model-20210716170042-whj22')

    # get model detail
    model.print()

    # deploy the selected model_version
    inference_service = model.deploy(flavor='ml.highcpu.large',
                                     replica=1,
                                     model_version=19)

    time.sleep(5)

    # explain inference_service
    inference_service.print()

    # undeploy model's inverence service
    model.undeploy()
    time.sleep(5)

    # explain inference_service
    inference_service.print()
