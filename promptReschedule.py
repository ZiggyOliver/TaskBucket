from PySide6.QtWidgets import QWidget, QDialog as QDialogue
from PySide6.QtCore import Signal, Slot, QDate, QTime, QDateTime
from ui_promptReschedule import Ui_Dialog as Ui_Dialogue
from betterArrange import BetterArrangeTask
from TaskArrangementAlgorithm import ArrangeUnarrangedTasks
import sqlite3

class PromptReschedule(QDialogue):
    def __init__(self, task, calendarWindow = None, parent = None):
        super(PromptReschedule, self).__init__()
        self.ui = Ui_Dialogue()
        print("promptReschedule.ui =", self.ui)
        self.ui.setupUi(self)
        print("prompt Reschdule Init Called")


        self.task = task
        self.ui.timeEdit.setTime(QTime.fromMSecsSinceStartOfDay(task.estimatedTime*1000))
        self.ui.deadlineEdit.setDateTime(QDateTime.fromSecsSinceEpoch(task.deadline))

        self.calendarWindow = calendarWindow

    @Slot()
    def RescheduleTask(self):
        print("RescheduleTask Called")
        #remove previously created taskBuckets of this task
        #actually, just remove all the task buckets because they can be replaced and moving one task
        #can create weird edge cases
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        print(self.task)
        cursor.execute(f"""
            DELETE FROM TaskBuckets
        """)

        #Modify this task 
        self.task.estimatedTime = self.ui.timeEdit.time().msecsSinceStartOfDay() // 1000
        self.task.deadline = self.ui.deadlineEdit.dateTime().toSecsSinceEpoch()
        cursor.execute(f"""
            UPDATE Tasks
            SET estimatedTime = {self.task.estimatedTime}, deadline = {self.task.deadline}
        """)

        connection.commit()

        #Arrange the task again
        #BetterArrangeTask(self.task)

        #to make up for deleting all tasks, now put them all back
        ArrangeUnarrangedTasks()
        self.calendarWindow.HighlightBucketsOnCalendar()
