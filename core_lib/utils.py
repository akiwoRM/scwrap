# -*- coding:utf-8 -*-
"""
utility functions not to depend on Maya
"""
import string


def get_opt(kwds, keys, init_val):
    """return value source dictionary

    ex.) 
    n = get_opt(kwds, ['n', 'name'], "Copy#")
    """
    val = init_val
    if isinstance(keys, list):
        for k in keys:
            val = kwds.get(k, val)
    return val


def get_abc(num):
    return string.ascii_uppercase[num]


def pascal_case(name):
    return name[0].upper() + name[1:]


def camel_case(name):
    return name[0].lower() + name[1:]
