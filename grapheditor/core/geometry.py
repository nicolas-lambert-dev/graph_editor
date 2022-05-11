from abc import abstractmethod, ABC


class IPoint2d(ABC):
    """
    Interface for a point in 2d coordinate

    """

    @property
    @abstractmethod
    def x(self) -> float: pass

    @property
    @abstractmethod
    def y(self) -> float: pass


class Point2d(IPoint2d):
    """
    Simplest implementation of a Point 2d
    It's just a DTO holding x and y, without any methods

    """

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y
