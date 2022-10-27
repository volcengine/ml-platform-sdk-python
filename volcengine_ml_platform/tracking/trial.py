import inspect
import types
import volcengine_ml_platform.tracking as tk
from volcengine_ml_platform.tracking import tk_cli

from typing import Dict, Any, Optional, List
from volcengine_ml_platform.tracking import data_types
from volcengine_ml_platform.tracking.common.logger import logger


class Trial():

    def __init__(self, sid):
        self.sid = sid

        self._step = 0

        self._entities = {}  # 统计当前step有哪些entity
        self._entity_items = {}  # 统计当前step下entity的具体打点
        self._entity_custom_step = {}  # 记录entity的custom step

        self._all_entities = {}  # 统计总共有哪些entity

    def define_metric(self, name, step_metric=""):
        """定义entity"""
        if name and step_metric:
            self._entity_custom_step[name] = step_metric

    def log(self, data: Dict[str, Any], step: Optional[int] = None, commit=True):
        """主要的打点入口
        Arguments:
            step:
                如果为None, 等同于递增了step. self._step += 1
                如果大于self.step 则上传之前的数据
                如果小于self.step 则忽略
                如果等于self.step 则继续记录数据
            commit:
                如果为True, 上传该次step的记录
                如果为False, 不上传

        """
        if step is None:
            # 上传self._step的数据，当前数据step为self._step + 1
            self._upload_data()
            self._step += 1

        elif step < self._step:
            # 忽略当前数据
            logger.debug("Step %d < %d, ignore this log data",
                         step, self._step)
        elif step > self._step:
            self._upload_data()
            self._step = step
        else:  # equals
            pass
        # 解析data，更新entity及entity items
        self._update_entity(data)
        # 如果commit，则上传数据，step += 1
        if commit:
            self._upload_data()
            self._step += 1

    def _update_entity(self, data: Dict[str, Any]) -> List[Any]:
        """Update entities and entity items"""
        for k, v in data.items():
            if not isinstance(v, data_types.Base):
                v = data_types.Scalar(value=float(v))
            self._entity_items[k] = v.step_item
            if k not in self._all_entities:
                entity = {
                    "Name": k,
                    "Type": v.__TYPE__,
                    "CustomStep": self._entity_custom_step.get(k),
                }
                self._entities[k] = entity
                self._all_entities[k] = entity

    def _upload_data(self):
        # 上传数据并清空list
        if self._entities:
            tk_cli.create_trial_entities(
                experiment_id=tk.experiment.sid,
                trial_id=tk.trial.sid,
                entities=list(self._entities.values()),
            )
            self._entities = {}
        if self._entity_items:
            tk_cli.create_trial_entity_steps(
                trial_id=tk.trial.sid,
                steps=[{
                    "Step": self._step,
                    "Items": self._entity_items,
                }],
            )
            # 清空当前step记录
            self._entity_items = {}

    def finish(self):
        self._upload_data()


class Config:

    def __init__(self, params: dict = None):
        object.__setattr__(self, "_items", params or {})

    def __setitem__(self, key, value):
        self._items[key] = value
        tk_cli.set_trial_config(
            tk.experiment.sid, tk.trial.sid, {key: value})

    def __getitem__(self, key):
        return self._items[key]

    def update(self, params):
        params = self._parse_config(params)
        self._items.update(params)
        tk_cli.set_trial_config(tk.experiment.sid, tk.trial.sid, params)

    def _parse_config(self, params):
        if isinstance(params, dict):
            return params
        # Handle some cases where params is not a dictionary
        # by trying to convert it into a dictionary
        meta = inspect.getmodule(params)
        if meta:
            is_tf_flags_module = (
                isinstance(params, types.ModuleType)
                and meta.__name__ == "tensorflow.python.platform.flags"  # noqa: W503
            )
            if is_tf_flags_module or meta.__name__ == "absl.flags":
                params = params.FLAGS
                meta = inspect.getmodule(params)

        # newer tensorflow flags (post 1.4) uses absl.flags
        if meta and meta.__name__ == "absl.flags._flagvalues":
            params = {name: params[name].value for name in dir(params)}
        elif not hasattr(params, "__dict__"):
            raise TypeError(
                "config must be a dict or have a __dict__ attribute.")
        elif "__flags" in vars(params):
            # for older tensorflow flags (pre 1.4)
            if not "__parsed" not in vars(params):
                params._parse_flags()
            params = vars(params)["__flags"]
        else:
            # params is a Namespace object (argparse)
            # or something else
            params = vars(params)

        return params

    __setattr__ = __setitem__
    __getattr__ = __getitem__

    def __repr__(self):
        return str(self._items)


class Summary:

    def __init__(self, params: dict = None):
        object.__setattr__(self, "_items", params or {})

    def __setitem__(self, key, value):
        self._items[key] = value
        tk_cli.set_trial_summary(tk.experiment.sid, tk.trial.sid, {key: value})

    def update(self, params):
        tk_cli.set_trial_summary(tk.experiment.sid, tk.trial.sid, params)

    __setattr__ = __setitem__

    def __repr__(self):
        return str(self._items)

    def __getitem__(self, key):
        return self._items[key]

    __setattr__ = __setitem__
    __getattr__ = __getitem__
