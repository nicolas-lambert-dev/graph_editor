from enum import Enum

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QPainter, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem

from grapheditor.core.geometry import Point2d
from grapheditor.ui.view.graph_ui import IGraphUI
from grapheditor.pyqt.ui.port_ui import PortUI

# Todo: Extract all constants to a conf file
from grapheditor.pyqt.wrappers.geometry_wrappers import QtPoint2d

BEZIER_TANGENT_OFFSET = 50
EDGE_DEFAULT_COLOR = "#ffffff"


class EdgePainter(Enum):
    LINE = 0
    BEZIER = 1


def line_painter(painter: QPainter, edge: 'EdgeUI'):
    painter.setPen(edge.pen)
    painter.drawLine(edge.source.scenePos(), edge.target.scenePos())


def bezier_painter(painter: QPainter, edge: 'EdgeUI'):
    painter.setPen(edge.pen)
    tangent_offset = QPointF(BEZIER_TANGENT_OFFSET, 0)
    source_pos = edge.source.scenePos()
    source_tangent = source_pos + tangent_offset
    target_pos = edge.target.scenePos()
    target_tangent = target_pos - tangent_offset
    path = QPainterPath()
    path.moveTo(source_pos)
    path.cubicTo(source_tangent, target_tangent, target_pos)
    painter.drawPath(path)


EDGE_PAINTERS = {
    EdgePainter.LINE: line_painter,
    EdgePainter.BEZIER: bezier_painter
}


class EdgeUI(QGraphicsItem, IGraphUI):

    EDGE_STYLE = EdgePainter.BEZIER

    def __init__(self, source: PortUI, target: PortUI, parent=None):
        super().__init__(parent=parent)
        self.source = source
        self.target = target

        self.pen = QPen(QColor(EDGE_DEFAULT_COLOR))
        self.pen.setWidth(2)
        self.setZValue(-10)

    def boundingRect(self) -> QtCore.QRectF:
        return QRectF(self.source.pos(), self.target.pos())

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget) -> None:
        EDGE_PAINTERS[self.EDGE_STYLE](painter, self)

    def set_position(self, position: Point2d):
        self.setPos(QPointF(position.x, position.y))