import sqlite3
import sys
from taskBucketObjects import Task, Bucket, TaskBucket
from PySide6.QtWidgets import (QApplication, QMainWindow, QSpacerItem, QWidget, QSizePolicy)
from PySide6.QtGui import QPalette, QColor as QColour
from PySide6.QtCore import QFile, Signal, Slot
from ui_calendar import Ui_MainWindow
from CalendarBucketElement import CalendarBucketElement

class MainWindow(QMainWindow):
    resized = Signal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resized.emit()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)
    

app = QApplication(sys.argv)
window = MainWindow()

#resize days
@Slot()
def resizeDays():
    totalSize = window.ui.scrollArea.size().width() - 10
    if totalSize < 500: totalSize = 500
    daysDisplayed = [
        window.ui.Aday_2,
        window.ui.Bday_2,
        window.ui.Cday_2,
        window.ui.Dday_2,
        window.ui.Eday_2,
        window.ui.Fday_2,
        window.ui.Gday_2
    ]
    for dayDisplayed in daysDisplayed:
        dayDisplayed.setFixedWidth(totalSize / 7)

window.resized.connect(resizeDays)

#fetch from database
connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()
cursor.execute("""
    SELECT bucketID, bucketType, startTime, finishTime, bucketColour
    FROM Buckets
""")
buckets = []
for row in cursor.fetchall():
    newBucketObject = Bucket(row[1], row[2], row[3])
    newBucketObject.setID(row[0])
    newBucketObject.setColour(row[4])
    buckets.append(newBucketObject)

highlightWidgetsParents = {}
calendarSpacersParents = {}

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

    #sort bucketTimes by startTime to prevent strangeness
    """
    bucketTimes.sort(key = lambda bucketUiElement:
                     secondsSinceStartOfWeek(bucketUiElement.startDay.currentText(),
                                             bucketUiElement.startTime.time())
    """ #no longer needed as Buckets will all be sorted when fetched

    #Add new spacers & widgets for each BucketTimeElement
    for bucket in buckets:      
        startTime = bucket.startTime
        endTime = bucket.finishTime

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

        #create a QSpacerItem to space-out buckets
        spacerHeight = ((startTime % 86400) - lastEndTime[dayContents] - 20) * timeLenFactor
                                                                            #-20 is for name and time
        newSpacer = QSpacerItem(2,spacerHeight, vData=QSizePolicy.Policy.Fixed)
        dayContents.layout().addSpacerItem(newSpacer)
        calendarSpacersParents[newSpacer] = dayContents

        #create the bucket itself
        widgetHeight = (endTime - startTime) * timeLenFactor
        newWidget = CalendarBucketElement(bucket.colour)
        print(bucket.bucketType, bucket.colour)
        newWidget.populateWithTasks(bucket.bucketID, startTime, endTime, widgetHeight + 20)#CBE
        newWidget.setNameAndTime(bucket)
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
    resizeDays()
        
if __name__ == "__main__":
    window.ui.pushButton.clicked.connect(HighlightBucketsOnCalendar)
    window.show()
    HighlightBucketsOnCalendar()
    sys.exit(app.exec())
