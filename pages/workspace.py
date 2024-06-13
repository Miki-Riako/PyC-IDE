from _compiler import Compiler
from PySide6.QtCore import Qt, QSize, QUrl, QPoint, QRegularExpression
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QDesktopServices, QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import (
    QApplication, QLabel, QFrame, QMessageBox,
    QWidget, QVBoxLayout,  QHBoxLayout, QVBoxLayout,
    QStackedWidget
    )
from qfluentwidgets import (
    CaptionLabel, PlainTextEdit, PushButton, CheckBox, BodyLabel, SpinBox, ComboBox, qrouter,
    NavigationItemPosition, MessageBox, TabBar, SubtitleLabel, setFont, TabCloseButtonDisplayMode, IconWidget,
    TransparentDropDownToolButton, TransparentToolButton, setTheme, Theme, isDarkTheme
    )
from qfluentwidgets import FluentIcon as FIF

DEBUG_MODE = True

class KeywordHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.call_format = QTextCharFormat()
        self.call_format.setForeground(QColor(255, 215, 00))
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(230, 57, 70))
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(180, 248, 200))
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(112, 214, 255))

        self.keywords = [
            'int',   'void', 'break', 'float',  'while', 'do',      'struct',
            'const', 'case', 'for',   'return', 'if',    'default', 'else',
            'char', 'double'
        ]

        self.string_patterns = [
            QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'),
            QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        ]

        self.function_pattern = QRegularExpression(r'\b(?:int|void|float|char|double)\s+(\w+)\s*\(')
        self.call_pattern = QRegularExpression(r'\b(\w+)\s*\(')

    def highlightBlock(self, text):
        expression = QRegularExpression(self.call_pattern)
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            if self.format(match.capturedStart(1)) != self.function_format:
                self.setFormat(match.capturedStart(1), match.capturedLength(1), self.call_format)

        expression = QRegularExpression(self.function_pattern)
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.function_format)

        for word in self.keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        for pattern in self.string_patterns:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

class Workspace(QWidget):
    def __init__(self, text: str, controller, parent=None):
        super().__init__(parent=parent)
        self.controller = controller

        self.vBoxLayout = QVBoxLayout(self)
        self.tabBoxLayout = QHBoxLayout(self)
        self.tabBar = TabBar(self)
        self.runButton = TransparentToolButton(FIF.PLAY.icon(color=QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)), self)
        self.stackedWidget = QStackedWidget(self)

        self.new_edit = PlainTextEdit(self)
        self.new_edit.setPlaceholderText("New code...")

        code = 'int main() {\n    int num;\n    int a;\n    num = 2;\n    if (num > 0) {\n        a = num;\n    } else {\n        a = 1;\n    }\n}'
        self.new_edit.setPlainText(code)
        
        self.__initWidget()
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.saveShortcut.activated.connect(self.save)
        self.runShortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.runShortcut.activated.connect(self.run)
        
        self.runButton.clicked.connect(self.run)
        
        self.setObjectName(text.replace(' ', '-'))

    def __initWidget(self):
        self.initLayout()
        self.addSubInterface(self.new_edit, 'New code', self.tr('new'), None)
        qrouter.setDefaultRouteKey(self.stackedWidget, self.new_edit.objectName())

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.tabBoxLayout.addWidget(self.tabBar)
        self.tabBoxLayout.addWidget(self.runButton)
        self.vBoxLayout.addLayout(self.tabBoxLayout)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(5, 5, 5, 5)

    def addSubInterface(self, widget: PlainTextEdit, objectName, text, icon):
        widget.setObjectName(objectName)
        widget.setFont(QFont("Consolas", 20))
        self.highlighter = KeywordHighlighter(widget.document())
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def save(self):
        QMessageBox.information(self, "Save", "You pressed Ctrl+S. Waiting for save to be implemented...")
    def run(self):
        compiler = Compiler()
        compiler.code = self.new_edit.toPlainText()

        try:
            compiler.compile()
            if compiler.error:
                raise Exception(compiler.error)
            token_show = []
            for i in range(len(compiler.tokens)):
                token_show.append((compiler.tokens[i][0], compiler.tokens[i][1], compiler.val_token(compiler.tokens[i])))
            self.controller.resetTokens(token_show)
            self.controller.resetQuad(compiler.quadruples)
            variables_show = []
            for var, value in compiler.variables.items():
                variables_show.append((var, value))
            self.controller.resetVariables(variables_show)
            QMessageBox.information(self, "Run", "Compilation Done.")

            if DEBUG_MODE:
                print(compiler.tokens)
                print(compiler.quadruples)
                print(compiler.variables)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Compilation failed:\n{str(e)}")
