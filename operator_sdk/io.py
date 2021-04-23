from operator_sdk import env


class Slot:

    def __init__(self):
        self._config = env.NodeConfig()

    def get_output_path(self, slot_index: int) -> str:
        """Convert output slot_id to local storage path"""
        if slot_index < 1 or slot_index > len(self._config.get_output_slots()):
            raise ValueError('wrong slot_index value,\
                 should be in the range [1, num_of_slots]')
        slot_property = None
        for s in self._config.get_output_slots():
            if s['index'] == slot_index:
                slot_property = s
                break
        return slot_property['path']

    def get_input_path(self, slot_index: int) -> str:
        """Convert input slot_id to local storage path"""
        if slot_index < 1 or slot_index > len(self._config.get_input_slots()):
            raise ValueError('wrong slot_index value,\
                 should be in the range [1, num_of_slots]')
        slot_property = None
        for s in self._config.get_input_slots():
            if s['index'] == slot_index:
                slot_property = s
                break
        return slot_property['path']
