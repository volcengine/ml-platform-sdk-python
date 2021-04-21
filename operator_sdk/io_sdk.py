import os


class Slot:

    def output_path(self, slot_id) -> str:
        """Convert output slot_id to local storage path"""
        return self._assemble_path(slot_id, 'output')

    def input_path(self, slot_id) -> str:
        """Convert input slot_id to local storage path"""
        return self._assemble_path(slot_id, 'input')

    def _assemble_path(self, slot_id, slot_type):
        """
        Generate path following the rule:
        /cache/{NODE_ID}/{SLOT_TYPE}/{SLOT_ID}
        """
        root_path = '/cache'
        node_id = os.environ['NODE_ID']
        return os.path.join(root_path, node_id, slot_type, str(slot_id))
