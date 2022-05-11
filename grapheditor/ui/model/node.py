from typing import Iterable

from grapheditor.core.geometry import Point2d
from grapheditor.core.graph.graph_object import BaseGraphObject
from grapheditor.ui.model.node_layout import default_layout_ports
from grapheditor.ui.model.port import Port
from grapheditor.pyqt.ui.node.node_ui import NodeUI

import logging
logger = logging.getLogger(__name__)


class Node(BaseGraphObject):
    """
    ViewModel glue for a Node. Main Entity of a graph

    """

    def __init__(self, name: str, uid: str = None):
        super().__init__(uid)

        self.name = name
        self.ui = NodeUI(name)

        self._input_by_uid = {}
        self._output_by_uid = {}

        self._inputs = []
        self._outputs = []

        default_layout_ports(self)

    @property
    def inputs(self) -> Iterable[Port]:
        return self._inputs

    @property
    def outputs(self) -> Iterable[Port]:
        return self._outputs

    def update(self):
        default_layout_ports(self)

    def contains_port(self, port: Port) -> bool:
        return (port.uid in self._input_by_uid) or (port.uid in self._output_by_uid)

    def add_input(self, port: Port) -> None:

        if self.contains_port(port):
            logger.warning(f"Port[{port.uid}] already exists in Node[{self.uid}]")
            return None

        port.node = self
        self._input_by_uid[port.uid] = port
        self._inputs.append(port)

        self.update()

    def add_output(self, port: Port) -> None:

        if self.contains_port(port):
            logger.warning(f"Port[{port.uid}] already exists in Node[{self.uid}]")
            return None

        port.node = self
        self._output_by_uid[port.uid] = port
        self._outputs.append(port)

        self.update()

    def get_input_by_uid(self, uid: str) -> Port | None:
        """
            Return port by its uid if it exists in inputs

            :param str uid: ::class::'PortUI' uid
            :return Port | None: found port or None
        """

        if uid not in self._input_by_uid:
            logger.warning(f"Could not found Port[{uid}] in Node[{self.uid}] inputs")
            return None

        return self._input_by_uid[uid]

    def get_output_by_uid(self, uid: str) -> Port | None:
        """
            Return port by its uid if it exists in outputs

            :param str uid: ::class::'PortUI' uid
            :return Port | None: found port or None
        """

        if uid not in self._output_by_uid:
            logger.warning(f"Could not found Port[{uid}] in Node[{self.uid}] inputs")
            return None

        return self._output_by_uid[uid]

    @classmethod
    def from_json(cls, json_dict: dict) -> 'Node':
        node = Node(name=json_dict["name"], uid=json_dict["uid"])
        node.ui.set_position(Point2d(json_dict["position"][0], json_dict["position"][1]))

        for port_json in json_dict["inputs"]:
            in_port = Port.from_json(port_json)
            node.add_input(in_port)

        for port_json in json_dict["outputs"]:
            out_port = Port.from_json(port_json)
            node.add_output(out_port)

        return node


