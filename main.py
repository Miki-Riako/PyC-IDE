from PySide6.QtWidgets import QApplication, QMainWindow

class MyWidow(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWidow()
    window.show()
    app.exec()
