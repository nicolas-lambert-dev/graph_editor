from abc import ABC, abstractmethod

from grapheditor.core.geometry import Point2d
from grapheditor.ui.model.graph_scene import IGraphScene
from grapheditor.ui.tools.tool import IEditorTool
from grapheditor.ui.view.graph_ui import IGraphUI


class IEditorView(ABC):

    @abstractmethod
    def set_scale(self, x: int, y: int): pass

    @abstractmethod
    def enable_dragmode(self, active: bool): pass

    @abstractmethod
    def register_tool(self, tool: IEditorTool): pass

    @abstractmethod
    def get_tool_by_name(self, name: str) -> IEditorTool | None: pass

    @property
    @abstractmethod
    def current_tool(self) -> IEditorTool: pass

    @current_tool.setter
    @abstractmethod
    def current_tool(self, tool: IEditorTool) -> IEditorTool: pass

    @abstractmethod
    def get_item_at(self, position: Point2d) -> IGraphUI: pass

    @abstractmethod
    def map_to_scene(self, position: Point2d) -> Point2d:
        """
        Convert any position in the graphicScene coordinates

        :param Point2d position: position on any coordinates
        :return Point2d: position mapped to world coordinates
        """
        pass

    @abstractmethod
    def set_scene(self, scene: IGraphScene): pass


class AbstractEditorView(IEditorView, ABC):

    def __init__(self):
        self._current_tools = {}
        self._current_tool = None

    def register_tool(self, tool: IEditorTool):
        """
        When registered, the tool is usable in the view

        """

        # The first tool is the default
        if not self._current_tools:
            self._current_tool = tool

        self._current_tools[tool.NAME] = tool
        tool.on_registered(self)

    @property
    def current_tool(self) -> IEditorTool:
        return self._current_tool

    @current_tool.setter
    def current_tool(self, tool: IEditorTool) -> IEditorTool:
        self.current_tool.on_stop()
        self._current_tool = tool
        self.current_tool.on_start()

    def get_tool_by_name(self, tool_name: str) -> IEditorTool | None:
        """
        Return the view tool by its name, if it is registered

        """
        if tool_name in self._current_tools:
            return self._current_tools[tool_name]

