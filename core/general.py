# -*- coding:utf-8 -*-
from maya import cmds

try:
    import unicode
except:
    unicode = str


class Attribute(unicode):
    _node = ''
    _attr = ''

    def __new__(cls, *args, **kwds):
        if len(args) == 2:
            cls._node = args[0]
            cls._attr = args[1]
        elif len(args) == 1:
            cls._node, cls._attr = args[0].split('.')
        return super(Attribute, cls).__new__(cls, cls._node + "." + cls._attr)

    def __getitem__(self, idx):
        return Attribute(self._node, self._attr + '[{0}]'.format(idx))

    def __rshift__(self, other):
        cmds.connectAttr(self, other, f=1)

    def __lshift__(self, other):
        cmds.connectAttr(other, self, f=1)

    def _connections(self, *args, **kwds):
        ret = cmds.listConnections(*args, **kwds)
        return list() if ret is None else ret

    def inputs(self, **kwds):
        [del kwds[arg] for arg in ['s', 'd', 'source', 'destination'] if arg in kwds.keys()]
        kwds['s'] = 1
        kwds['d'] = 0
        return [Node(node) for node in self._conection(self, **kwds)]
    
    def outputs(self, **kwds):
        [del kwds[arg] for arg in ['s', 'd', 'source', 'destination'] if arg in kwds.keys()]
        kwds['s'] = 0
        kwds['d'] = 1
        return [Node(node) for node in self._conection(self, **kwds)]

    def history(self, **kwds):
        ret = cmds.listHistory(self, **kwds)
        return list() if ret is None else [Node(node) for node in ret]

    def get(self, **kwds):
        return cmds.getAttr(self, **kwds)

    def set(self, *val, **kwds):
        cmds.setAttr(self, *val, **kwds)
    

class Node(unicode):
    def __getattr__(self, attr):
        return Attribute(self, attr)

    def __setattr__(self, attr, val):
        try:
            cmds.setAttr(self + "." + attr, val)
        except:
            cmds.setAttr(self + "." + attr, *val)

    def attr(self, attr):
        return Attribute(self, attr)