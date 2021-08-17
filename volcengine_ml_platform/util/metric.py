# -*- coding: utf-8 -*-

import time

current_ts = lambda: int(round(time.time() * 1000.0))
cost_time = lambda start_time: int(round(time.time() * 1000.0 - start_time))
