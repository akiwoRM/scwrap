# -*- coding:utf-8 -*-
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
        return super(Attribute, cls).__new__(cls, cls._node+"."+cls._attr)


class Node(unicode):
    def __getattr__(self, attr):
        return Attribute(self, attr)