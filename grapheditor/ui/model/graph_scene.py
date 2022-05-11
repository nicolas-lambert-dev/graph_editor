from abc import ABC, abstractmethod

from grapheditor.ui.view.graph_ui import IGraphUI


class IGraphScene:
    """
    A graph ui model representation. It have it's own coordinates system

    """

    @abstractmethod
    def add_item(self, graph_item: IGraphUI) -> None: pass