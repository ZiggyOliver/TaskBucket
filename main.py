#from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (QApplication, QMainWindow)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication.instance()
if app == None: app = QAppliaction(sys.argv)

window = MainWindow()

if __name__ == "__main__":
    window.show()
    sys.exit(app.exec())
