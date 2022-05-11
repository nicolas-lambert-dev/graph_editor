import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, QPoint, QPointF
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem

from grapheditor.core.geometry import Point2d
from grapheditor.ui.view.graph_ui import IGraphUI
from grapheditor.pyqt.ui.node.node_state import DefaultNodeState, SelectedState


class NodeLabel(QGraphicsTextItem):
    """
    Node label as a TextItem

    """

    def __init__(self, text: str, parent: 'NodeUI' = None):
        super().__init__(parent)

        self.setPlainText(text)
        font = QFont('Helvetica')
        font.setPixelSize(15)
        self.setFont(font)
        self.setDefaultTextColor(QColor("#ffffff"))


class NodeUI(QGraphicsItem, IGraphUI):
    min_width = 80
    min_height = 125

    def __init__(self, label: str, parent=None):
        super().__init__(parent)

        self._label = ""
        self._rect = QRectF(-self.min_width // 2, -self.min_height // 2, self.min_width, self.min_height)
        self.padding = QPoint(5, 5)
        self.port_padding = QPoint(5, 5)
        self.label_item = NodeLabel(label, parent=self)
        self.init_layout()
        self.label = label
        self.state = DefaultNodeState()

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label
        self.label_item.setPlainText(label)

        label_rect = self.label_item.boundingRect()

        if label_rect.width() > self.boundingRect().width():
            width = label_rect.width() + self.padding.x()
            height = self._rect.height()
            self._rect = QRectF(width//2, height//2, width, height)
            self.init_layout()

    def init_layout(self):
        self.label_item.setPos(self.boundingRect().topLeft() + self.padding)

    def boundingRect(self) -> QRectF:
        return self._rect

    def itemChange(self, change: 'QGraphicsItem.GraphicsItemChange', value: typing.Any) -> typing.Any:

        if change == QGraphicsItem.ItemSelectedChange:
            self.state = SelectedState() if value == 1 else DefaultNodeState()

        return super().itemChange(change, value)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:

        self.state.paint(self, painter)

    def set_position(self, position: Point2d) -> None:
        self.setPos(QPointF(position.x, position.y))
