import json

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from grapheditor.pyqt.graph_editor import QtGraphEditor
from grapheditor.pyqt.ui.graph_scene import QtGraphScene
from grapheditor.pyqt.ui.graph_view import QtGraphView


class QtGraphEditorWidget(QWidget):
    """
    GraphEditor pyqt widget

    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.editor = QtGraphEditor(QtGraphScene())
        self.view = QtGraphView(self.editor.graph_scene)

        self._layout = QVBoxLayout()
        self.init_layout()
        self._add_dummydata()

    def init_layout(self):
        self.setWindowTitle("Graph Editor")
        self.setGeometry(200, 200, 800, 600)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.layout().addWidget(self.view)

    def _add_dummydata(self):

        import os
        print (os.getcwd())
        dummy_data_str = open("dummy_data.json", "r").read()
        dummy_data = json.loads(dummy_data_str)

        self.editor.from_json(dummy_data)



