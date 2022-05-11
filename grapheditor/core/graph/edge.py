from abc import ABC

from grapheditor.core.graph.graph_object import BaseGraphObject, IGraphObject
from grapheditor.core.graph.node import INode


class IEdge(IGraphObject, ABC):
    """
    An Edge is the relation between 2 Nodes in a graph

    """

    source: INode
    target: INode


class Edge(IEdge, BaseGraphObject):
    """
    As in graph theory, an edge represent a connection between two nodes
    It is directed, so it has a source and a target node giving its direction

    """

    def __init__(self, source: 'INode', target: 'INode', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source = source
        self.target = target
