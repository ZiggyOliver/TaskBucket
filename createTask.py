import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QFormLayout,
                               QDialogButtonBox as QDialogueButtonBox)
from PySide6.QtCore import Qt, QFile, Signal, Slot
from ui_createTask import Ui_Form
from taskBucketObjects import Task
import epoch
import sqlite3


class CreateTaskWindow(QMainWindow):
    def __init__(self):
        super(CreateTaskWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.warningShown = False

        #setup TaskBucketTypeSelector to display bucket types
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT bucketType
            FROM Buckets
            ORDER BY bucketType
        """)
        self.bucketTypes = []
        for bucketType in cursor.fetchall():
            if bucketType[0] in self.bucketTypes: continue
            self.bucketTypes.append(bucketType[0])
        
        self.ui.taskBucketTypeSelector.addItems(self.bucketTypes)


    def showWarning(self, warningText):
        if not self.warningShown:
            global warningLabel
            warningLabel = QLabel()
            self.ui.formLayout.addWidget(warningLabel)
            warningLabel.setText(warningText)
            self.warningShown = True
        else:
            warningLabel.setText(warningText)
        

    @Slot()
    def CreateTask(self):
        taskName = self.ui.taskNameEdit.toPlainText()
        compatibleBucketType = self.ui.taskBucketTypeSelector.currentText()
        taskDeadline = self.ui.taskDeadlineEdit.dateTime().toSecsSinceEpoch()
        estimatedTime = self.ui.estTaskTime.time().msecsSinceStartOfDay() // 1000
        description = self.ui.taskDescriptionEdit.toPlainText()
        maxSessionTime = self.ui.maxSessionTimeEdit.time().msecsSinceStartOfDay() // 1000
        if maxSessionTime == 0: maxSessionTime = estimatedTime
        status = self.ui.taskStatusEdit.toPlainText()
        recursion = ""
        if self.ui.dailyRecRadio.isChecked(): recursion = "daily"
        elif self.ui.weeklyRecRadio.isChecked(): recursion = "weekly"
        elif self.ui.monthlyRecRadio.isChecked(): recursion = "monthly"
        elif self.ui.yearlyRecRadio.isChecked(): recursion = "yearly"

        #input validation
        inputsAreValid = True
        warning = ""

        if taskName == "": inputsAreValid = False ; warning += "task name needed "
        if compatibleBucketType == "": inputsAreValid = False ; warning += "Bucket type needed "
        if taskDeadline <= epoch.now():
            inputsAreValid = False
            warning += "Deadline must be in future "
        if estimatedTime < 1: inputsAreValid = False ; warning += "Time estimate must be above zero "

        if inputsAreValid:
            taskToCreate = Task(taskName, compatibleBucketType, taskDeadline, estimatedTime,
                                description, maxSessionTime, status, recursion)
            taskToCreate.AddTaskToDB()
            self.close()
        else:
            print(warning)
            self.showWarning(warning)



    def setupConnections(self):       
        okButton = self.ui.buttonBox.button(QDialogueButtonBox.Ok)
        okButton.clicked.connect(self.CreateTask)

        cancelButton = self.ui.buttonBox.button(QDialogueButtonBox.Cancel)
        cancelButton.clicked.connect(self.close)
    

if __name__ == "__main__":
    app = QApplication.instance()
    if app == None: app = QApplication()
    
    window = CreateTaskWindow()
    window.show()
    window.setupConnections()
    
    try: sys.exit(app.exec())
    except: app.beep()
