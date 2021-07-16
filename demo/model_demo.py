from ml_platform_sdk.models import Model
from ml_platform_sdk.config import credential as auth_credential
import ml_platform_sdk

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    ml_platform_sdk.init(auth_credential.Credential(ak, sk, region))

    model = Model(local_path='demo_model/1',
                  model_id='model-20210715213220-bmm2f')

    model.register(model_name='test-sdk1',
                   model_format='SavedModel',
                   model_type='TensorFlow',
                   description='Test')

    model.download(local_path='download_model')
    model.explain()

    # model.explain()
    #
    # model.unregister()
    # model.explain()
    #
    # model.unregister_all_versions()
