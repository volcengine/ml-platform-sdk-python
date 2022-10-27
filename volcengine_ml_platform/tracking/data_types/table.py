import os
import uuid
import json

from volcengine_ml_platform.tracking import tos_cli, get_tos_path
from volcengine_ml_platform.tracking.data_types import Image
from volcengine_ml_platform.tracking.data_types import Base


class Table(Base):

    __TYPE__ = "table"
    MAX_ROWS = 10000

    def __init__(
        self,
        columns=None,
        data=None,
        column_type={},
    ):
        if self._is_dataframe(data):
            self._init_from_dataframe(data)
        elif self._is_numpy_array(data):
            self._init_from_dataframe(data, columns)
        else:
            self._init_from_list(data, columns, column_type)

    def _is_dataframe(self, data):
        try:
            import pandas as pd
            return isinstance(data, pd.DataFrame)
        except ImportError:
            return False

    def _is_numpy_array(self, data):
        try:
            import numpy as np
            return isinstance(data, np.ndarray)
        except ImportError:
            return False

    def _init_from_dataframe(self, dataframe):
        self.data = []
        self.column_type = {}
        self.column_idx_type = {}
        self.columns = {c for c in list(dataframe.columns)}
        for row in range(len(dataframe)):
            self.add_row(*[dataframe[col].values[row] for col in self.columns])

    def _init_from_ndarray(self, ndarray, columns):
        self.data = []
        self.column_type = {}
        self.column_idx_type = {}
        self.columns = columns
        for row in ndarray:
            self.add_row(*row)

    def _init_from_list(self, data, columns, column_type):
        self.data = []
        self.columns = columns
        self.column_type = column_type
        _column_idx = {columns[idx]: idx for idx in range(len(columns))}
        self.column_idx_type = {
            _column_idx[column]: type for column, type in column_type.items()}
        if data is not None:
            for row in data:
                self.add_row(*row)

    def add_row(self, *data):
        if len(data) != len(self.columns):
            raise Exception(
                "Table expects {} columns, found {}.".format(len(self.columns), len(data)))
        if isinstance(data, tuple):
            data = list(data)
        # 检查类型是否满足要求
        for idx, type in self.column_idx_type.items():
            if not isinstance(data[idx], type):
                raise Exception("Column %s should be an Image",
                                self.columns[idx])
        self.data.append(data)

    def upload_tos(self):
        """将信息上传至tos
        """
        _data = []
        tos_bucket, tos_prefix = get_tos_path()
        for row in self.data:
            for idx in range(len(row)):
                item = row[idx]
                if isinstance(row[idx], Image):
                    path = item.upload_tos(tos_bucket, tos_prefix)
                    row[idx] = path
            _data.append(row)
        info = {
            "data": _data,
            "columns": self.columns,
            "column_type": {column: type.__TYPE__ if hasattr(type, '__TYPE__') else type for column, type in self.column_type.items()},
        }
        file_name = uuid.uuid4().hex
        local_path = "/tmp/" + file_name
        with open(local_path, 'w') as f:
            f.write(json.dumps(info))
        tos_path = tos_cli.upload(local_path, tos_bucket, tos_prefix)
        os.remove(local_path)
        return os.path.join(tos_path, file_name)

    @property
    def step_item(self):
        tos_path = self.upload_tos()
        return {
            "Type": self.__TYPE__,
            "Table": {
                "TosPath": tos_path,
            }
        }
