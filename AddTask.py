import sqlite3


class Task:
    taskID = float("nan")
    taskName = ""
    compatibleBucketType = ""
    deadline = float("nan")
    estimatedTime = float("nan")

    def __init__(self, compatibleBucketType, deadline, estimatedTime, description):
        self.compatibleBucketType = compatibleBucketType
        self.deadline = deadline
        self.estimatedTime = estimatedTime
        self.description = description
        

def AddTaskToDB(taskToAdd):
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

    operationString = f"""
    INSERT INTO Tasks (name, compatibleBucketType, deadline, description, estimatedTime)
    VALUES ("{taskToAdd.taskName}", "{taskToAdd.compatibleBucketType}", {taskToAdd.deadline}, "{taskToAdd.description}", {taskToAdd.estimatedTime})
    """

    cursor.execute(operationString)
    print(operationString)
    connection.commit()
