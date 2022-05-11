from typing import Any

from grapheditor.core.graph.graph_object import BaseGraphObject

from abc import ABC, abstractmethod


class INode(ABC):
    """
    This is the interface of a node

    A node is part of a graph, and can contain any kind of data.
    Connected by edges, it provides some helpers to travers the graph from it.

    """

    @property
    @abstractmethod
    def data(self): pass

    """
    This is the data embedded by the node, it could be any ing of data.
    The main purpose of data is binding any object to the node behavior.
    Ex: node.data = Task()

    """

    @data.setter
    @abstractmethod
    def data(self): pass


class Node(INode, BaseGraphObject):
    """
    This is the simplest implementation of a node.
    It serves to contain any kind of data.

    """

    def __init__(self, data: Any, graph: 'IGraph'= None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = data
        self._graph = graph

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
