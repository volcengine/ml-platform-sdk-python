import random
import time


def get_ms_timestamp():
    return int(round(time.time() * 1000))


def gen_req_id():
    date_part = str(get_ms_timestamp())
    random_part = str(random.randint(1000, 9999))
    return date_part + random_part
