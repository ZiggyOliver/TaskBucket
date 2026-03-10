import sys
import sqlite3
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                               QDialogButtonBox as QDialogueButtonBox,
                               QSpacerItem, QSizePolicy)
from PySide6.QtCore import (Qt, QFile, Signal, Slot, QSize, QTime)
from PySide6.QtGui import (QPalette, QColor as QColour)
from ui_createBucket import Ui_MainWindow
from uiwidget_bucketTime import BucketTimeElement
from taskBucketObjects import Bucket


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
app = QApplication(sys.argv)
window = MainWindow()
addBucketsArea = window.ui.AddBucketsArea
bucketTimes = []
warningShown = False

highlightWidgetsParents = {}
calendarSpacersParents = {}

@Slot()
def HighlightBucketOnCalendar(bucketElement):

    startTime = secondsSinceStartOfWeek(bucketElement.startDay.currentText(),
                                        bucketElement.startTime.time())
    endTime = secondsSinceStartOfWeek(bucketElement.finishDay.currentText(),
                                      bucketElement.finishTime.time())

    #find correct day UI element
    daySize = window.ui.days.frameSize().height()
    timeLenFactor = (daySize / 86400) / 2
    match startTime // 86400:
        case 0: dayContents = window.ui.Acontents
        case 1: dayContents = window.ui.Bcontents
        case 2: dayContents = window.ui.Ccontents
        case 3: dayContents = window.ui.Dcontents
        case 4: dayContents = window.ui.Econtents
        case 5: dayContents = winodw.ui.Fcontents
        case 6: dayContents = window.ui.Gcontents


    #remove this day's previous widgets
    widgetDeleteList = []
    for widget in highlightWidgetsParents.keys():
        if widget.parentWidget() == dayContents: widgetDeleteList.append(widget)
    for widget in widgetDeleteList:
        dayContents.layout().removeWidget(widget)
        widget.destroy()
        highlightWidgetsParents.pop(widget)
        del widget
    
    #do the same for spacers
    spacerDeleteList = []
    for spacer in calendarSpacersParents.keys():
        if calendarSpacersParents[spacer] == dayContents: spacerDeleteList.append(spacer)
    for spacer in spacerDeleteList:
        dayContents.layout().removeItem(spacer)
        calendarSpacersParents.pop(spacer)
        del spacer

    #create a new spacer with correct height
    spacerHeight = (startTime % 86400) * timeLenFactor
    newSpacer = QSpacerItem(0, spacerHeight, vData = QSizePolicy.Fixed)
    dayContents.layout().addItem(newSpacer)
    calendarSpacersParents[newSpacer] = dayContents
    #do the same for a new widget
    widgetHeight = (startTime - endTime) * timeLenFactor
    newWidget = QWidget()
    newWidget.setFixedHeight(widgetHeight)
    newWidget.setAutoFillBackground(True)
    highlightPalette = QPalette()
    highlightPalette.setColor(QPalette.ColorRole.Window, QColour(0,255,0))
    newWidget.setPalette(highlightPalette)
    dayContents.layout().addWidget(newWidget)
    highlightWidgetsParents[newWidget] = dayContents    
    

    print("=======================================")
    print(f"""StartTime:{startTime}, endTime:{endTime}\
          length:{widgetHeight}, spacerHeight:{spacerHeight},
          timeLenFactor: {timeLenFactor}
    """)



@Slot()
def AddBucketTime():
    newBucketTime = BucketTimeElement()
    addBucketsArea.layout().addWidget(newBucketTime)
    bucketTimes.append(newBucketTime)                                                  

    #print(startTime, endTime)
    newBucketTime.startTime.timeChanged.connect(lambda time, bucketElement=newBucketTime:
                                                HighlightBucketOnCalendar(newBucketTime))


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

    seconds += QTimeObject.msecsSinceStartOfDay() // 1000

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
                warning += \
                "Bucket could not be created because it would have been inside another bucket\n"
        # - ensuring this won't encase another bucket
        for bucket in otherBuckets:
            if (
                    bucket[0] >= startTime and bucket[0] <= endTime
                    or
                    bucket[1] >= startTime and bucket[1] <= endTime
                ):
                inputsAreValid = False
                warning += \
                "Bucket could not be created because it would have interfered with another bucket\n"

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

if __name__ == "__main__" or True:
    window.show()
    sys.exit(app.exec())
