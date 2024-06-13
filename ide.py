import os
from _compiler import Compiler

from PySide6.QtCore import QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from qfluentwidgets import FluentWindow
from qfluentwidgets import NavigationItemPosition
from qfluentwidgets import setTheme, SplashScreen
from qfluentwidgets import Theme
from qfluentwidgets import FluentIcon as FIF

from pages import Home, Workspace, Controller, Helper, About, Setting

class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        ...
        self.setObjectName(text.replace(' ', '-'))

class IDE(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(210, 210))
        self.show()
        self.createSubInterface()

        self.compiler = Compiler()

        self.homeInterface       = Home("Home Interface", self)
        self.controllerInterface = Controller('Controller Interface', self)
        self.workspaceInterface  = Workspace('Workspace Interface', self.compiler, self.controllerInterface, self)
        self.helperInterface     = Helper('Helper Interface', self)
        self.aboutInterface      = About('About Interface', self)
        self.settingInterface    = Setting('Setting Interface', self)

        self.initNavigation()
        self.splashScreen.finish()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页 Home')
        self.addSubInterface(self.workspaceInterface, FIF.DEVELOPER_TOOLS, '工作区 Work Space')
        self.addSubInterface(self.controllerInterface, FIF.APPLICATION, '控制台 Control Menu')
        self.addSubInterface(self.helperInterface, FIF.BOOK_SHELF, '帮助文档 Helper Document')

        self.addSubInterface(self.aboutInterface, FIF.PEOPLE, '关于 About', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置 Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        setTheme(Theme.DARK)
        self.resize(900, 700)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images', 'SOSlogo.png')))
        self.setWindowTitle('欢迎！Welcome to PyC-IDE')
        self.showMaximized()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(618, loop.quit)
        loop.exec()

    def setupUI(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
