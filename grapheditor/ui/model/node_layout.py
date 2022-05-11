from grapheditor.pyqt.ui.port_ui import LabelSide


def default_layout_ports(node: 'Node') -> None:
    """
    Input ports are drawn on left side of the node and outputs n the right side

    :param node: The node that hold the layout
    """

    node_ui = node.ui
    node_rect = node_ui.boundingRect()
    top_left = (-node_rect.width()/2, -node_rect.height()/2 + 50)
    top_right = (node_rect.width()/2, -node_rect.height()/2 + 50)

    for i, input_port in enumerate(node.inputs):
        x = top_left[0]
        y = top_left[1] + i * (input_port.height + node_ui.port_padding.y())
        input_port.ui.setX(x)
        input_port.ui.setY(y)

    for i, output_port in enumerate(node.outputs):
        x = top_right[0]
        y = top_right[1] + i * (input_port.height + node_ui.port_padding.y())
        output_port.ui.setX(x)
        output_port.ui.setY(y)
        output_port.ui.label_side = LabelSide.RIGHT
