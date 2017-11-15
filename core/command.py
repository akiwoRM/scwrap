# -*- coding:utf-8 -*-
from maya import cmds

from . import general


def ls(*args, **kwds):
    res = cmds.ls(*args, **kwds)
    return list() if res is None else [general.wrap(r) for r in res]


def duplicate(*args, **kwds):
    dups = cmds.duplicate(*args, **kwds)
    
    rets = []
    for dup in dups:
        # unlock attribute
        for attr in cmds.listAttr(dup, l=1, k=1):
            cmds.setAttr(dup + '.' + attr, l=0)

        # delete intermediate shape
        for shp in cmds.listRelatives(dup, s=1):
            if cmds.getAttr(shp + '.io'):
                cmds.delete(shp)
        rets.append(general.wrap(dup))
    
    return rets
        