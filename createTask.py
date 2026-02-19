import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QFormLayout,
                               QDialogButtonBox as QDialogueButtonBox)
from PySide6.QtCore import Qt, QFile, Signal, Slot
from ui_createTask import Ui_Form
from taskBucketObjects import Task
import epoch
import createTask


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__" or True:
    app = QApplication(sys.argv)
    window = MainWindow()
    warningShown = False

    def showWarning(warningText):
        global warningShown
        if not warningShown:
            global warningLabel
            warningLabel = QLabel()
            window.ui.formLayout.addWidget(warningLabel)
            warningLabel.setText(warningText)
            warningShown = True
        else:
            warningLabel.setText(warningText)
        

    @Slot()
    def CreateTask():
        taskName = window.ui.taskNameEdit.toPlainText()
        compatibleBucketType = window.ui.taskBucketTypeEdit.toPlainText()
        taskDeadline = window.ui.taskDeadlineEdit.dateTime().toSecsSinceEpoch()
        estimatedTime = window.ui.estTaskTime.time().msecsSinceStartOfDay() // 1000
        description = window.ui.taskDescriptionEdit.toPlainText()
        maxSessionTime = window.ui.maxSessionTimeEdit.time().msecsSinceStartOfDay() // 1000
        status = window.ui.taskStatusEdit.toPlainText()
        recursion = ""
        if window.ui.dailyRecRadio.isChecked(): recursion = "daily"
        elif window.ui.weeklyRecRadio.isChecked(): recursion = "weekly"
        elif window.ui.monthlyRecRadio.isChecked(): recursion = "monthly"
        elif window.ui.yearlyRecRadio.isChecked(): recursion = "yearly"

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
            window.close()
        else:
            print(warning)
            showWarning(warning)
            

    okButton = window.ui.buttonBox.button(QDialogueButtonBox.Ok)
    okButton.clicked.connect(CreateTask)

    cancelButton = window.ui.buttonBox.button(QDialogueButtonBox.Cancel)
    cancelButton.clicked.connect(window.close)
    
    window.show()
    sys.exit(app.exec())
