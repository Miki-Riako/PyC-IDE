from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QFrame, QWidget, QSpacerItem, QSizePolicy)

class About(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)  # Set initial window size
        Form.setMaximumSize(600, 400)  # Set maximum window size
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")

        spacerItemTop = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItemTop)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)  # Enable word wrap
        self.label.setFont(QFont("Arial", 12))  # Set font size
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)  # Enable word wrap
        self.label_2.setFont(QFont("Arial", 10))  # Set font size
        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)  # Enable word wrap
        self.label_3.setFont(QFont("Arial", 12))  # Set font size
        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)  # Enable word wrap
        self.label_4.setFont(QFont("Arial", 10))  # Set font size
        self.verticalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setWordWrap(True)  # Enable word wrap
        self.label_5.setFont(QFont("Arial", 12))  # Set font size
        self.verticalLayout.addWidget(self.label_5)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)  # Enable word wrap
        self.label_6.setFont(QFont("Arial", 10))  # Set font size
        self.verticalLayout.addWidget(self.label_6)

        spacerItemBottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItemBottom)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u516c\u544a</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u8054\u7cfb\u4f5c\u8005\uff1a20225443@stu.neu.edu.cn\n"
"\u5df2\u77e5\u7684\u5c0fBug\uff1a\u6682\u65e0\uff0c\u5982\u679c\u53d1\u73b0\u8bf7\u52a1\u5fc5\u8054\u7cfb\u4f5c\u8005\uff0c\u5341\u5206\u611f\u8c22\u3002", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u4f7f\u7528\u8bf4\u660e</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u7f16\u8bd1\u89c4\u5219\u662f\u4e25\u683c\u89c4\u5219\u3002</p><p>\u73b0\u5728\u4ecd\u6709\u8bb8\u591a\u529f\u80fd\u672a\u5b8c\u5584\u3002</p><p>\u7f16\u8bd1\u8fc7\u7a0b\u4ee5\u4f9b\u5b66\u4e60\u3002</p><p>Enjoy!</p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u5173\u4e8ePyC-IDE</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Design by <a href=\"https://github.com/Miki-Riako\"><span style=\" text-decoration: underline; color:#007af4;\">Miki_Riako</span></a></p><p>\u672c\u9879\u76ee\u7528\u5230\u7684\u5f00\u6e90\u6846\u67b6\uff1aPySide6\u53ef\u89c6\u5316\u6846\u67b6\u3001PyQt-Fluent-Widgets\u63a7\u4ef6</p></body></html>", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = QWidget()
    ui = About("About", window)
    window.show()
    sys.exit(app.exec())
