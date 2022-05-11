from grapheditor.ui.tools.tool import AbstractEditorTool
from grapheditor.ui.view.graph_view_events import WheelMouseEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grapheditor.pyqt.ui.graph_view import GraphView


class PanTool(AbstractEditorTool):
    """
    In charge of panning the graph view
    This is the default tool, all handlers not overriding by others tools is managed by ::class::'PanTool'

    """

    NAME = "PanTool"

    def __init__(self, view: 'GraphView'):
        super().__init__("Pan Tool", view)

    @property
    def view(self) -> 'GraphView':
        return self._view

    def on_mouse_press(self, event: 'EditorMouseEvent'):
        self.view.enable_dragmode(True)

    def on_mouse_release(self, event: 'EditorMouseEvent'):
        self.view.enable_dragmode(False)

    def on_wheel_event(self, event: WheelMouseEvent):
        pass

    def on_mouse_move(self, event: 'EditorMouseEvent'):
        pass
