from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtCore import Qt

from grapheditor.pyqt.wrappers.geometry_wrappers import QtPoint2d
from grapheditor.ui.view.graph_view_events import EditorMouseEvent, MouseButton, WheelMouseEvent

mouse_buttons_mapping = {
    Qt.NoButton: MouseButton.NONE,
    Qt.LeftButton: MouseButton.LEFT,
    Qt.MidButton: MouseButton.MIDDLE,
    Qt.RightButton: MouseButton.RIGHT
}


def qtmouse_event_to_mousebutton(qt_event: QMouseEvent):
    return mouse_buttons_mapping[qt_event.button()]


def from_mouseevent(event: QMouseEvent) -> EditorMouseEvent:
    button = qtmouse_event_to_mousebutton(event)
    position = QtPoint2d(event.pos())
    return EditorMouseEvent(button, position)


def from_wheelevent(event: QWheelEvent) -> WheelMouseEvent:
    angle_delta = QtPoint2d(event.angleDelta())
    position = QtPoint2d(event.pos())
    return WheelMouseEvent(angle_delta, position)
