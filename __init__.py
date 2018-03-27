# -*- coding:utf-8 -*-
import sys

__version__ = '0.0.1'
__author__  = 'Tatsuya Akagi'


def reload():
    for mod in sys.modules.keys():
        if mod.find("scwrap") > -1:
            del sys.modules[mod]