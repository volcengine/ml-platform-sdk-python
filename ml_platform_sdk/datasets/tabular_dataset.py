from typing import Optional

from ml_platform_sdk.datasets.dataset import _Dataset


class TabularDataset(_Dataset):

    def create(self, local_path: Optional[str] = None):
        if local_path is not None:
            self.local_path = local_path
        self._download_file(self._get_storage_path(), self.local_path)
        self.created = True
