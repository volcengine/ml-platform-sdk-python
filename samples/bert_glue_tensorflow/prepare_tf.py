import os


try:
    import env

    env.init()
except Exception:
    pass

os.system("python3.7 -m pip install -r ./requirement.txt")

DATA_PATH = os.getenv("GLUE_DIR", default="./download_data")
TOS_SOURCE = "https://ml-platform-public-examples-cn-beijing.tos-cn-beijing.volces.com/bert/glue/glue_data.tar.gz"
DATA_PATH = os.path.abspath(DATA_PATH)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
os.system(f"wget {TOS_SOURCE} && tar -zxvf {TOS_SOURCE.split('/')[-1]} -C {DATA_PATH}/")
os.system(f"rm -rf {TOS_SOURCE.split('/')[-1]}")

BERT_BASE_MODEL = "uncased_L-12_H-768_A-12"
MODEL_PATH = os.getenv("BERT_MODEL_DIR", default="./download_model")
MODEL_PATH = os.path.abspath(MODEL_PATH)
TOS_MODEL_SOURCE = f"https://ml-platform-public-examples-cn-beijing.tos-cn-beijing.volces.com//bert/model/{BERT_BASE_MODEL}.zip"

os.system(
    f"wget {TOS_MODEL_SOURCE} && unzip {TOS_MODEL_SOURCE.split('/')[-1]} -d {MODEL_PATH}/"
)
os.system(f"rm {TOS_MODEL_SOURCE.split('/')[-1]}")
