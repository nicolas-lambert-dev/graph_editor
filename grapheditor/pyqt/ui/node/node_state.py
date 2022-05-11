from abc import abstractmethod, ABC

from PyQt5.QtGui import QColor, QPainter, QBrush, QPen


class INodeState(ABC):
    """
    State pattern is used to draw the ::class:'NodeUI' depending on its current state
    ::meth::'paint' is called by the ::class::'NodeUI'

    """

    @abstractmethod
    def paint(self, node: 'NodeUI', painter: QPainter):
        """

        :param NodeUI node: The node to paint
        :param QPainter painter: A reference to the ::class::'NodeUI' QPainter
        """

        pass


class DefaultNodeState(INodeState):
    """
    Default drawing state for a ::clas:: 'NodeUI'
    """

    def paint(self, node: 'NodeUI', painter: QPainter):
        painter.setBrush(QColor("#225d70"))
        painter.drawRect(node.boundingRect())


class SelectedState(DefaultNodeState):
    """
    SelectedState drawing when a node is selected
    """

    def paint(self, node: 'NodeUI', painter: QPainter):
        painter.setBrush(QColor("#273f4f"))
        painter.setPen(QPen(QBrush(QColor("#111133")), 2))
        super().paint(node, painter)
