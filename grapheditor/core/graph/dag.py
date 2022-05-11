from collections.abc import Iterable
from typing import Callable

from grapheditor.core.graph.graph_object import BaseGraphObject
from grapheditor.core.event_system.event import Observable, Event
from .node import INode
from ...core.graph.exceptions import ConnectionException, DependencyCycleException
import networkx as nx

from ...core.graph.graph import IEdge, IGraph, GraphEventType

import logging
logger = logging.getLogger(__name__)


class DirectedAcyclicGraph(BaseGraphObject, IGraph):
    """
    An implementation of a graph using the NetworkX library

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nodes_by_id = {}
        self.graph = nx.DiGraph()
        self._events = Observable[GraphEventType]()

    @property
    def events(self):
        return self._events

    @property
    def nodes(self) -> Iterable[INode]:
        return list(self.graph.nodes)

    @property
    def edges(self) -> Iterable[IEdge]:
        return list(self.graph.edges)

    def get_node_by_id(self, node_id: str) -> INode | None:

        if node_id in self._nodes_by_id:
            return self._nodes_by_id[node_id]
        else:
            return None

    def add_node(self, node: INode) -> INode | None:

        if node is None:
            raise IndexError("Cannot add None object to the graph")

        if node.uid in self._nodes_by_id:
            logger.warning(f"Node [{node.uid}] already exists in graph")
            return

        self._nodes_by_id[node.uid] = node
        self.graph.add_node(node)

        self.events.emit(GraphEventType.ADD_NODE, Event(self, {
            "added": node,
            "count": len(self.nodes)
        }))

        return node

    def remove_node(self, node_id: str) -> None:
        node = self.get_node_by_id(node_id)

        if node is None:
            raise LookupError(f"Trying to remove a Node [{node_id}] not existing in graph ")
            return

        self.graph.remove_node(node)
        self.events.emit(GraphEventType.REMOVE_NODE, Event(self, {
            "removed": node_id,
            "count": len(self.nodes)
        }))

    def remove_edge(self, edge: IEdge) -> None:
        self.graph.remove_edge(edge.source, edge.target)
        self.events.emit(GraphEventType.REMOVE_EDGE, Event(self, {
            "removed": edge.uid,
            "count": len(self.edges)
        }))

    def connect(self, source: INode, target: INode) -> None | ConnectionException:
        self.graph.add_edge(source, target)

        if self.have_some_cycle():
            raise DependencyCycleException(source, target)
        elif not self.is_valid():
            raise ConnectionException()

        self.events.emit(GraphEventType.ADD_EDGE, Event(self, {
            "source": source,
            "target": target,
            "count": len(self.edges)
        }))

    def traverse(self, callback: Callable[[INode], None]) -> None:
        nodes = self.topological_sort()
        for node in nodes:
            callback(node)

    def is_valid(self) -> bool:
        return not self.have_some_cycle()

    def have_some_cycle(self) -> bool:
        return not self.graph.is_directed()

    def shortest_path(self, source: INode, target: INode) -> Iterable[INode]:
        return list(nx.topological_sort(self.graph))
