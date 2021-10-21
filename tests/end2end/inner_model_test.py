import os
import shutil

from samples.mnist import tf_mnist
from tests.end2end.common_fixtures_test import get_model_metrics
from tests.end2end.common_fixtures_test import get_model_tensor_config, get_perf_job_tensor_config
from volcengine_ml_platform.models import inner_model


def test_inner_model_end2end():
    # 准备tensorflow mnist模型包
    tf_mnist.main()

    client = inner_model.Model()
    model_tensor_config = get_model_tensor_config()
    model_metrics = get_model_metrics()

    # 创建一个模型
    resp = client.register(
        model_name="tensorflow-minist-model1",
        model_format="SavedModel",
        model_type="TensorFlow:2.4",
        description="tensorflow-minist-model_description",
        local_path=tf_mnist.get_saved_path(),
        tensor_config=model_tensor_config,
    )
    model_version_1 = resp["Result"]
    model_id = model_version_1["ModelID"]
    model_version = model_version_1["VersionInfo"]["ModelVersion"]
    model_version_id = model_version_1["VersionInfo"]["ModelVersionID"]
    assert model_id is not None
    assert model_version == "V1.0"

    # 获取模型信息(模拟推理服务用法)
    resp = client.get_model_version(model_id=model_id, model_version=model_version)
    assert resp["Result"]["TensorConfig"] is not None
    print("tensor config: {}".format(resp["Result"]["TensorConfig"]))

    # 下载模型
    local_path = "./tmp_model"
    os.mkdir(local_path)
    client.download(
        model_id=model_id,
        model_version=model_version,
        local_path=local_path,
    )
    shutil.rmtree(local_path)

    # 更新模型metrics数据
    resp = client.update_model_version(
        model_id=model_id,
        model_version=model_version,
        model_metrics=model_metrics,
    )
    assert resp["Result"] is not None

    # 为模型注册新的版本，带tensor配置信息(模拟模型转换任务的用法)
    resp = client.register(
        model_id=model_id,
        model_format="SavedModel",
        model_type="TensorFlow:2.4",
        description="converted model",
        local_path=tf_mnist.get_saved_path(),
        tensor_config=model_tensor_config,
        source_type="Perf",
        base_model_version_id=model_version_id,
    )
    model_version_2 = resp["Result"]
    assert model_version_2["ModelID"] is not None
    assert model_version_2["VersionInfo"]["ModelVersion"] == "V1.1"

    # 创建一个带metrics信息的模型（模拟AutoML的用法）
    resp = client.register(
        model_id=model_id,
        model_format="AutoML",
        model_type="AutoML:1.0",
        description="automl model",
        local_path=tf_mnist.get_saved_path(),
        model_metrics=model_metrics,
        source_type="AutoML"
    )
    model_version_3 = resp["Result"]
    assert model_version_3["ModelID"] is not None
    assert model_version_3["VersionInfo"]["ModelVersion"] == "V2.0"
