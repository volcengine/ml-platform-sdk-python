import json
import os
from typing import Optional

from volcengine_ml_platform.config import credential as auth_credential


class _Config:

    def __init__(self):
        self._credential = None

    def init(self, credential: Optional[auth_credential.Credential] = None):
        env_credential = None
        if os.environ.get('HOME', None) is not None:
            path = os.environ['HOME'] + '/.volc/mlplatform.conf'
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    nconf = json.load(f)
                    env_credential = auth_credential.Credential(
                        ak=nconf['ak'], sk=nconf['sk'], region=nconf['region'])

        if env_credential:
            self._credential = env_credential
        if credential:
            self._credential = credential

    def get_credential(self):
        return self._credential


global_config = _Config()
