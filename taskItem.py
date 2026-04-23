from PySide6.QtWidgets import QWidget, QDialogButtonBox as QDialogueButtonBox
from PySide6.QtGui import QColor as QColour, QPalette
from ui_taskItem import Ui_taskItem
from promptReschedule import PromptReschedule
import sqlite3


class TaskItem(QWidget, Ui_taskItem):
    def __init__(self, task, calendarWindow = None, parent = None):
        super(TaskItem, self).__init__()
        self.ui = Ui_taskItem()
        self.ui.setupUi(self)

        #set colour to the colour of the bucket
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT bucketColour
            FROM Buckets
            WHERE BucketType == "{task.compatibleBucketType}"
        """)
        colourString = cursor.fetchone()[0]

        print(self.ui)
        
        self.ui.centralwidget.setPalette(QPalette(QColour(70,70,70),QColour(
            int(colourString[0:3]),
            int(colourString[3:6]),
            int(colourString[6:]),
            a = 255
        )))

        #set Name to name of the task
        self.ui.taskName.setText(task.taskName)

        #setup reschedule button connection
        print(task)
        print(task.taskID)

        """
        taskOptionsWindow = PromptReschedule(task)
        taskOptionsWindow.show()
        
        """
        print("name in taskItem is ", __name__)
        def PromptPromptReschedule():
            self.dialogue = PromptReschedule(task, calendarWindow = calendarWindow)
            self.dialogue.show()
            okButton = self.dialogue.ui.buttonBox.button(QDialogueButtonBox.Ok)
            okButton.clicked.connect(self.dialogue.RescheduleTask)

        
        self.ui.rescheduleButton.clicked.connect(PromptPromptReschedule)
        
        
        
    
