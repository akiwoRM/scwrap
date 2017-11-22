# -*- coding:utf-8 -*-
from maya import cmds
import re
import string

from . import general
from . import utils


def ls(*args, **kwds):
    res = cmds.ls(*args, **kwds)
    return list() if res is None else [general.wrap(r) for r in res]

def _getABC(num):
    return string.ascii_uppercase[num]

def duplicate(*args, **kwds):
    cmpl = re.compile('([0-9]+)$')
    name = utils.get_opt(kwds, ('n', 'name'), None)

    dups = cmds.duplicate(*args, **kwds)

    rets = []
    for dup in dups:
        # rename to alphabet order if name option is not specified
        if name == None:
            matchObj = cmpl.search(dup)
            if matchObj:
                num_order = int(matchObj.group()[0])
                rep_alp = ""
                while num_order // 26:
                    rep_alp += _getABC(num_order // 26 - 1)
                    num_order %= 26
                rep_alp += _getABC(num_order % 26)
                
                dup = cmds.rename(dup, cmpl.sub(rep_alp , dup))

        # unlock attribute
        for attr in cmds.listAttr(dup, l=1, k=1):
            cmds.setAttr(dup + '.' + attr, l=0)

        # delete intermediate shape
        for shp in cmds.listRelatives(dup, s=1):
            if cmds.getAttr(shp + '.io'):
                cmds.delete(shp)
        rets.append(general.wrap(dup))
    
    return rets
        