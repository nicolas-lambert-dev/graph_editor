import math

from PyQt5.QtCore import QRect, QLine
from PyQt5.QtGui import QColor, QPainter, QPen


class GridUI:

    def __init__(self, size: int = 20, nb_squares: int = 5, light_color: QColor = None, dark_color: QColor = None):

        self.size = size
        self.nb_squares = nb_squares

        self.light_pen = QPen(light_color if light_color is not None else QColor("#333333"))
        self.dark_pen = QPen(dark_color if dark_color is not None else QColor("#000000"))

    # Todo extract lines creation logic to a generic grid generator and only implement drawing in this class
    def draw(self, painter: QPainter, region: QRect):

        left = int(math.floor(region.left()))
        right = int(math.ceil(region.right()))
        top = int(math.floor(region.top()))
        bottom = int(math.ceil(region.bottom()))

        first_left = left - (left % self.size)
        first_top = top - (top % self.size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.size):

            if x % (self.size * self.nb_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.size):

            if y % (self.size * self.nb_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self.light_pen)
        painter.drawLines(*lines_light)
        painter.setPen(self.dark_pen)
        painter.drawLines(*lines_dark)



