# -*- coding:utf-8 -*-
from maya import cmds
import re
import string

from . import general
from . import utils

from maya.cmds import *
""" 全てのcmdsコマンドを展開して
scwrap.commandモジュール上から呼び出す。
下記コマンドはオーバーライドされる。
"""

def ls(*args, **kwds):
    """override ls command
    This function returns wrapper objects.
    if return is None, it returns null list.
    """
    res = cmds.ls(*args, **kwds)
    return list() if res is None else [general.wrap(r) for r in res]


def deleteNode(*args, **kwds):
    """custom delete command
    This function is deleted node even if not exist node, skip delete .
    """
    nodes = args
    if len(args) < 1:
        nodes = cmds.ls(sl=1)
    
    for node in nodes:
        node_lst = [node]
        if isinstance(node, (list, tuple)):
            node_lst = node

        for n in node_lst:
            if cmds.objExists(str(n)):
                cmds.delete(str(n), **kwds)
            else:
                cmds.warning("# Don’t exist - " + node)


def duplicate(*args, **kwds):
    """override duplicate command
    - naming not number order, but alphabet order.
    - all locked attributes are unlocked.
    - if source has intermediate geometries, delete them.
    """
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
                    rep_alp += utils.get_abc(num_order // 26 - 1)
                    num_order %= 26
                rep_alp += utils.get_abc(num_order % 26)
                
                dup = cmds.rename(dup, cmpl.sub(rep_alp , dup))

        # unlock attribute
        attrs = cmds.listAttr(dup, l=1, k=1)
        if attrs:
            for attr in atrs:
                cmds.setAttr(dup + '.' + attr, l=0)

        # delete intermediate shape
        shps = cmds.listRelatives(dup, s=1)
        if shps:
            for shp in shps:
                if cmds.getAttr(shp + '.io'):
                    cmds.delete(shp)
        rets.append(general.wrap(dup))
    
    return rets
        