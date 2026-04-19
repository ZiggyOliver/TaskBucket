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


class CreateBucketWindow(QMainWindow):
    def __init__(self):
        print("create Bucket Main Window __init__ ran")
        super(CreateBucketWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print(self.ui)

        #other stuff
        self.addBucketsArea = self.ui.AddBucketsArea
        self.bucketTimes = []
        self.warningShown = False

        self.connection = sqlite3.connect("TaskBucket_Data.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            SELECT startTime, finishTime
            FROM Buckets
                       """)
        self.bucketsInDB = self.cursor.fetchall()
        self.highlightWidgetsParents = {}
        self.calendarSpacersParents = {}

    @Slot()
    def HighlightBucketsOnCalendar(self):
        #print("HighlightBucketsOnCalendarCalled")

        #Remove All Previous Highlights

            #For Widgets
        widgetDeleteList = []
        for widget in self.highlightWidgetsParents.keys(): widgetDeleteList.append(widget)
        for widget in widgetDeleteList:
            #print("delete widget called")
            widget.hide()
            #dayContents.layout().removeWidget(widget)
            widget.destroy()
            self.highlightWidgetsParents.pop(widget)
            del widget

            #For Spacers
        spacerDeleteList = []
        for spacer in self.calendarSpacersParents.keys():
            spacerDeleteList.append(spacer)
            self.calendarSpacersParents[spacer].layout().removeItem(spacer)
        for spacer in spacerDeleteList:
            #print("delete spacer called")
            #dayContents.layout().removeItem(spacer)
            self.calendarSpacersParents.pop(spacer)
            del spacer

        #keep track of when the last item in each day ends
        lastEndTime = {
            self.ui.Acontents: 0,
            self.ui.Bcontents: 0,
            self.ui.Ccontents: 0,
            self.ui.Dcontents: 0,
            self.ui.Econtents: 0,
            self.ui.Fcontents: 0,
            self.ui.Gcontents: 0
        }

        #sort bucketTimes by startTimeto prevent strangeness
        self.bucketTimes.sort(key = lambda bucketUiElement:
                         self.secondsSinceStartOfWeek(bucketUiElement.startDay.currentText(),
                                                 bucketUiElement.startTime.time()))

        #Add new spacers & widgets for each BucketTimeElement
        for bucketElement in self.bucketTimes:      
            startTime = self.secondsSinceStartOfWeek(bucketElement.startDay.currentText(),
                                            bucketElement.startTime.time())
            endTime = self.secondsSinceStartOfWeek(bucketElement.finishDay.currentText(),
                                          bucketElement.finishTime.time())

            if (endTime - startTime) <= 0: continue

            #find correct day UI element
            daySize = self.ui.days.frameSize().height()
            timeLenFactor = (daySize / 86400)
            match startTime // 86400:
                case 0: dayContents = self.ui.Acontents
                case 1: dayContents = self.ui.Bcontents
                case 2: dayContents = self.ui.Ccontents
                case 3: dayContents = self.ui.Dcontents
                case 4: dayContents = self.ui.Econtents
                case 5: dayContents = self.ui.Fcontents
                case 6: dayContents = self.ui.Gcontents

            #create a QSpacerItem to space-out highlight areas
            spacerHeight = ((startTime % 86400) - lastEndTime[dayContents]) * timeLenFactor
            newSpacer = QSpacerItem(2,spacerHeight, vData=QSizePolicy.Policy.Fixed)
            dayContents.layout().addSpacerItem(newSpacer)
            self.calendarSpacersParents[newSpacer] = dayContents

            #create the highlight Widget itself
            widgetHeight = (endTime - startTime) * timeLenFactor
            newWidget = QWidget()
            newWidget.setFixedHeight(widgetHeight)
            newWidget.setAutoFillBackground(True)
            highlightPalette = QPalette()
            highlightPalette.setColor(QPalette.ColorRole.Window, QColour(255,0,0, a=150))
            newWidget.setPalette(highlightPalette)
            dayContents.layout().addWidget(newWidget)
            self.highlightWidgetsParents[newWidget] = dayContents

            #update LastEndTime
            lastEndTime[dayContents] = endTime % 86400

            #some helpful debug info
            '''
            print("=======================================")
            print(f"""StartTime:{startTime}, endTime:{endTime}\
                  length:{widgetHeight}, spacerHeight:{spacerHeight},
                  timeLenFactor: {timeLenFactor}
            """)

            print(self.highlightWidgetsParents, "\n =======\n", self.calendarSpacersParents)
            '''

    @Slot()
    def AddBucketTime(self):
        newBucketTime = BucketTimeElement()
        self.addBucketsArea.layout().addWidget(newBucketTime)
        self.bucketTimes.append(newBucketTime)

        newBucketTime.startTime.timeChanged.connect(self.HighlightBucketsOnCalendar)
        newBucketTime.finishTime.timeChanged.connect(self.HighlightBucketsOnCalendar)
        newBucketTime.startDay.currentTextChanged.connect(self.HighlightBucketsOnCalendar)
        newBucketTime.finishDay.currentTextChanged.connect(self.HighlightBucketsOnCalendar)

    @Slot()
    def RemoveBucketTime(self):
        if len(self.bucketTimes) == 0: return 0
        lastBucketTime = self.bucketTimes.pop(-1)
        self.addBucketsArea.layout().removeWidget(lastBucketTime)


    @Slot()
    def UpdateSampleColour(self):
        colour = QColour(
            self.ui.redSpinBox.value(),
            self.ui.greenSpinBox.value(),
            self.ui.blueSpinBox.value()
        )
        palette = QPalette(colour, colour) # This is and ought to be.
        self.ui.sampleColour.setPalette(palette)


    def secondsSinceStartOfWeek(self, day, QTimeObject):
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
    def CreateBucket(self):
        print("bucketsInDB:", self.bucketsInDB)
        otherBuckets = self.bucketsInDB.copy()
        print(otherBuckets)
        inputsAreValid = True
        warning = ""
        bucketName = self.ui.bucketNameEdit.text()
        if bucketName == "": inputsAreValid = False; warning += "Bucket name needed\n"

        for BucketTimeUiElement in self.bucketTimes:
            startTime = self.secondsSinceStartOfWeek(BucketTimeUiElement.startDay.currentText(),
                                                BucketTimeUiElement.startTime.time())
            endTime = self.secondsSinceStartOfWeek(BucketTimeUiElement.finishDay.currentText(),
                                              BucketTimeUiElement.finishTime.time())
            bucketColour = str(self.ui.redSpinBox.value()).zfill(3) + \
                           str(self.ui.greenSpinBox.value()).zfill(3) + \
                           str(self.ui.blueSpinBox.value()).zfill(3)

            # inputvalidation
            for bucket in otherBuckets:
                # - ensuring this won't be inside another bucket
                if (
                        startTime >= bucket[0] and startTime <= bucket[1]
                        or
                        endTime >= bucket[0] and endTime <= bucket[1]
                    ):
                    inputsAreValid = False
                    warning += \
                    "Bucket could not be created because it would have been inside another bucket\n"

                # - ensuring this won't encase another bucket
                if (
                        bucket[0] >= startTime and bucket[0] <= endTime
                        or
                        bucket[1] >= startTime and bucket[1] <= endTime
                    ):
                    inputsAreValid = False
                    warning += \
                    "Bucket could not be created because it would've interfered with another bucket\n"

            # - ensuring bucket is over a minute
            if (endTime - startTime) <= 60:
                inputsAreValid = False
                warning += "The bucket cannot finish before it has started\n"

            #add bucket to database if all is well
            if inputsAreValid:
                bucketToAdd = Bucket(bucketName, startTime, endTime)
                bucketToAdd.setColour(bucketColour)
                bucketToAdd.AddBucketToDB(connection = self.connection)
                print("bucket ready to be added")
                otherBuckets.append((startTime, endTime))
            else:
                print(warning)
                self.showWarning(warning)
                self.connection.rollback()
                break

        if inputsAreValid:
            self.connection.commit()
            print("all ready buckets added")
            self.close()
            return 1
        return 0;

    def setupConnections(self):
        #connections for Add and Remove Bucket Time Buttons
        addNewBucketTimeElementButton  = self.ui.AddBucketTimeButton
        addNewBucketTimeElementButton.clicked.connect(self.AddBucketTime)
        addNewBucketTimeElementButton.clicked.connect(self.HighlightBucketsOnCalendar)

        removeLastBucketTimeButton = self.ui.RemoveBucketTimeButton
        removeLastBucketTimeButton.clicked.connect(self.RemoveBucketTime)
        removeLastBucketTimeButton.clicked.connect(self.HighlightBucketsOnCalendar)

        #connections for Update Sample Colour to RGB spin boxes
        self.ui.redSpinBox.valueChanged.connect(self.UpdateSampleColour)
        self.ui.greenSpinBox.valueChanged.connect(self.UpdateSampleColour)
        self.ui.blueSpinBox.valueChanged.connect(self.UpdateSampleColour)

        #connections for cancel and submit buttons
        okButton = self.ui.buttonBox.button(QDialogueButtonBox.Ok)
        okButton.clicked.connect(self.CreateBucket)

        cancelButton = self.ui.buttonBox.button(QDialogueButtonBox.Cancel)
        cancelButton.clicked.connect(self.close)



if __name__ == "__main__":
    app = QApplication.instance()
    if app == None: app = QApplication(sys.argv)
    window = CreateBucketWindow()
    window.show()
    window.setupConnections()
    try: sys.exit(app.exec())
    except: app.beep()
else: print("not __main__")
