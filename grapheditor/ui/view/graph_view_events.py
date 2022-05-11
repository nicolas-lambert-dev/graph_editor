from dataclasses import dataclass
from enum import Enum

from grapheditor.core.geometry import IPoint2d


class MouseButton(Enum):
    NONE = "none"
    LEFT = "left"
    MIDDLE = "middle"
    RIGHT = "right"


@dataclass
class EditorMouseEvent:
    button: MouseButton
    position: IPoint2d


@dataclass
class WheelMouseEvent:
    angle_delta: IPoint2d
    position: IPoint2d
