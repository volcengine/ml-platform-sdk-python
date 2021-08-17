# -*- coding: utf-8 -*-

import random
import time

rand_min = 1000
rand_max = 9999


def get_ms_timestamp():
    return int(round(time.time() * 1000))


def gen_req_id():
    date_part = str(get_ms_timestamp())
    random_part = str(random.randint(rand_min, rand_max))
    return date_part + random_part
