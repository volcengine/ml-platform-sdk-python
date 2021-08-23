# -*- coding: utf-8 -*-
import pytest

from samples.mnist import tf_mnist
from tests.end2end.common_fixtures import get_tensor_config, get_model_metrics
from volcengine_ml_platform.models import model


def test_model_end2end():
    # 准备tensorflow mnist模型包
    tf_mnist.main()

    client = model.Model()
    tensor_config = get_tensor_config()
    model_metrics = get_model_metrics()

    # 创建一个带metrics信息的模型（模拟AutoML的用法）
    resp = client.register(model_name='tensorflow-minist-model1',
                           model_format='SavedModel',
                           model_type='TensorFlow:2.4',
                           description='tensorflow-minist-model_description',
                           local_path=tf_mnist.get_saved_path(),
                           model_metrics=model_metrics)
    model_version_1 = resp["Result"]
    assert model_version_1["ModelID"] is not None
    assert model_version_1["ModelVersion"] == 1
    model_id = model_version_1["ModelID"]

    # 为模型注册新的版本，带tensor配置信息
    resp = client.register(model_id=model_id,
                           model_name='tensorflow-minist-model1',
                           model_format='SavedModel',
                           model_type='TensorFlow:2.4',
                           description='tensorflow-minist-model_description',
                           local_path=tf_mnist.get_saved_path(),
                           tensor_config=tensor_config)
    model_version_2 = resp["Result"]
    assert model_version_2["ModelID"] is not None
    assert model_version_2["ModelVersion"] == 2

    # 获取模型版本1
    resp = client.get_model_versions(
        model_id=model_version_1["ModelID"],
        model_version=model_version_1["ModelVersion"])
    assert resp["Result"]["Total"] == 1
    assert resp["Result"]["List"][0]["ModelVersion"] == 1

    # 删除模型版本1
    resp = client.unregister(model_id=model_version_1["ModelID"],
                             model_version=model_version_1["ModelVersion"])
    resp = client.get_model_versions(
        model_id=model_version_1["ModelID"],
        model_version=model_version_1["ModelVersion"])
    assert resp["Result"]["Total"] == 0

    # 为模型版本2创建一个评测任务
    job_params = [{
        "FlavorIDList": ["fl-20210727155225-2n9lw", "fl-20210727155225-b86fl"],
    }]
    resp = client.create_perf_job(model_id=model_version_2["ModelID"],
                                  model_version=model_version_2["ModelVersion"],
                                  tensor_config=tensor_config,
                                  job_type="PERF_ONLY",
                                  job_params=job_params)
    assert resp["Result"]["JobID"] is not None
    job_id = resp["Result"]["JobID"]

    # 获取评测任务列表
    resp = client.list_perf_tasks(job_id=job_id)
    assert resp["Result"]["Total"] == 2
    task_1_id = resp["Result"]["List"][0]["TaskID"]

    # 更新评测任务状态
    status = "Finished"
    resp = client.update_perf_task(task_id=task_1_id, task_status=status)
    assert resp["Result"]["TaskID"] == task_1_id

    # 更新模型版本2的metrics数据（模拟PerfWorker的用法）
    resp = client.update_model_version(
        model_id=model_version_2["ModelID"],
        model_version=model_version_2["ModelVersion"],
        model_metrics=model_metrics)

    # 获取评测任务列表
    resp = client.list_perf_tasks(task_id=task_1_id)
    assert resp["Result"]["Total"] == 1
    assert resp["Result"]["List"][0]["TaskStatus"] == status

    # 测试结束，删掉模型
    client.unregister_all_versions(model_id=model_id)