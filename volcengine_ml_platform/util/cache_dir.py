import os

HOME_DIR = os.environ.get('HOME', default='/tmp')

SAMPLES_ROOT = '.volcengine_ml_platform/samples/'


def create(name):
    return CacheDir(name)


class CacheDir:
    def __init__(self, name):
        print(os.path.dirname(__file__))
        self.root_path = os.path.join(HOME_DIR, SAMPLES_ROOT, name)
        os.makedirs(self.root_path, exist_ok=True)
        print('use cache dir: ' + self.root_path)

    def get_root_path(self):
        return self.root_path

    def subpath(self, path):
        res = os.path.join(self.get_root_path(), path)
        res_dir = os.path.dirname(res)
        os.makedirs(res_dir, exist_ok=True)
        return res

    def clear(self):
        pass
