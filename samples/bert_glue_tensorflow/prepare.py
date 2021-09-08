import os


try:
    import env

    env.init()
except Exception:
    pass

BASE_DIR = "~/.volcengine_ml_platform/samples/bert_glue"
BASE_DIR = os.path.expanduser(BASE_DIR)


def create_dir(dirs, index=0):
    if index >= len(dirs):
        return
    cur = "/".join(dirs[: index + 1])
    cur = os.path.expanduser(cur)
    if cur == "":
        pass
    elif not os.path.exists(cur):
        os.mkdir(cur)
    create_dir(dirs, index + 1)


create_dir(BASE_DIR.split("/"))


# download glue data
DATA_PATH = os.getenv("GLUE_DIR", default=BASE_DIR)
TOS_SOURCE = "https://ml-platform-public-examples-cn-beijing.tos-cn-beijing.volces.com/bert/glue/glue_data.tar.gz"
DATA_PATH = os.path.abspath(DATA_PATH)
if not os.path.exists(DATA_PATH):
    create_dir(DATA_PATH.split("/"))
data_file = TOS_SOURCE.split("/")[-1]
data_file = f"{BASE_DIR}/{data_file}"
os.system(f"wget -O {data_file} {TOS_SOURCE} && tar -zxvf {data_file} -C {DATA_PATH}/")
os.system(f"rm {data_file}")

BERT_BASE_MODEL = "uncased_L-12_H-768_A-12"
MODEL_PATH = os.getenv("BERT_MODEL_DIR", default=BASE_DIR)
MODEL_PATH = os.path.abspath(MODEL_PATH)
if not os.path.exists(MODEL_PATH):
    create_dir(MODEL_PATH.split("/"))
TOS_MODEL_SOURCE = f"https://ml-platform-public-examples-cn-beijing.tos-cn-beijing.volces.com//bert/model/{BERT_BASE_MODEL}.zip"
model_file = TOS_MODEL_SOURCE.split("/")[-1]
model_file = f"{BASE_DIR}/{model_file}"
os.system(
    f"wget -O {model_file} {TOS_MODEL_SOURCE} && unzip {model_file} -d {MODEL_PATH}/"
)
os.system(f"mv {BASE_DIR}/{BERT_BASE_MODEL} {BASE_DIR}/{BERT_BASE_MODEL}-model")
os.system(f"rm {model_file}")
