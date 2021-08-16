# -*- coding: utf-8 -*-
import pytest

from tests.end2end.common_fixtures import tf_mnist_model


@pytest.mark.usefixtures("tf_mnist_model")
def test_model_end2end(tf_mnist_model):
    # register new model_version to mlplatform.model_repo

    assert tf_mnist_model.model_id is not None
    assert tf_mnist_model.model_version == 1
    # TODO: 注册另外一个版本
    # TODO: 查询版本
    # TODO: 删除版本
