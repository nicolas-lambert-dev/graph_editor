from typing import TYPE_CHECKING

from grapheditor.pyqt.ui.edge_ui import EdgeUI
from grapheditor.pyqt.ui.port_ui import PortUI

if TYPE_CHECKING:
    from grapheditor.ui.view.graph_view import IEditorView


from grapheditor.core.geometry import Point2d
from grapheditor.ui.tools.pan_tool import PanTool

import logging
logger = logging.getLogger("drag_edge_tool")


class DragEdgeTool(PanTool):
    """
    Draw a temporary edge, between a por::class::'PortUI' ans the mouse.
    Delegates connection validation to the graph model.
    In case connection is valid, it instantiates the edge in graph
    """

    NAME = "DragEdgeTool"

    def __init__(self, view: 'IEditorView'):
        super().__init__(view)
        self.start_drag_position: Point2d = None

        self.dragging_edge: EdgeUI = None
        self.dragging_target: PortUI = None

    def on_mouse_press(self, event: 'EditorMouseEvent'):
        self.dragging_target = PortUI("target_port")
        self.dragging_target.setVisible(False)
        self.dragging_target.set_position(self.view.map_to_scene(event.position))
        self.dragging_edge = EdgeUI(self.view.get_item_at(event.position), self.dragging_target)
        self.view.scene().addItem(self.dragging_edge)

    def on_mouse_release(self, event: 'EditorMouseEvent'):

        if self.dragging_edge:
            is_valid_edge = self.validate_edge_connection()

            if is_valid_edge:
                self.commit()
            else:
                self.rollback()

        self.view.current_tool = self.view.get_tool_by_name(PanTool.NAME)

    def on_mouse_move(self, event: 'EditorMouseEvent'):
        logger.debug(event.position)
        self.dragging_target.set_position(self.view.map_to_scene(event.position))
