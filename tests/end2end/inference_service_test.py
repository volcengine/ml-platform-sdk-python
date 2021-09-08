import pytest

from tests.end2end.common_fixtures_test import model


@pytest.mark.usefixtures("tf_mnist_model")
def test_inference_service_end2end(tf_mnist_model):
    client = model.Model()
    inference_service = client.deploy(
        model_id=tf_mnist_model["ModelID"],
        model_version=tf_mnist_model["ModelVersion"],
        service_name="test_tf_mnist_service",
        flavor="ml.highcpu.large",
        replica=2,
    )
    inference_service.print()
    assert inference_service.service_id is not None
    # TODO: 3分钟内可以调通推理服务接口
    # TODO: 扩容
    # TODO: 缩容
    # TODO: 关停服务
