import os


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CUR_DIR)
# os.system(f"cd {CUR_DIR}/dllogger && python3.7 setup.py install --user && cd {CUR_DIR}")
os.system(f"python3.7 -m pip install -r {CUR_DIR}/requirements.txt --user")
