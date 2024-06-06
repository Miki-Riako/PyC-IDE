from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QLabel, QFrame, QMessageBox, QWidget, QVBoxLayout, QSplitter
from qfluentwidgets import CaptionLabel
from qfluentwidgets import PlainTextEdit, PushButton

class CommandLine(PlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Command Line\n")

class Workspace(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__()
        self.setupUi()
        self.setObjectName(text.replace(' ', '-'))
    
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveShortcut.activated.connect(self.save)
        self.runShortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.runShortcut.activated.connect(self.run)

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        
        # Top navigation placeholder
        self.topNav = CaptionLabel("Top Navigation Placeholder", self)
        self.topNav.setAlignment(Qt.AlignCenter)
        self.topNav.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.topNav.setFixedHeight(50)  # Adjust the height as needed

        # Middle code editor area
        self.edit = PlainTextEdit(self)
        self.edit.setPlaceholderText("Code Editor")

        # Bottom command line area
        self.commandLine = CommandLine(self)

        # Create a splitter for middle and bottom areas
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.edit)
        self.splitter.addWidget(self.commandLine)
        self.splitter.setSizes([400, 100])  # Initial sizes for the splitter

        self.layout.addWidget(self.topNav)
        self.layout.addWidget(self.splitter)

    def save(self):
        QMessageBox.information(self, "Save", "You pressed Ctrl+S. Waiting for save to be implemented...")
    def run(self):
        QMessageBox.information(self, "Run", "You pressed Ctrl+R. Waiting for run to be implemented...")
