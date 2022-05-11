from PyQt5.QtWidgets import QApplication

from grapheditor.pyqt.graph_editor_widget import QtGraphEditorWidget
import logging
logging.basicConfig(level=logging.DEBUG)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)

    graph_editor = QtGraphEditorWidget()
    graph_editor.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    sys.excepthook = except_hook

    main()