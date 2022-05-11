from abc import abstractmethod, ABC

from grapheditor.core.geometry import Point2d


class IGraphUI:
    """
    Base interface for all the graph item drawn in a ::class:: 'IGraphView'
    """

    @abstractmethod
    def set_position(self, position: Point2d):
        """
        Setting the position of the ::class:: 'GraphUI'

        :param Point2d position:
        """
        pass
