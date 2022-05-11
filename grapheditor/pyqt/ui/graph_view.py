from typing import cast

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.uic.properties import QtGui

from grapheditor.core.geometry import Point2d
from grapheditor.ui.model.graph_scene import IGraphScene

from grapheditor.ui.tools.drag_edge_tool import DragEdgeTool
from grapheditor.ui.tools.pan_tool import PanTool
from grapheditor.ui.tools.zoom_tool import ZoomTool
from grapheditor.ui.view.graph_ui import IGraphUI
from grapheditor.ui.view.graph_view import AbstractEditorView
from grapheditor.pyqt.ui.graph_scene import QtGraphScene
from grapheditor.pyqt.ui.graph_view_events import from_mouseevent, from_wheelevent
from grapheditor.pyqt.ui.port_ui import PortUI
from grapheditor.pyqt.wrappers.geometry_wrappers import QtPoint2d

import logging
logger = logging.getLogger("graph_view")


class Meta(type(AbstractEditorView), type(QGraphicsView)): pass


class QtGraphView(QGraphicsView, AbstractEditorView, metaclass=Meta):
    """
    The view in charge of presenting and interacting with graph model objects
    User interaction events are delegated to ::class:: IEditorTool

    """

    def __init__(self, graphic_scene: QtGraphScene, parent=None):

        super().__init__(parent=parent)

        self.graphic_scene = graphic_scene
        self.set_scene(graphic_scene)
        self.init_qt_settings()

        # Todo: extract tools registration in a ToolRegistry
        self.register_tool(PanTool(self))
        self.register_tool(ZoomTool(self))
        self.register_tool(DragEdgeTool(self))
        self.current_tool = self.get_tool_by_name(PanTool.NAME)
        self._zoom_factor = 1

        self._dragging_edge = None
        self._dragging_target_port = None

    def set_scale(self, x: int, y: int):
        self.scale(x, y)

    def init_qt_settings(self):
        """
        Initialize all the specific qt settings for the view behavior

        """
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)

    def enable_dragmode(self, enable: bool):
        """
        Activate/Deactivate the builtin ScrollHandDrag drag mode of QGraphicsView

        """
        if enable:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)

    def mousePressEvent(self, event: 'QtGui.QMouseEvent') -> None:
        """
        Delegate the mousePressEvent's QGraphicsView events to the current IEditorTool

        """

        if event.button() == Qt.MidButton:
            self.current_tool = self.get_tool_by_name(PanTool.NAME)

        self.current_tool.on_mouse_press(from_mouseevent(event))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: 'QtGui.QMouseEvent') -> None:
        """
        Delegate the mouseReleaseEvent's QGraphicsView events to the current IEditorTool

        """
        self.current_tool.on_mouse_release(from_mouseevent(event))

        item = self.itemAt(event.pos())

        if item:
            logger.debug(f"{item.pos()}")

        super().mouseReleaseEvent(event)

    def wheelEvent(self, event: 'QtGui.QWheelEvent') -> None:
        """
        Delegate the wheelEvent's QGraphicsView events to the current IEditorTool

        """
        self.current_tool = self.get_tool_by_name(ZoomTool.NAME)
        wheel_event = from_wheelevent(event)
        self.current_tool.on_wheel_event(wheel_event)

    def mouseMoveEvent(self, event: 'QtGui.QMouseEvent') -> None:
        """
        Delegate the mouseMoveEvent's QGraphicsView events to the current IEditorTool

        """
        self.current_tool.on_mouse_move(from_mouseevent(event))
        return super().mouseMoveEvent(event)

    def get_item_at(self, position: Point2d) -> IGraphUI | None:
        """
        Fetch the first graph item on this position

        :param Point2d position: position to look at
        :return IGraphUI: the first item under this position
        """

        item = self.itemAt(QPoint(position.x, position.y))
        logger.debug(f"get_item_at: {item}")

        if isinstance(item, IGraphUI):
            return item

    def map_to_scene(self, position: Point2d) -> Point2d:
        """
        Fetch the first graph item on this position

        :param Point2d position: position to look at
        :return IGraphUI: the first item under this position
        """

        scene_pos = self.mapToScene(QPoint(position.x, position.y))
        return Point2d(scene_pos.x(), scene_pos.y())

    def set_scene(self, scene: QtGraphScene):
        self.setScene(scene)
