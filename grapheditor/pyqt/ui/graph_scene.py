from PyQt5.QtCore import QObject, QRect
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QGraphicsScene

from grapheditor.ui.model.graph_scene import IGraphScene
from grapheditor.ui.style import GraphSceneStyle
from grapheditor.ui.view.graph_ui import IGraphUI
from grapheditor.pyqt.ui.grid_ui import GridUI


class Meta(type(QGraphicsScene), type(IGraphScene)): pass


class QtGraphScene(QGraphicsScene, IGraphScene, metaclass=Meta):
    """
    A PyQt implementation of the GraphicScene

    """

    def __init__(self, parent: QObject = None, palette: GraphSceneStyle = None):
        super().__init__(parent)

        self._width = 100000
        self._height = 100000
        self.palette = palette if palette is not None else GraphSceneStyle()

        self.grid_ui = GridUI()
        self.gridSize = 20
        self.gridSquares = 5

        self.init_qt_settings()

    def init_qt_settings(self):
        """
        Init Qt specific settings

        """

        self.setSceneRect(-self._width//2, -self._height//2, self._width, self._height)
        self.setBackgroundBrush(QColor(self.palette.background_color))

    def drawBackground(self, painter: QPainter, rect: QRect):
        super().drawBackground(painter, rect)

        self.grid_ui.draw(painter, rect)

    def as_QGraphicsScene(self) -> QGraphicsScene:
        """
        QGraphicsScene casting
        :return QGraphicsScene: self as a QGraphicsScene
        """

        return self

    def add_item(self, graph_item: IGraphUI) -> None:
        self.addItem(graph_item)



