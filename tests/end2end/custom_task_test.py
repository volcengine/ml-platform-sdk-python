import time

from volcengine_ml_platform.custom_task.custom_task import CustomTask


def test_custom_task_e2e():
    ctlist = CustomTask.list()
    print(ctlist)

    ct = CustomTask(
        entrypoint_path="sleep 1d",
        framework="Horovod",
        image_id="ml_platform/pytorch:1.7",
        name="task_from_python_sdk",
        # https://console.volcengine.com/ml-platform/resourceGroup/detail?Id=r-20211129110629-5p69f
        resource_group_id="r-20211129110629-5p69f",
        task_role_specs=[
            {"RoleName": "worker", "RoleReplicas": 1, "ResourceSpecId": "ml.g1e.large"}
        ],
        description="end2end test",
    )

    ct.submit()

    get_result = ct.get()
    assert get_result["Name"] == ct.name
    assert get_result["ImageSpec"]["Id"] == ct.image_id
    assert get_result["EntrypointPath"] == ct.entrypoint_path
    assert get_result["ResourceGroupId"] == ct.resource_group_id
    assert (
        get_result["TaskRoleSpecs"][0]["RoleName"] == ct.task_role_specs[0]["RoleName"]
    )
    assert (
        get_result["TaskRoleSpecs"][0]["RoleReplicas"]
        == ct.task_role_specs[0]["RoleReplicas"]
    )
    assert (
        get_result["TaskRoleSpecs"][0]["ResourceSpecId"]
        == ct.task_role_specs[0]["ResourceSpecId"]
    )
    assert get_result["Framework"] == ct.framework
    assert get_result["Description"] == ct.description

    # waiting for custom task to be running
    while get_result["State"] in ["Queue", "Staging", "Initialized"]:
        print(
            f"the current state is {get_result['State']}, waiting for custom task to be running, retry after 3s..."
        )
        time.sleep(3)
        get_result = ct.get()

    list_instances_res = ct.list_instances()
    assert list_instances_res["Total"] == 1
    assert list_instances_res["List"][0]["RoleName"] == "worker"
    assert list_instances_res["List"][0]["RoleIndex"] == "0"
    assert list_instances_res["List"][0]["ResourceSpecId"] == "ml.g1e.large"
    assert list_instances_res["List"][0]["PodName"] == f"{ct.custom_task_id}-worker-0"
    assert list_instances_res["List"][0]["ContainerName"] == "mljob"

    ct.cancel()

    # waiting for custom task to be in terminal state
    while get_result["State"] not in ["Success", "Failed", "Cancelled"]:
        print(
            f"the current state is {get_result['State']}, waiting for custom task to be stopped, retry after 3s..."
        )
        time.sleep(3)
        get_result = ct.get()

    ct.delete()
