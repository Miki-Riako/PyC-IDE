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
    TransparentDropDownToolButton, TransparentToolButton, setTheme, Theme, isDarkTheme,
    InfoBar, InfoBarPosition, InfoBarManager
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



class Helper(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.tabBoxLayout = QHBoxLayout(self)
        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)

        self.new_edit = PlainTextEdit(self)
        self.new_edit.setPlaceholderText("New code...")

        code = ''
        self.new_edit.setPlainText(code)
        
        self.__initWidget()
        
        self.setObjectName(text.replace(' ', '-'))

    def set_code(self, code):
        self.new_edit.setPlainText(code)

    def __initWidget(self):
        self.initLayout()
        self.addSubInterface(self.new_edit, 'New code', self.tr('new'), None)
        qrouter.setDefaultRouteKey(self.stackedWidget, self.new_edit.objectName())

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.tabBoxLayout.addWidget(self.tabBar)
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
