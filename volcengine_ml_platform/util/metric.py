import time


def current_ts():
    return int(round(time.time() * 1000.0))


def cost_time(start_time):
    return int(round(time.time() * 1000.0 - start_time))
