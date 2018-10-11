# -*- coding:utf-8 -*-
from . import general
from . import utils
"""
This module is dynamic node wrapeer class
"""


class NodeCall(object):
    def __getattr__(self, nodeType):
        if nodeType in dir(general):
            """
            generalモジュールに指定のノードクラスがあれば
            そのノードクラスを返す。
            そのためgeneralモジュールにはノードクラスのみを定義する必要がある。
            現状ではそうなっていないためリファクタリングする、あるいは取得の仕方を変更する必要がある。
            取得したものがクラスかどうか、nodeTypeメンバー変数を持つかを調べる。
            """
            NodeClass = getattr(general, nodeType)
        else:
            NodeClass = type(utils.pascal_case(nodeType), (general.Node,), dict(nodeType=utils.camel_case(nodeType)))
        return NodeClass

node = NodeCall()