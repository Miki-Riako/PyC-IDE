import os

from PySide6.QtCore import Qt, QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout

from qfluentwidgets import FluentWindow
from qfluentwidgets import NavigationItemPosition
from qfluentwidgets import setFont, SplashScreen, SubtitleLabel
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        ...
        # self.label = SubtitleLabel(text, self)
        # self.hBoxLayout = QHBoxLayout(self)
        # setFont(self.label, 24)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        ...
        self.setObjectName(text.replace(' ', '-'))

class IDE(FluentWindow):
    """Main Window"""
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(210, 210))
        self.show()
        self.createSubInterface()
        
        self.homeInterface       = Widget('Home Interface', self)
        self.workspaceInterface  = Widget('Workspace Interface', self)
        self.controllerInterface = Widget('Controller Interface', self)
        self.helperInterface     = Widget('Helper Interface', self)
        self.aboutInterface       = Widget('About Interface', self)
        self.settingInterface    = Widget('Setting Interface', self)

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
        self.resize(900, 700)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images', 'SOSlogo.png')))
        self.setWindowTitle('欢迎！Welcome to PyC-IDE')

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(618, loop.quit)
        loop.exec()

    def setupUI(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
