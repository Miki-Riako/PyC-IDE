# pages/workspace.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCompleter
from qfluentwidgets import PlainTextEdit, PushButton, setTheme, Theme

class Workspace(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__()
        self.setupUi()
        self.setObjectName(text.replace(' ', '-'))

    def setupUi(self):
        self.Layout = QVBoxLayout(self)
        self.edit = PlainTextEdit(self)
        self.Layout.addWidget(self.edit)

# pages/end workspace.py