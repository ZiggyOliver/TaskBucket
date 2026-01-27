import sqlite3

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


def AddTaskBucketToDB(taskBucket):
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

    cursor.execute(f"""
    INSERT INTO TaskBuckets (taskID, bucketID, sessionTimeStart, SessionTimeEnd)
    VALUES ({taskBucket.task}, {taskBucket.bucket}, {taskBucket.sessionTimeStart}, {taskBucket.sessionTimeEnd})
    """)
    connection.commit()
