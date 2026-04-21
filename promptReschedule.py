from PySide6.QtWidgets import QWidget, QDialog as QDialogue
from PySide6.QtCore import Signal, Slot
from ui_promptReschedule import Ui_Dialogue
from TaskArrangementAlgorithm import ArrangeTask

class PromptReschedule(QDialogue, Ui_Dialogue):
    @Slot()
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        print("prompt Reschdule Init Called")

    def RescheduleTask(task, timeNeeded, deadline):
        print("RescheduleTask Called")
        #remove previously created taskBuckets of this task
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        cursor.execute(f"""
        DELETE FROM TaskBuckets
        WHERE taskID = {task.taskID}
        """)

        #Modify this task 
        task.estimatedTime = timeNeeded
        task.deadline = deadline
        cursor.execute(f"""
        UPDATE Tasks
        SET estimatedTime = {task.estimatedTime}, deadline = {task.deadline}
        """)

        connection.commit()

        #Arrange the task again
        ArrangeTask(task)
