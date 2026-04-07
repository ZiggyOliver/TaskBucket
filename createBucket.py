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

connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT startTime, finishTime
    FROM Buckets
               """)
bucketsInDB = cursor.fetchall()

highlightWidgetsParents = {}
calendarSpacersParents = {}

@Slot()
def HighlightBucketsOnCalendar():
    #print("HighlightBucketsOnCalendarCalled")

    #Remove All Previous Highlights
    
        #For Widgets
    widgetDeleteList = []
    for widget in highlightWidgetsParents.keys(): widgetDeleteList.append(widget)
    for widget in widgetDeleteList:
        #print("delete widget called")
        widget.hide()
        #dayContents.layout().removeWidget(widget)
        widget.destroy()
        highlightWidgetsParents.pop(widget)
        del widget

        #For Spacers
    spacerDeleteList = []
    for spacer in calendarSpacersParents.keys():
        spacerDeleteList.append(spacer)
        calendarSpacersParents[spacer].layout().removeItem(spacer)
    for spacer in spacerDeleteList:
        #print("delete spacer called")
        #dayContents.layout().removeItem(spacer)
        calendarSpacersParents.pop(spacer)
        del spacer

    #keep track of when the last item in each day ends
    lastEndTime = {
        window.ui.Acontents: 0,
        window.ui.Bcontents: 0,
        window.ui.Ccontents: 0,
        window.ui.Dcontents: 0,
        window.ui.Econtents: 0,
        window.ui.Fcontents: 0,
        window.ui.Gcontents: 0
    }

    #sort bucketTimes by startTimeto prevent strangeness
    bucketTimes.sort(key = lambda bucketUiElement:
                     secondsSinceStartOfWeek(bucketUiElement.startDay.currentText(),
                                             bucketUiElement.startTime.time()))

    #Add new spacers & widgets for each BucketTimeElement
    for bucketElement in bucketTimes:      
        startTime = secondsSinceStartOfWeek(bucketElement.startDay.currentText(),
                                        bucketElement.startTime.time())
        endTime = secondsSinceStartOfWeek(bucketElement.finishDay.currentText(),
                                      bucketElement.finishTime.time())

        if (endTime - startTime) <= 0: continue

        #find correct day UI element
        daySize = window.ui.days.frameSize().height()
        timeLenFactor = (daySize / 86400)
        match startTime // 86400:
            case 0: dayContents = window.ui.Acontents
            case 1: dayContents = window.ui.Bcontents
            case 2: dayContents = window.ui.Ccontents
            case 3: dayContents = window.ui.Dcontents
            case 4: dayContents = window.ui.Econtents
            case 5: dayContents = window.ui.Fcontents
            case 6: dayContents = window.ui.Gcontents

        #create a QSpacerItem to space-out highlight areas
        spacerHeight = ((startTime % 86400) - lastEndTime[dayContents]) * timeLenFactor
        newSpacer = QSpacerItem(2,spacerHeight, vData=QSizePolicy.Policy.Fixed)
        dayContents.layout().addSpacerItem(newSpacer)
        calendarSpacersParents[newSpacer] = dayContents

        #create the highlight Widget itself
        widgetHeight = (endTime - startTime) * timeLenFactor
        newWidget = QWidget()
        newWidget.setFixedHeight(widgetHeight)
        newWidget.setAutoFillBackground(True)
        highlightPalette = QPalette()
        highlightPalette.setColor(QPalette.ColorRole.Window, QColour(255,0,0, a=150))
        newWidget.setPalette(highlightPalette)
        dayContents.layout().addWidget(newWidget)
        highlightWidgetsParents[newWidget] = dayContents

        #update LastEndTime
        lastEndTime[dayContents] = endTime % 86400

        #some helpful debug info
        '''
        print("=======================================")
        print(f"""StartTime:{startTime}, endTime:{endTime}\
              length:{widgetHeight}, spacerHeight:{spacerHeight},
              timeLenFactor: {timeLenFactor}
        """)

        print(highlightWidgetsParents, "\n =======\n", calendarSpacersParents)
        '''

@Slot()
def AddBucketTime():
    newBucketTime = BucketTimeElement()
    addBucketsArea.layout().addWidget(newBucketTime)
    bucketTimes.append(newBucketTime)
    
    newBucketTime.startTime.timeChanged.connect(HighlightBucketsOnCalendar)
    newBucketTime.finishTime.timeChanged.connect(HighlightBucketsOnCalendar)
    newBucketTime.startDay.currentTextChanged.connect(HighlightBucketsOnCalendar)
    newBucketTime.finishDay.currentTextChanged.connect(HighlightBucketsOnCalendar)

@Slot()
def RemoveBucketTime():
    if len(bucketTimes) == 0: return 0
    lastBucketTime = bucketTimes.pop(-1)
    addBucketsArea.layout().removeWidget(lastBucketTime)

#connections for Add and Remove Bucket Time Buttons
addNewBucketTimeElementButton  = window.ui.AddBucketTimeButton
addNewBucketTimeElementButton.clicked.connect(AddBucketTime)
addNewBucketTimeElementButton.clicked.connect(HighlightBucketsOnCalendar)

removeLastBucketTimeButton = window.ui.RemoveBucketTimeButton
removeLastBucketTimeButton.clicked.connect(RemoveBucketTime)
removeLastBucketTimeButton.clicked.connect(HighlightBucketsOnCalendar)

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
    print("bucketsInDB:", bucketsInDB)
    otherBuckets = bucketsInDB.copy()
    print(otherBuckets)
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

        #add bucket to database if all is well
        if inputsAreValid:
            bucketToAdd = Bucket(bucketName, startTime, endTime)
            bucketToAdd.AddBucketToDB(connection = connection)
            print("bucket ready to be added")
            otherBuckets.append((startTime, endTime))
        else:
            print(warning)
            showWarning(warning)
            connection.rollback()
            break
        
    if inputsAreValid:
        connection.commit()
        print("all ready buckets added")
        window.close()
        return 1
    return 0;
        

#connections for cancel and submit buttons
okButton = window.ui.buttonBox.button(QDialogueButtonBox.Ok)
okButton.clicked.connect(CreateBucket)

cancelButton = window.ui.buttonBox.button(QDialogueButtonBox.Cancel)
cancelButton.clicked.connect(window.close)

if __name__ == "__main__" or True:
    window.show()
    sys.exit(app.exec())
