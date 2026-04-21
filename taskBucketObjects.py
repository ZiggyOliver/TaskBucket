import sqlite3


class Task:
    taskID = float("nan")
    taskName = ""
    compatibleBucketType = ""
    deadline = float("nan")
    estimatedTime = float("nan")
    description = ""
    maximumSessionTime = float("nan")
    status = ""
    recursion = ""

    def __init__(self, taskName, compatibleBucketType, deadline, estimatedTime, description,
                 maximumSessionTime, status, recursion):

        self.taskName = taskName
        self.compatibleBucketType = compatibleBucketType
        self.deadline = deadline
        self.estimatedTime = estimatedTime
        self.description = description
        self.maximumSessionTime = maximumSessionTime

    def setID(self, ID): self.taskID = ID
        

    def AddTaskToDB(self):
        connection = sqlite3.connect("TaskBucket_Data.db")
        cursor = connection.cursor()
        operationString = f"""
        INSERT INTO Tasks (name, compatibleBucketType, deadline, description, estimatedTime,
        maxSessionTime)
        VALUES ("{self.taskName}", "{self.compatibleBucketType}",
                 {self.deadline}, "{self.description}", {self.estimatedTime},
                 {self.maximumSessionTime})
        """

        cursor.execute(operationString)
        print(operationString)
        connection.commit()
        print("task added succesfully to database")

class Bucket:
    bucketID = float("nan")
    bucketType = ""
    startTime = float("nan")
    finishTime = float("nan")
    colour = None

    def __init__(self, bucketType, startTime, finishTime):
        self.bucketType = bucketType
        self.startTime = startTime
        self.finishTime = finishTime

    def setID(self, bucketID): self.bucketID = bucketID
    
    def setColour(self, colourAsRgb): self.colour = colourAsRgb

    def AddBucketToDB(self, connection = sqlite3.connect("TaskBucket_Data.db")):
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO Buckets (bucketType, startTime, finishTime, bucketColour)
        VALUES ("{self.bucketType}", {self.startTime}, {self.finishTime}, "{self.colour}")
        """)

class TaskBucket:
    task = float("nan")
    bucket = float("nan")
    sessionTimeStart = float("nan")
    sessionTimeEnd = float("nan")

    def __init__(self, task, bucket, sessionTimeStart, sessionTimeEnd):
        self.task = task
        self.bucket = bucket
        self.sessionTimeStart = sessionTimeStart
        self.sessionTimeEnd = sessionTimeEnd


    def AddTaskBucketToDB(self, connection = sqlite3.connect("TaskBucket_Data.db")):
        print("addTaskBUcketToDBCalled")
        cursor = connection.cursor()

        cursor.execute(f"""
        INSERT INTO TaskBuckets (taskID, bucketID, sessionTimeStart, SessionTimeEnd)
        VALUES ("{self.task}", {self.bucket}, {self.sessionTimeStart},{self.sessionTimeEnd})
        """)
