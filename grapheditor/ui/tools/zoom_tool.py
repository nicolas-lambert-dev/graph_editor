from grapheditor.ui.tools.pan_tool import PanTool
from grapheditor.ui.view.graph_view_events import WheelMouseEvent


class ZoomTool(PanTool):
    """
    In charge of zoom/dezoom in the graph view
    """

    NAME = "ZoomTool"

    def __init__(self, view: 'IEditorView'):
        super().__init__(view)
        self.name = "Zoom Tool"
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_in_factor = 1.25

    def on_wheel_event(self, event: WheelMouseEvent):

        # zoom in
        if event.angle_delta.y > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step

        # zoom out
        else:
            zoom_factor = 1 / self.zoom_in_factor
            self.zoom -= self.zoom_step

        self.view.scale(zoom_factor, zoom_factor)