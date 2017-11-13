# -*- coding:utf-8 -*-
from maya import cmds

from . import general


def ls(*args, **kwds):
    res = cmds.ls(*args, **kwds)
    return list() if res is None else [general.wrap(r) for r in res]