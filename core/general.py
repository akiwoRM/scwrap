# -*- coding:utf-8 -*-
try:
    import unicode
except:
    unicode = str


class Attribute(unicode):
    pass


class Node(unicode):
    def __getattr__(self, attr):
        return Attribute(self, attr)