from grapheditor.core.graph.graph_object import BaseGraphObject
from grapheditor.pyqt.ui.port_ui import PortUI
import json


class Port(BaseGraphObject):
    """
    ViewModel glue for a Port

    It is an attribute of a ::class:: 'Node'
    """

    def __init__(self, name: str = "", node: 'Node' = None, is_output: bool = False, uid: str = None):
        super().__init__(uid)

        self.name = name
        self._node = node
        self.is_output = is_output
        self.ui = PortUI(label=name, parent=node.ui) if node else None

    @property
    def node(self) -> 'Node':
        return self.node

    @node.setter
    def node(self, node: 'Node') -> None:
        self._node = node

        # update ui parent
        if self.ui:
            self.ui = self.ui.node = node
        else:
            self.ui = PortUI(label=self.name, parent=node.ui)

    @property
    def height(self) -> int:
        return self.ui.height

    def __repr__(self):
        return f"Port[{self.uid}]"

    @classmethod
    def from_json(cls, json_dict: dict) -> 'Port':
        port = Port()

        port.uid = json_dict["uid"]
        port.name = json_dict["name"]

        return port

