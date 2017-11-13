# -*- coding:utf-8 -*-
from maya import cmds
import maya.api.OpenMaya as om

from . import general as gen



def wrap(node):
    node_sep = node.split('.')
    if len(node_sep) == 2:
        return gen.Attribute(*node_sep)
    sels = om.MSelectionList()
    sels.add(node)
    try:
        sels.getDagPath(0)
        return gen.DAGNode(node)
    except:
        pass
    return gen.Node(node)