from grapheditor.core.graph.graph_object import BaseGraphObject
from grapheditor.core.graph.graph import IEdge
from grapheditor.pyqt.ui.edge_ui import EdgeUI
from grapheditor.ui.model.port import Port


class Edge(BaseGraphObject, IEdge):
    """
    ViewModel glue for an Edge (Nodes relation)
    """

    def __init__(self, source: Port, target: Port, uid: str = None):
        super().__init__(uid)

        self.source = source
        self.target = target
        self.ui = EdgeUI(source.ui, target.ui)

    @classmethod
    def from_json(cls, json_dict: dict) -> 'Edge':
        edge = Edge(
            uid=json_dict["uid"],
            source=BaseGraphObject.objects_by_uuid[json_dict["source"]],
            target=BaseGraphObject.objects_by_uuid[json_dict["target"]]
        )
        return edge
