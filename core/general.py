# -*- coding:utf-8 -*-
from maya import cmds
from maya.api import OpenMaya

try:
    import unicode
except:
    unicode = str


class Base(unicode):
    """Base class for Node class and Attribute class. This class has common methods like connection.
    """
    def connections(self, *args, **kwds):
        ret = cmds.listConnections(*args, **kwds)
        return list() if ret is None else ret

    def inputs(self, **kwds):
        """override listConnection command fixed only source argument setting.

        Args:
            same as listConnections, but ‘source’ option is always on, ‘destination’ is always off

        Returns:
            list (Node or Attribute)
        """
        ks = kwds.keys()
        [kwds.pop(arg) for arg in ['s', 'd'] if arg in ks]

        func = wrap
        for arg in ['p', 'plug']:
            if arg in ks:
                if ks[arg]:
                    func = Attribute
                    break

        kwds['source'] = 1
        kwds['destination'] = 0

        return [func(node) for node in self.connections(self, **kwds)]
    
    def outputs(self, **kwds):
        """override listConnection command fixed only destination argument setting.

        Args:
            same as listConnections, but ‘source’ option is always off, ‘destination’ is always on

        Returns:
            list (Node or Attribute)
        """
        ks = kwds.keys()
        [kwds.pop(arg) for arg in ['s', 'd'] if arg in ks]

        func = wrap
        for arg in ['p', 'plug']:
            if arg in ks:
                if ks[arg]:
                    func = Attribute
                    break

        kwds['source'] = 0
        kwds['destination'] = 1

        return [func(node) for node in self.connections(self, **kwds)]

    def history(self, **kwds):
        ret = cmds.listHistory(self, **kwds)
        return list() if ret is None else [wrap(node) for node in ret]


class Attribute(Base):
    """
    Attribute wrapper class
    """
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

    def __floordiv__(self, other):
        cmds.disconnectAttr(self, other)

    def get(self, **kwds):
        return cmds.getAttr(self, **kwds)

    def set(self, *val, **kwds):
        cmds.setAttr(self, *val, **kwds)
    

class Node(Base):
    """
    DependNode wrapper class
    """
    def __getattr__(self, attr):
        return Attribute(self, attr)

    def __setattr__(self, attr, val):
        try:
            cmds.setAttr(self + "." + attr, val)
        except:
            cmds.setAttr(self + "." + attr, *val)

    def attr(self, attr):
        return Attribute(self, attr)

    def listAttr(self, **kwds):
        return [Attribute(self, attr) for attr in cmds.listAttr(self, **kwds)]

    def addAttr(self, attr, **kwds):
        cmds.addAttr(self, ln=attr, **kwds)

    def type(self, **kwds):
        return cmds.nodeType(self, **kwds)

    def rename(self, name):
        return Node(cmds.rename(self, name))


class DAGNode(Node):
    """
    DAGNode wrapper class
    """

    def __or__(self, other):
        cmds.parent(other, self)

    def parent(self, *args, **kwds):
        cmds.parent(self, *args, **kwds)

    def _relatives(self, *args, **kwds):
        ret = cmds.listRelatives(*args, **kwds)
        return list() if ret is None else ret

    def getParent(self):
        return DAGNode(self._relatives(self, p=1))

    def getShape(self):
        return [DAGNode(node) for node in self._relatives(self, s=1)]

    def getDagPath(self):
        sels = OpenMaya.MSelectionList()
        sels.add(self)
        return sels.getDagPath(0)


class Transform(DAGNode):
    def getTranslation(self, space='world'):
        spaceDict = {
            'world': 'ws', 
            'object': 'os'
        }
        opt = {'q': 1, 't': 1}
        opt[spaceDict[space]] = 1
        return cmds.xform(self, **opt)


def wrap(node):
    sels = OpenMaya.MSelectionList()
    sels.add(node)
    try:
        dag = sels.getDagPath(0)
        if dag.apiType() == getattr(OpenMaya.MFn, 'kTransform'):
            return Transform(node)
        return DAGNode(node)
    except:
        pass
    return Node(node)
