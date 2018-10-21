# -*- coding:utf-8 -*-
"""
naming functions
"""
from __future__ import division
import string
from maya import cmds
from . import utils


namingRule = "{name}{sq}"


def n_(name, *args, **opt):
    """
    Args:
        name(string): basic name
        namespace, ns(string): namespace

    Returns;
        string - unique name
    """
    def uniqAbc(num, st=""):
        j = num // 26
        if j:
            st += uniqAbc(j - 1, st)
        k = num % 26
        st += utils.get_abc(k)
        return st

    global namingRule
    ns = utils.get_opt(opt, ["namespace", "ns"], "")

    ret = name
    f_name = namingRule.format(name=name)
    if name.find("#") > -1:
        f_name = name.replace("#", "{sq}")

    i = 0    
    while cmds.objExists(ns + ":" + ret):
        alp = uniqAbc(i)

        ret = f_name.format(sq=alp)
        alp = ""
        i += 1            
    
    return ret if ns is "" else ns + ":" + ret