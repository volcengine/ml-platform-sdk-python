import datetime
import logging.handlers
import os
import time

logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

# /data00 为 tos bucket挂载的根目录，以下本地POSIX本地目录/data00/logs 对应 tos://${your_bucket_name}/logs
logging_file_dir = "/data00/logs/test_logging"
os.makedirs(logging_file_dir, exist_ok=True)

# TOS挂载带来的限制: 不能追加写入已存在的文件，每次必须是一个新文件
logging_file_path = "{}/stdout_{}.log".format(
    logging_file_dir, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
)

logger_handler = logging.handlers.TimedRotatingFileHandler(
    logging_file_path, when="midnight", interval=1, backupCount=7
)
logger_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(logger_handler)

start_time = time.perf_counter()

for i in range(0, 100000):
    print(f"i={i}")
    logger.info(
        "i={}, Train Epoch: 987 [3840/50000 (61%)] Loss: 2.297047Train Epoch: 987 [3840/50000 (61%)] Loss: 2.309227Train Epoch: 987 [3840/50000 (61%)] Loss: 2.306513Train Epoch: 987 [3840/50000 (61%)] Loss: 2.301000".format(
            i
        )
    )
    time.sleep(1)

time_cost = (time.perf_counter() - start_time) * 1000
logger.info("time-cost=%s", time_cost)
print("time-cost=%s" % time_cost)
