import sqlite3
from taskBucketObjects import TaskBucket
from uiwidget_calendarTaskBucket import Ui_Form
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor as QColour, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class CalendarTaskBucketElement(QWidget, Ui_Form):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        

    def setNameAndTime(self, taskBucket, bucketTimeStart):
        #find task this taskBucket belongs to
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT name
            FROM Tasks
            WHERE taskID == {taskBucket.task}

        """)
        self.taskName.setText(cursor.fetchone()[0])
        
        absoluteStartTime = taskBucket.sessionTimeStart + bucketTimeStart
        absoluteEndTime = taskBucket.sessionTimeEnd + bucketTimeStart
        
        startTimeString = str((absoluteStartTime % 86400)\
                              // (60**2)).zfill(2) + ":" + \
                          str(((absoluteStartTime % 86400) // 60) % 60).zfill(2)
        
        endTimeString = str((absoluteEndTime % 86400) // (60**2)).zfill(2) \
                        + ":" + \
                        str(((absoluteEndTime % 86400) // 60) % 60).zfill(2)

        self.taskTime.setText(startTimeString + " — " + endTimeString)

    def setColour(self, colourAsRgbTuple):
        self.taskBucket.setPalette(QPalette(QColour(),QColour(
            colourAsRgbTuple[0],
            colourAsRgbTuple[1],
            colourAsRgbTuple[2],
            a = 255
        )))
        


        
