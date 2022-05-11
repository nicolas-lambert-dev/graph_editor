from abc import ABC, abstractmethod
from grapheditor.ui.view.graph_view_events import EditorMouseEvent, WheelMouseEvent

import logging
logger = logging.getLogger(__name__)


class IEditorTool(ABC):
    """
    Tool interface for the ::clas::'AbstractEditorView'
    The view delegates user events t the current ::class:: 'IEditorTool'
    """

    NAME: str

    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def view(self) -> 'IEditorView' : pass

    @abstractmethod
    def on_registered(self, view: 'IEditorView'): pass

    @abstractmethod
    def on_start(self): pass

    @abstractmethod
    def on_stop(self): pass

    @abstractmethod
    def on_mouse_press(self, event: EditorMouseEvent): pass

    @abstractmethod
    def on_mouse_release(self, event: EditorMouseEvent): pass

    @abstractmethod
    def on_wheel_event(self, event: WheelMouseEvent): pass

    @abstractmethod
    def on_mouse_move(self, event: EditorMouseEvent): pass

    @abstractmethod
    def commit(self) -> None: pass

    @abstractmethod
    def rollback(self) -> None: pass


class AbstractEditorTool(IEditorTool, ABC):

    @abstractmethod
    def __init__(self, name: str, view: 'IEditorView'):
        self._view = view
        self._name = name

    def name(self) -> str:
        return self._name

    def view(self) -> 'IEditorView':
        return self._view

    def on_registered(self, view: 'IEditorView'):
        self._view = view

    def on_start(self):
        logger.debug(f"Tool [{self.name}] started")

    def on_stop(self):
        logger.debug(f"Tool [{self.name}] stopped")

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
