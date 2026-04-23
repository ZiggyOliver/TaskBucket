from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (QMainWindow, QApplication, QPushButton)
from PySide6.QtCore import Signal, Slot
import sys
import createBucket
from createBucket import CreateBucketWindow
from createTask import CreateTaskWindow
from Calendar import CalendarWindow
from GenerateDatabase import GenerateDatabase
import os

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
    #create the database file if it doesn't exist already
    if os.path.exists("TaskBucket_Data.db"):
        print("YouAlreadyHaveADBFile")
    else:
        print("No DB file detected, generating one")
        GenerateDatabase()
    
    app = QApplication.instance()
    if app == None: app = QApplication(sys.argv)
    window = MainWindow()

    #connections
    window.ui.addBucketsButton.clicked.connect(window.LoadAddBuckets)
    window.ui.viewCalendarButton.clicked.connect(window.LoadSchedule)
    window.ui.addTasksButton.clicked.connect(window.LoadAddTasks)

    window.show()
    sys.exit(app.exec())


