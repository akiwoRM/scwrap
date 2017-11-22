# -*- coding:utf-8 -*-
"""
utility functions not to depend on Maya
"""


def get_opt(kwds, keys, init_val):
    val = init_val
    if isinstance(keys, list):
        for k in keys:
            val = kwds.get(k, val)
    return val

def get_abc(num):
    return string.ascii_uppercase[num]
