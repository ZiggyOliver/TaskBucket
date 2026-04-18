import sqlite3
from taskBucketObjects import TaskBucket, Bucket
from uiwidget_calendarBucket import Ui_Form
from CalendarTaskBucketElement import CalendarTaskBucketElement
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor as QColour, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)


class CalendarBucketElement(QWidget, Ui_Form):
    colour = (0,0,0,)
    
    def __init__(self, colourAsRgbString, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.colour = (
            int(colourAsRgbString[0:3]),
            int(colourAsRgbString[3:6]),
            int(colourAsRgbString[6:])
        )
        self.bmiddle.setPalette(QPalette(QColour(),QColour(
            self.colour[0],
            self.colour[1],
            self.colour[2],
            a = 70
        )))
        self.TopTextArea.setPalette(QPalette(QColour(),QColour(
            self.colour[0],
            self.colour[1],
            self.colour[2],
            a = 255
        )))

    def populateWithTasks(self, bucketID, bucketStartTime, bucketEndTime, bucketHeight):

        #fetching applicable taskBuckets from the Database
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT taskID, bucketID, sessionTimeStart, sessionTimeEnd
            FROM TaskBuckets
            WHERE bucketID == {bucketID}
            ORDER BY sessionTimeStart ASC
        """)
        taskBuckets = []
        for row in cursor.fetchall():
            newTaskBucket = TaskBucket(row[0], row[1], row[2], row[3])
            taskBuckets.append(newTaskBucket)
            
        #placing these inside the bucket
        lastEndTime = bucketStartTime
        timeLenFactor = bucketHeight / (bucketEndTime - bucketStartTime)

        for taskBucket in taskBuckets:
            startTime = taskBucket.sessionTimeStart
            endTime = taskBucket.sessionTimeEnd

            #create a QSpacerItem to space-out the taskbuckets
            spacerHeight = startTime * timeLenFactor
            newSpacer = QSpacerItem(2, spacerHeight, vData=QSizePolicy.Policy.Fixed)
            self.bucketContents.layout().addSpacerItem(newSpacer)

            #create the widget for the task itself
            widgetHeight = (endTime - startTime) * timeLenFactor
            newWidget = CalendarTaskBucketElement()
            newWidget.setNameAndTime(taskBucket)
            newWidget.setFixedHeight(widgetHeight)
            newWidget.setAutoFillBackground(True)
            newWidget.setColour(self.colour)
            highlightPalette = QPalette()
            highlightPalette.setColor(QPalette.ColorRole.Window, QColour(0,255,0))
            newWidget.setPalette(highlightPalette)
            self.bucketContents.layout().addWidget(newWidget)
            
            #updateLastEndTime
            lastEndTime = endTime

    def setNameAndTime(self, bucket):
        self.bucketName.setText(bucket.bucketType)
        
        startTimeString = str((bucket.startTime % 86400) // (60**2)).zfill(2) \
                           + ":" + \
                          str(((bucket.finishTime % 86400) // 60) % 60).zfill(2)
        
        endTimeString = str((bucket.finishTime % 86400) // (60**2)).zfill(2) \
                        + ":" + \
                        str(((bucket.finishTime % 86400) // 60) % 60).zfill(2)

        
        
        self.bucketTime.setText(startTimeString + " — " + endTimeString)
