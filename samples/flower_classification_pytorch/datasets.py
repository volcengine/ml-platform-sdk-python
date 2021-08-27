import torch

from volcengine_ml_platform.io import tos_files_io


class CustomDataset(tos_files_io.TorchTOSDataset):
    def _target_transform(self, target):
        classes = list(set(self.annotations))
        target = torch.tensor(classes.index(target))
        target = torch.nn.functional.one_hot(target, len(classes))
        return target
