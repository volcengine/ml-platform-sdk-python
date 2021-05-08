import logging
import os
from operator_sdk import env


class Slot:

    def __init__(self, io_type: str, slot_index: int):
        self._config = env.Config()

        if io_type not in ('input', 'output'):
            raise ValueError('io_type can only be "input" or "output"')

        slots = None
        if io_type == 'input' and 0 < slot_index <= len(
                self._config.get_input_slots()):
            slots = self._config.get_input_slots()
        elif io_type == 'output' and 0 < slot_index <= len(
                self._config.get_output_slots()):
            slots = self._config.get_output_slots()
        else:
            raise ValueError('invalid slot_index value,\
                              should be in the range [1, num_of_slots]')

        self._index = slot_index
        self._io_type = io_type
        self._property = None

        for s in slots:
            if s['index'] == self._index:
                self._property = s
                break

        self.local_path = self._property['path']

        if io_type == 'output' and self.local_path != "":
            try:
                os.makedirs(self.local_path, exist_ok=True)
            except OSError as e:
                logging.warning('Cannot create output directory')
                raise e

    def get_path(self) -> str:
        """return local storage path"""
        return self.local_path
