import sys
import sqlite3
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                               QDialogButtonBox as QDialogueButtonBox)
from PySide6.QtCore import (Qt, QFile, Signal, Slot)
from ui_createBucket import Ui_MainWindow
from uiwidget_bucketTime import BucketTimeElement
from taskBucketObjects import Bucket


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__" or True:
    app = QApplication(sys.argv)
    window = MainWindow()
    addBucketsArea = window.ui.AddBucketsArea
    bucketTimes = []
    warningShown = False

    @Slot()
    def AddBucketTime():
        newBucketTime = BucketTimeElement()
        addBucketsArea.layout().addWidget(newBucketTime)
        bucketTimes.append(newBucketTime)

    @Slot()
    def RemoveBucketTime():
        if len(bucketTimes) == 0: return 0
        lastBucketTime = bucketTimes.pop(-1)
        addBucketsArea.layout().removeWidget(lastBucketTime)

    addNewBucketTimeElementButton  = window.ui.AddBucketTimeButton
    addNewBucketTimeElementButton.clicked.connect(AddBucketTime)

    removeLastBucketTimeButton = window.ui.RemoveBucketTimeButton
    removeLastBucketTimeButton.clicked.connect(RemoveBucketTime)
        
    def secondsSinceStartOfWeek(day, QTimeObject):
        match day:
            case "Monday": seconds = 0
            case "Tuesday": seconds = 86400
            case "Wednesday": seconds = 172800
            case "Thursday": seconds = 259200
            case "Friday": seconds = 345600
            case "Saturday": seconds = 432000
            case "Sunday": seconds = 518400

        seconds += QTimeObject.msecsSinceStartOfDay()

        return seconds

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
    def CreateBucket():
        inputsAreValid = True
        warning = ""
        bucketName = window.ui.bucketNameEdit.text()
        if bucketName == "": inputsAreValid = False; warning += "Bucket name needed\n"

        for BucketTimeUiElement in bucketTimes:
            startTime = secondsSinceStartOfWeek(BucketTimeUiElement.startDay.currentText(),
                                                BucketTimeUiElement.startTime.time())
            endTime = secondsSinceStartOfWeek(BucketTimeUiElement.finishDay.currentText(),
                                              BucketTimeUiElement.finishTime.time())

            # inputvalidation - ensuring this won't be inside another bucket
            connection = sqlite3.connect("TaskBucket_Data.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT startTime, finishTime
                FROM Buckets
                           """)
            otherBuckets = cursor.fetchall()

            for bucket in otherBuckets:
                if (
                        startTime >= bucket[0] and startTime <= bucket[1]
                        or
                        endTime >= bucket[0] and endTime <= bucket[1]
                    ):
                    inputsAreValid = False
                    warning += "Bucket could not be created because it would have been inside another bucket\n"
            # - ensuring this won't encase another bucket
            for bucket in otherBuckets:
                if (
                        bucket[0] >= startTime and bucket[0] <= endTime
                        or
                        bucket[1] >= startTime and bucket[1] <= endTime
                    ):
                    inputsAreValid = False
                    warning += "Bucket could not be created because it would have interfered with another bucket\n"

            # - ensuring bucket is over a minute
            if (endTime - startTime) <= 60:
                inputsAreValid = False
                warning += "The bucket cannot finish before it has started\n"

            #add buckets to database if all is well
            if inputsAreValid:
                bucketToAdd = Bucket(bucketName, startTime, endTime)
                bucketToAdd.AddBucketToDB()
                print("bucket added succesfully")
                window.close()
            else:
                print(warning)
                showWarning(warning)
                

    okButton = window.ui.buttonBox.button(QDialogueButtonBox.Ok)
    okButton.clicked.connect(CreateBucket)

    cancelButton = window.ui.buttonBox.button(QDialogueButtonBox.Cancel)
    cancelButton.clicked.connect(window.close)

    window.show()
    sys.exit(app.exec())
