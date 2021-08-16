# -*- coding: utf-8 -*-

from tests.end2end.common_fixtures import *


@pytest.mark.usefixtures("tf_mnist_model")
def test_inference_service_end2end(tf_mnist_model):
    inference_service = tf_mnist_model.deploy(flavor='ml.highcpu.large',
                                              replica=2)
    inference_service.print()
    assert inference_service.service_id is not None
    # TODO: 3分钟内可以调通推理服务接口
    # TODO: 扩容
    # TODO: 缩容
    # TODO: 关停服务
