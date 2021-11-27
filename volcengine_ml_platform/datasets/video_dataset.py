from volcengine_ml_platform.datasets.dataset import _Dataset


class VideoDataset(_Dataset):
    """
    VideoDataset创建函数同 ``ImageDataset``

    """

    def download(self, local_path: str = "VideoDataset", limit=-1):
        """把数据集从 TOS 下载到本地

        Args:
            local_path(str): 设置下载目录
            limit (int, optional): 设置最大下载数据条目
        """

        """download datasets from source

        Args:
            limit (int, optional): download size. Defaults to -1 (no limit).
        """
        if local_path:
            self.local_path = local_path

        self._create_manifest_dataset(
            manifest_keyword="VideoURL",
        )

    def split(self, training_dir: str, testing_dir: str, ratio=0.8, random_state=0):
        return super().split_dataset(
            VideoDataset, training_dir, testing_dir, ratio, random_state
        )
