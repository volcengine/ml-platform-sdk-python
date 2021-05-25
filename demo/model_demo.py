from ml_platform_sdk.model.model_client import ModelClient

ak = 'AKLTOTk1NmEwOTYyZDQ2NGJmNTk5M2E1MWY4N2NmMzA4M2Q'
sk = 'TnpjNFlUTmtZalZoTkRSaU5HRXdNV0l4TjJOaU9UWXlZekUxTnpBeE1tUQ=='
region = 'cn-north-1'

if __name__ == '__main__':
    client = ModelClient(ak, sk, region)

    # upload a model
    model_name = "sdk_tf_model"
    model_format = "SavedModel"
    model_type = "TensorFlow:2.0"
    local_path = "/Users/bytedance/Downloads/tf_model/saved_model/"

    resp = client.upload_model(
        model_name,
        model_format,
        model_type,
        local_path,
        # create_new_model=True
    )
    print("create model result: {}".format(resp))
    model_id = resp["Result"]["ModelId"]
    model_version_id = resp["Result"]["ModelVersionId"]

    # download model
    resp = client.download_model(model_version_id, "./")
    print("download model result: {}".format(resp))

    # list models
    resp = client.list_models()
    print("list models result: {}".format(resp))

    # list model versions
    resp = client.list_model_versions()
    print("list model versions result: {}".format(resp))

    # get model version
    resp = client.get_model_version(model_version_id=model_version_id)
    print("get model version result: {}".format(resp))

    # update model version
    resp = client.update_model_version(model_version_id=model_version_id,
                                       description="modified description.")
    print("update model version: {}".format(resp))

    resp = client.delete_model_version(model_name=model_name, model_version='1')
    print("delete model version result: {}".format(resp))

    resp = client.delete_model(model_id=model_id)
    print("delete model result: {}".format(resp))
