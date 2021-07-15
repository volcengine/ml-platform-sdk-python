import os


class Credential:

    def __init__(self, ak=None, sk=None, region=None):
        self.ak = ak
        self.sk = sk
        self.region = region

    def get_access_key_id(self) -> str:
        if self.ak is None or self.ak == "":
            return os.environ['ACCESS_KEY_ID']
        return self.ak

    def get_secret_access_key(self) -> str:
        if self.sk is None or self.sk == "":
            return os.environ['SECRET_ACCESS_KEY']
        return self.sk

    def get_region(self) -> str:
        if self.region is None or self.region == "":
            return os.environ['SERVICE_REGION']
        return self.region
