from PySide6.QtWidgets import QApplication
from ide import IDE

class MainWindow(IDE):
    def __init__(self):
        super().__init__()
        self.setupUI()

if __name__ == '__main__':
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
