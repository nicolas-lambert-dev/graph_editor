from dataclasses import dataclass


@dataclass
class Style:
    background_color: str = "#444444"
    stroke_color: str = "#ff0000"


class GraphSceneStyle(Style):
    pass


class NodeStyle(GraphSceneStyle):
    selected_color: str = "#cc0000"

