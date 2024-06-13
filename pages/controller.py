from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme,
    NavigationAvatarWidget,  SplitFluentWindow, FluentTranslator, TableWidget)
from qfluentwidgets import FluentIcon as FIF

class Controller(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi()
        self.addTables()
        self.setObjectName(text.replace(' ', '-'))

    def setupUi(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
    
    def addTables(self):
        self.tokens_table = TableWidget(self)
        self.quad_table = TableWidget(self)
        self.variables_table = TableWidget(self)
        self.tokens_table.setBorderVisible(True)
        self.tokens_table.setBorderRadius(8)
        self.tokens_table.setWordWrap(False)
        self.tokens_table.setColumnCount(3)
        self.quad_table.setBorderVisible(True)
        self.quad_table.setBorderRadius(8)
        self.quad_table.setWordWrap(False)
        self.quad_table.setColumnCount(5)
        self.variables_table.setBorderVisible(True)
        self.variables_table.setBorderRadius(8)
        self.variables_table.setWordWrap(False)
        self.variables_table.setColumnCount(2)
        self.layout.addWidget(self.tokens_table)
        self.layout.addWidget(self.quad_table)
        self.layout.addWidget(self.variables_table)

        self.resetTokens([])
        self.resetQuad([])
        self.resetVariables([])

    def resetTokens(self, tokens):
        self.infos = tokens
        self.tokens_table.setRowCount(len(self.infos))
        for i in range(len(self.infos)):
            self.tokens_table.setItem(i, 0, QTableWidgetItem(self.infos[i][0]))
            self.tokens_table.setItem(i, 1, QTableWidgetItem(str(self.infos[i][1])))
            self.tokens_table.setItem(i, 2, QTableWidgetItem(self.infos[i][2]))
        
        self.tokens_table.setHorizontalHeaderLabels(['标识符 Identifier', '索引 Index', '值 Value'])
        self.tokens_table.verticalHeader().hide()
        self.tokens_table.resizeColumnsToContents()
        self.tokens_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def resetQuad(self, quad):
        self.infos = quad
        self.quad_table.setRowCount(len(self.infos))
        for i in range(len(self.infos)):
            self.quad_table.setItem(i, 0, QTableWidgetItem(self.infos[i][0]))
            self.quad_table.setItem(i, 1, QTableWidgetItem(str(self.infos[i][1])))
            self.quad_table.setItem(i, 2, QTableWidgetItem(str(self.infos[i][2])))
            self.quad_table.setItem(i, 3, QTableWidgetItem(str(self.infos[i][3])))
            self.quad_table.setItem(i, 4, QTableWidgetItem(str(self.infos[i][4])))
        
        self.quad_table.setHorizontalHeaderLabels(['索引 Index', '算符 Operation', '对象1 Operand 1', '对象2 Operand 2', '结果 Result'])
        self.quad_table.verticalHeader().hide()
        self.quad_table.resizeColumnsToContents()
        self.quad_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def resetVariables(self, variables):
        self.infos = variables
        self.variables_table.setRowCount(len(self.infos))
        for i in range(len(self.infos)):
            self.variables_table.setItem(i, 0, QTableWidgetItem(self.infos[i][0]))
            self.variables_table.setItem(i, 1, QTableWidgetItem(str(self.infos[i][1])))
        
        self.variables_table.setHorizontalHeaderLabels(['对象 Operand', '值 Value'])
        self.variables_table.verticalHeader().hide()
        self.variables_table.resizeColumnsToContents()
        self.variables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)