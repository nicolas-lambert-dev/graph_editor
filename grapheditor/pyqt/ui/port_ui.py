import typing
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QBrush, QPen, QFont, QFontMetrics
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem

from grapheditor.core.geometry import Point2d
from grapheditor.ui.view.graph_ui import IGraphUI


class LabelSide(Enum):
    LEFT = "Left"
    RIGHT = 'Right'


class PortUI(QGraphicsItem, IGraphUI):
    """
    Graphical representation of a node port

    """

    def __init__(self, label: str, parent=None, label_side: LabelSide = LabelSide.LEFT):
        super().__init__(parent=parent)

        self.radius = 5
        self.background_brush = QBrush(QColor("#e0764c"))
        self.stroke_pen = QPen(QColor("#000000"))
        self.font = QFont('Helvetica', 5)
        self.label = label

        self._label_side = label_side
        self.label_item = QGraphicsTextItem(label, parent=self)
        self.label_item.setFont(self.font)
        self.set_label_position()
        self.label_item.setDefaultTextColor(QColor("#ffffff"))

    @property
    def height(self):
        return self.radius * 2

    @property
    def label_side(self) -> LabelSide:
        return self._label_side

    @label_side.setter
    def label_side(self, side: LabelSide):
        self._label_side = side
        self.set_label_position()

    def set_label_position(self):
        font_metrics = QFontMetrics(self.font)
        label_x = 5

        if self.label_side == LabelSide.RIGHT:
            label_x = - font_metrics.horizontalAdvance(self.label) - self.radius * 2 - 5

        self.label_item.setX(label_x)
        self.label_item.setY(-font_metrics.height())

    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...) -> None:

        painter.setBrush(self.background_brush)
        painter.setPen(self.stroke_pen)
        painter.drawEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def set_position(self, position: Point2d) -> None:
        self.setPos(QPointF(position.x, position.y))
