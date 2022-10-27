import os
import uuid
import numpy as np
from pathlib import Path
from PIL import Image as PILImage
from volcengine_ml_platform.tracking import tos_cli


class Image():

    __TYPE__ = "image"

    def __init__(self, data):
        if isinstance(data, PILImage.Image):
            self.pil_image = data
        elif isinstance(data, str):
            path = Path(data)
            if not path.is_file():
                raise ValueError(f'Not a regular file: {path}')
            self.pil_image = PILImage.open(path)
        elif isinstance(data, np.ndarray):
            if data.dtype == np.uint8:
                pass
            elif data.dtype == np.float32 or data.dtype == np.float64:
                data = (data * 255).astype(np.uint8)
            else:
                raise ValueError(
                    f'Expect np.ndarray with dtype uint8/float32/float64, but got {data.dtype}')
            if data.ndim == 2:
                self.pil_image = PILImage.fromarray(data)
            elif data.ndim == 3:
                self.pil_image = PILImage.fromarray(data)
            else:
                raise ValueError(f'Invalid image shape: {data.ndim}')

    def upload_tos(self, bucket, prefix):
        """将图片上传至tos，换成tos path
        """
        # image path
        file_name = uuid.uuid4().hex + '.PNG'
        local_path = "/tmp/" + file_name
        self.pil_image.save(local_path, 'PNG')
        tos_path = tos_cli.upload(local_path, bucket, prefix)
        os.remove(local_path)
        return os.path.join(tos_path, file_name)
