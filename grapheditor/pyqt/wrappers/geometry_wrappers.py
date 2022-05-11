from PyQt5.QtCore import QPointF

from grapheditor.core.geometry import Point2d


class QtPoint2d(Point2d):
    """
    Wrap QPointF to a more generic Point2d class

    """

    def __init__(self, qt_point: QPointF):
        self._point = qt_point

    @property
    def x(self) -> float:
        return self._point.x()

    @x.setter
    def x(self, x: float):
        self._point.setX(x)

    @property
    def y(self) -> float:
        return self._point.y()

    @y.setter
    def y(self, y: float):
        self._point.setY(y)

    def __repr__(self):
        return f"{__class__}: (x: {self.x}, y: {self.y})"
