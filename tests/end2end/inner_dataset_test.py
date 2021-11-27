# type: ignore
"""
测试前置条件: 注入ML_PLATFORM_HOST、VOLC_ACCESSKEY、VOLC_SECRETKEY、VOLC_REGION等环境变量
"""
from volcengine_ml_platform.datasets.image_dataset import ImageDataset
from volcengine_ml_platform.datasets.inner_dataset import InnerDataset
from volcengine_ml_platform.datasets.tabular_dataset import TabularDataset

# 根据实际情况填写
target_account_id = 0
target_user_id = 0
tabular_dataset_id = "xxx"
non_tabular_dataset_id = "xxx"
non_tabular_annotation_id = "xxx"


def test_inner_tabular_dataset():
    print("test inner tabular dataset")
    dataset = InnerDataset(
        dataset_type=TabularDataset,
        dataset_id=tabular_dataset_id,
        target_user_id=target_user_id,
        target_account_id=target_account_id,
    )
    print(dataset.target_account_id)
    dataset.download(local_path="InnerTabulareDataset")
    train_dataset, test_dataset = dataset.split(
        dataset.dataset_type, "./tabular_train_dir", "./tabular_test_dir", ratio=0.5
    )
    print("train_dataset_count: ", train_dataset.data_count)
    print("test_dataset_count: ", test_dataset.data_count)


def test_inner_non_tabular_dataset():
    print("test inner non tabular dataset")
    dataset = InnerDataset(
        dataset_type=ImageDataset,
        dataset_id=non_tabular_dataset_id,
        annotation_id=non_tabular_annotation_id,
        target_user_id=target_user_id,
        target_account_id=target_account_id,
    )
    print(dataset.target_account_id)
    dataset.download(local_path="InnerNonTabulareDataset")
    train_dataset, test_dataset = dataset.split(
        dataset.dataset_type,
        "./non_tabular_train_dir",
        "./non_tabular_test_dir",
        ratio=0.5,
    )
    print("train_dataset_count: ", train_dataset.data_count)
    print("test_dataset_count: ", test_dataset.data_count)


if __name__ == "__main__":
    test_inner_tabular_dataset()
    test_inner_non_tabular_dataset()
