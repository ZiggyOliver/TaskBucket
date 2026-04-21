from PySide6.QtWidgets import QWidget, QDialog as QDialogue
from PySide6.QtCore import Signal, Slot, QTime
from ui_promptReschedule import Ui_Dialog as Ui_Dialogue
from TaskArrangementAlgorithm import ArrangeTask
import sqlite3

class PromptReschedule(QDialogue):
    def __init__(self, task, parent = None):
        super(PromptReschedule, self).__init__()
        self.ui = Ui_Dialogue()
        print("promptReschedule.ui =", self.ui)
        self.ui.setupUi(self)
        print("prompt Reschdule Init Called")


        self.task = task

        self.ui.timeEdit.setTime(QTime().addSecs(task.deadline))


    def RescheduleTask(self, task):
        print("RescheduleTask Called")
        #remove previously created taskBuckets of this task
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        cursor.execute(f"""
            DELETE FROM TaskBuckets
            WHERE taskID == {task.taskID}
        """)

        #Modify this task 
        task.estimatedTime = self.ui.timeEdit.time().msecsSinceStartOfDay // 1000
        task.deadline = self.ui.deadlineEdit.dateTime().toSecsSinceEpoch()
        cursor.execute(f"""
            UPDATE Tasks
            SET estimatedTime = {task.estimatedTime}, deadline = {task.deadline}
        """)

        connection.commit()

        #Arrange the task again
        ArrangeTask(task)
