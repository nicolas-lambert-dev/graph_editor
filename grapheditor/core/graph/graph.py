from abc import ABC, abstractmethod
from typing import Iterable, Callable

from grapheditor.core.event_system.event import IObservable
from grapheditor.core.event_system.event_types import EventType
from grapheditor.core.graph.graph_object import IGraphObject
from .edge import IEdge
from .node import INode
from ...core.graph.exceptions import ConnectionException


# Todo: Implement a basic TraversingIterator
class ITraversingIterator:
    """
    Iterate through a graph using specific algorithm
    """
    pass


class GraphEventType(EventType):
    """
    These are an exhaustive enum event IGraph can emit

    """
    ADD_NODE = "add_node"
    REMOVE_NODE = "remove_node"
    ADD_EDGE = "add_edge"
    REMOVE_EDGE = "remove_edge"


class IGraph(IGraphObject, ABC):
    """
        This is the public interface of a graph.

        As in graph theory, it is a set of nodes (vertices) connected by edges
        It gives basic methods to navigate threw it and sort nodes

    """

    @property
    @abstractmethod
    def events(self) -> IObservable[GraphEventType]:
        """
        Listening to this in order to react to IGraph events
        :return IObservable[GraphEventType]: IGraph observable
        """
        pass

    @property
    @abstractmethod
    def nodes(self) -> Iterable[INode]:
        """
        Return all the nodes in graph

        :return Iterable[INode]: All the nodes in the graph
        """
        pass

    @nodes.setter
    @abstractmethod
    def nodes(self, nodes: Iterable[INode]) -> None:
        """
        Replace graph nodes with the specified nodes

        :param nodes: The nodes to set
        """
        pass

    @property
    @abstractmethod
    def edges(self) -> Iterable[IEdge]:
        """
        Return all the edges in graph

        :return Iterable[IEdge]: All the edges in the graph
        """
        pass

    @abstractmethod
    def get_node_by_id(self, node_id: str) -> INode | None:
        """
        Retrieves a node by its uid

        :param str node_id:
        :return INode|None: the node if found
        """
        pass

    @abstractmethod
    def add_node(self, node: INode) -> INode:
        """
        Add the given node to the graph
        If a node with same id already exists, it will be used and returned.



        :param INode node: the node to add
        :return INode: the node provided or a node with same id already in graph
        :raises <IndexError>
        """
        pass

    @abstractmethod
    def remove_node(self, node_id: str) -> None:
        """
        Removes a node by its uid.
        If node is not in graph
        :param str node_id:
        """
        pass

    @abstractmethod
    def remove_edge(self, node: IEdge) -> None: pass

    @edges.setter
    @abstractmethod
    def edges(self, edges) -> None: pass

    @abstractmethod
    def connect(self, source: INode, target: INode) -> IEdge | ConnectionException:
        """
        Create en IEdge from source to target

        In case the connection is illegal, a ConnectionException is raised

        """
        pass

    @abstractmethod
    def traverse(self, source: INode, target: INode, callback: Callable, iterator: ITraversingIterator = None) -> None:
        """

        @iterator: ITraversingIterator  Default shortest path

        Traverse the graph from source to target (If path exists), using the iterator algorithm.
        Execute the callback passing the (current node, previous and future node) as arguments
        """
        pass

    @abstractmethod
    def shortest_path(self, source: INode, target: INode) -> Iterable[INode]:
        """

        Returns the shortest path between source and target
        [1]: https://en.wikipedia.org/wiki/Shortest_path_problem#Single-source_shortest_paths
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Return False if some graph rules are broken

        :rtype bool: Return False if some graph rules are broken
        """
        pass
