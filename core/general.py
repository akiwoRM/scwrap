# -*- coding:utf-8 -*-
from maya import cmds
from maya.api import OpenMaya
from . import utils

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
        """override listHistory command
        add type option
        """
        nType = utils.get_opt(kwds, ("type", "t"), None)
        kwds.pop("type", None)
        kwds.pop("t", None)

        ret = cmds.listHistory(self, **kwds)

        if nType is not None:
            ret = [node for node in ret if cmds.nodeType(node) == nType]

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
        """Access to multi attribute
        """
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
        return Attribute(self, attr)

    def type(self, **kwds):
        return cmds.nodeType(self, **kwds)

    def rename(self, name):
        return wrap(cmds.rename(self, name))


class DAGNode(Node):
    """
    DAGNode wrapper class
    """

    def __or__(self, other):
        cmds.parent(other, self)

    def parent(self, *args, **kwds):
        cmds.parent(self, *args, **kwds)

    def relatives(self, *args, **kwds):
        ret = cmds.listRelatives(*args, **kwds)
        return list() if ret is None else ret

    def getParent(self, num=1):
        ret = self
        for i in range(num):
            ret = DAGNode(self.relatives(ret, p=1))
        return ret

    def getShape(self):
        return [DAGNode(node) for node in self.relatives(self, s=1)]

    def getDagPath(self):
        sels = OpenMaya.MSelectionList()
        sels.add(self)
        return sels.getDagPath(0)


class Transform(DAGNode):
    """Transform class
    """
    spaceDict = {
        'world': 'ws', 
        'object': 'os'
    }

    def freeze(self, **kwds):
        if kwds == {}:
            kwds = {'apply': 1, 't': 1, 'r': 1, 's': 1}
        cmds.makeIdentity(self, **kwds)
        # reset pivot
        cmds.xform(self, os=1, piv=[0, 0, 0])
        # delete history
        cmds.delete(self, ch=1)

    def getTranslation(self, space='world'):
        opt = {'q': 1, 't': 1}
        opt[self.spaceDict[space]] = 1
        return cmds.xform(self, **opt)
        
    def setTranslation(self, args, space='world'):
        opt = {self.spaceDict[space]: 1}
        if len(args) > 1:
            opt['t'] = args
        elif len(args) == 1:
            if isinstance(args[0], list):
                opt['t'] = args[0]
        cmds.xform(self, **opt)

    def getRotation(self, space='world'):
        opt = {'q': 1, 'ro': 1}
        opt[self.spaceDict[space]] = 1
        return cmds.xform(self, **opt)

    def setRotation(self, args, space='world'):
        opt = {self.spaceDict[space]: 1}
        if len(args) > 1:
            opt['ro'] = args
        elif len(args) == 1:
            if isinstance(args[0], list):
                opt['ro'] = args[0]
        cmds.xform(self, **opt)

    def getScale(self, space='world'):
        opt = {'q': 1, 's': 1}
        opt[self.spaceDict[space]] = 1
        return cmds.xform(self, **opt)

    def setScale(self, args, space='world'):
        opt = {self.spaceDict[space]: 1}
        if len(args) > 1:
            opt['s'] = args
        elif len(args) == 1:
            if isinstance(args[0], list):
                opt['s'] = args[0]
        cmds.xform(self, **opt)

    def matchTransform(self, args, attrs=['t', 'r', 's']):
        attr_io = {
            't': {
                'get': lambda x: x.getTranslation(),
                'set': lambda x, v: x.setTranslation(*v)}, 
            'r': {
                'get': lambda x: x.getRotation(),
                'set': lambda x, v: x.setRotation(*v)}, 
            's': {
                'get': lambda x: x.getScale(),
                'set': lambda x, v: x.setScale(*v)}, 
        }
        for other in args:
            other = wrap(other)
            for at in attrs:
                v = attr_io[at]['get'](other)
                attr_io[at]['set'](self, v)

    def addParentNode(self, n='', nType='transform'):
        if n == '':
            n = self + "Par"

        try:
            par = cmds.createNode(nType, n=n)
        except:
            raise TypeError,'Don’t exists nodeType:' + nType

        cmds.parent(self, par, r=1)
        cur_par = self.getParent()
        if cur_par:
            cmds.parent(par, cur_par)
        else:
            cmds.parent(par, w=1)
        cmds.parent(self, par)
        return Transform(par)


def wrap(node):
    """wrapper function
    This function returns appropriate wrapper object from source node.
    """
    sels = OpenMaya.MSelectionList()
    sels.add(node)
    try:
        dag = sels.getDagPath(0)
        if dag.apiType() == getattr(OpenMaya.MFn, 'kTransform'):
            base_class = Transform
        else:
            base_class = DAGNode
        nodeType = cmds.objExists(node)
        wrap_class = type(utils.pascal_case(nodeType), (base_class,), dict(nodeType=nodeType))
        return wrap_class(node)
    except:
        pass
    return Node(node)
