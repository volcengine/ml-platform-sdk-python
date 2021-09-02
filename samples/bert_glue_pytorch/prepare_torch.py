import os


try:
    import env

    env.init()
except Exception:
    pass


os.system(
    "wget https://mlplatform-public-examples-cn-beijing.tos-cn-beijing.volces.com/bert/util/transformers.tar.gz"
)
os.system("tar -zxf transformers.tar.gz")
os.system("rm transformers.tar.gz")
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
os.system(f"cd {CUR_DIR}/transformers && python3.7 setup.py install --user && cd ..")
os.system("python3.7 -m pip install -r ./requirement.txt")


DATA_PATH = os.getenv("GLUE_DIR", default="./download_data")
TOS_SOURCE = "https://mlplatform-public-examples-cn-beijing.tos-cn-beijing.volces.com/bert/glue/glue_data.tar.gz"
DATA_PATH = os.path.abspath(DATA_PATH)
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
os.system(f"wget {TOS_SOURCE} && tar -zxvf {TOS_SOURCE.split('/')[-1]} -C {DATA_PATH}/")
os.system(f"rm -rf {TOS_SOURCE.split('/')[-1]}")

BERT_BASE_MODEL = "bert-base-uncased"
MODEL_PATH = os.getenv("BERT_MODEL_DIR", default="./download_model")
MODEL_PATH = os.path.abspath(MODEL_PATH)
if not os.path.exists(MODEL_PATH):
    os.mkdir(MODEL_PATH)
TOS_MODEL_SOURCE = f"https://mlplatform-public-examples-cn-beijing.tos-cn-beijing.volces.com/bert/model/{BERT_BASE_MODEL}.tar.gz"
os.system(
    f"wget {TOS_MODEL_SOURCE} && tar -zxvf {TOS_MODEL_SOURCE.split('/')[-1]} -C {MODEL_PATH}/"
)
os.system(f"rm {TOS_MODEL_SOURCE.split('/')[-1]}")
