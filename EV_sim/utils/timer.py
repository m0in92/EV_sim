"""
Contains the decorator to calculate the time for a function or method.
"""

#  Copyright (c) 2023. Moin Ahmed. All rights reserved.

import time


def sol_timer(func):
    def calc_time(*args, **kwargs):
        time_start = time.time()
        sol = func(*args, **kwargs)
        time_end = time.time()
        print(f'Sol time: {time_end - time_start}s')
        return sol
    return calc_time