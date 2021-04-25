import os
import json


class NodeConfig:

    def __init__(self):
        config_str = os.environ['NODE_CONFIG']
        self.config = json.loads(config_str)

    def get_node_id(self):
        return self.config['id']

    def get_input_slots(self):
        return self.config['inputs']

    def get_output_slots(self):
        return self.config['outputs']

    def get_params(self):
        return self.config['config']['parameters']
