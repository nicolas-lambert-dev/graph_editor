from abc import ABC

from grapheditor.ui.model.edge import Edge
from grapheditor.ui.model.graph_scene import IGraphScene
from grapheditor.ui.model.node import Node


class AbstractGraphEditor(ABC):

    def __init__(self, graph_scene: IGraphScene):
        """
        AbstractGraphEditor constructor
        For a concrete class, it needs a concrete grap_scene.

        :param IGraphScene graph_scene: The concrete class to inject
        """

        self.graph_scene = graph_scene
        self.nodes = []
        self.edges = []

    def add_node(self, node: Node) -> None:
        self.graph_scene.add_item(node.ui)
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        self.graph_scene.add_item(edge.ui)
        self.edges.append(edge)

    def from_json(self, json_data: dict):

        for node_json in json_data["scene"]["nodes"]:
            node = Node.from_json(node_json)
            self.add_node(node)

        for edge_json in json_data["scene"]["edges"]:
            edge = Edge.from_json(edge_json)
            self.add_edge(edge)

        print('Deserialized')

