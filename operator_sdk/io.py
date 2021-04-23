from operator_sdk import env


class Slot:

    def __init__(self, slot_index: int, io_type: str):
        self._config = env.NodeConfig()

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

    def get_path(self) -> str:
        """return local storage path"""
        return self._property['path']
