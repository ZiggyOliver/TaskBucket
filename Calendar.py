import sqlite3
import sys
from taskBucketObjects import Task, Bucket, TaskBucket
from PySide6.QtWidgets import (QApplication, QMainWindow, QSpacerItem, QWidget, QSizePolicy,
                               QDialog as QDialogue)
from PySide6.QtGui import QPalette, QColor as QColour
from PySide6.QtCore import QFile, Signal, Slot
from ui_calendar import Ui_MainWindow
from CalendarBucketElement import CalendarBucketElement
import TaskArrangementAlgorithm
from taskItem import TaskItem

class CalendarWindow(QMainWindow):
    resized = Signal()
    def __init__(self):
        super(CalendarWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resized.emit()

        TaskArrangementAlgorithm.ArrangeUnarrangedTasks()

        #fetch from database
        self.connection = sqlite3.connect("TaskBucket_Data.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            SELECT bucketID, bucketType, startTime, finishTime, bucketColour
            FROM Buckets
            ORDER BY startTime ASC
        """)
        self.buckets = []
        for row in self.cursor.fetchall():
            newBucketObject = Bucket(row[1], row[2], row[3])
            newBucketObject.setID(row[0])
            newBucketObject.setColour(row[4])
            self.buckets.append(newBucketObject)

        self.highlightWidgetsParents = {}
        self.calendarSpacersParents = {}


    def resizeEvent(self, event):
        self.resized.emit()
        return super(CalendarWindow, self).resizeEvent(event)
    


    @Slot()
    def resizeDays(self):
        totalSize = self.ui.scrollArea.size().width() - 10
        if totalSize < 500: totalSize = 500
        daysDisplayed = [
            self.ui.Aday_2,
            self.ui.Bday_2,
            self.ui.Cday_2,
            self.ui.Dday_2,
            self.ui.Eday_2,
            self.ui.Fday_2,
            self.ui.Gday_2
        ]
        for dayDisplayed in daysDisplayed:
            dayDisplayed.setFixedWidth(totalSize / 7)



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

        #sort bucketTimes by startTime to prevent strangeness
        """
        bucketTimes.sort(key = lambda bucketUiElement:
                         secondsSinceStartOfWeek(bucketUiElement.startDay.currentText(),
                                                 bucketUiElement.startTime.time())
        """ #no longer needed as Buckets will all be sorted when fetched

        #Add new spacers & widgets for each BucketTimeElement
        for bucket in self.buckets:      
            startTime = bucket.startTime
            endTime = bucket.finishTime

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

            #create a QSpacerItem to space-out self.buckets
            spacerHeight = ((startTime % 86400) - lastEndTime[dayContents] - 20) * timeLenFactor
                                                              #-20 is for name and time
            newSpacer = QSpacerItem(2,spacerHeight, vData=QSizePolicy.Policy.Fixed)
            dayContents.layout().addSpacerItem(newSpacer)
            self.calendarSpacersParents[newSpacer] = dayContents

            #create the bucket itself
            widgetHeight = (endTime - startTime) * timeLenFactor
            newWidget = CalendarBucketElement(bucket.colour)
            #print(bucket.bucketType, bucket.colour)
            newWidget.populateWithTasks(bucket.bucketID, startTime, endTime, widgetHeight + 20)#CBE
            newWidget.setNameAndTime(bucket)
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
    def showTaskItems(self):
        self.taskItemsInTasksList = []
        self.cursor.execute("""
        SELECT name, compatibleBucketType, deadline, estimatedTime, description, maxSessionTime,
                status, recursion, taskID
        FROM Tasks
        """)
        for row in self.cursor.fetchall():
            newTask = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            newTask.setID(row[8])
            newTaskItem = TaskItem(newTask)
            self.ui.tasksList.layout().addWidget(newTaskItem)
            self.taskItemsInTasksList.append(newTaskItem)
            
        
    def setupConnections(self):
        self.resized.connect(self.resizeDays)
        self.HighlightBucketsOnCalendar()
        self.showTaskItems()


if __name__ == "__main__":
    app = QApplication.instance()
    if app == None: app = QApplication()
    window = CalendarWindow()
    window.show()
    window.setupConnections()
    try: sys.exit(app.exec())
    except: app.beep()
