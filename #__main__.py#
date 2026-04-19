from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton)
from PySide6.QtCore import Signal, Slot
import sys
import createBucket
from createBucket import CreateBucketWindow
from createTask import CreateTaskWindow
from Calendar import CalendarWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @Slot()
    def LoadAddBuckets(self):
        self.window = CreateBucketWindow()
        self.window.show()
        self.window.setupConnections()

    @Slot()
    def LoadAddTasks(self):
        self.window = CreateTaskWindow()
        self.window.show()
        self.window.setupConnections()


    @Slot()
    def LoadSchedule(self):
        self.window = CalendarWindow()
        self.window.show()
        self.window.setupConnections()

if __name__ == "__main__":
    app = QApplication.instance()
    if app == None: app = QApplication(sys.argv)
    window = MainWindow()

    #connections
    window.ui.addBucketsButton.clicked.connect(window.LoadAddBuckets)
    window.ui.viewCalendarButton.clicked.connect(window.LoadSchedule)
    window.ui.addTasksButton.clicked.connect(window.LoadAddTasks)

    window.show()
    sys.exit(app.exec())


