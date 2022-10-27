import functools
import time
import logging


def retry(count, delay_seconds=0):
    '''retry a given number of times, supports set delay internal
    count: int, retry times
    delay_seconds: int
    '''
    def deco_retry(f):
        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries = count
            while mtries > 1:
                try:
                    mtries -= 1
                    return f(*args, **kwargs)
                except Exception as e:
                    time.sleep(delay_seconds)
                    logging.info(
                        'Retrying function [%s]..., Error: %s', f.__name__, e)
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry
