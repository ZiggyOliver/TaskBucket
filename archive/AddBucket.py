import sqlite3

class Bucket:
    bucketID = float("nan")
    bucketType = ""
    startTime = float("nan")
    finishTime = float("nan")

    def __init__(self,bucketID, bucketType, startTime, finishTime):
        self.bucketID = bucketID
        self.bucketType = bucketType
        self.startTime = startTime
        self.finishTime = finishTime

def AddBucketToDB(bucketToAdd):
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

    cursor.execute(f"""
    INSERT INTO Buckets (bucketType, startTime, finishTime)
    VALUES ("{bucketToAdd.bucketType}", {bucketToAdd.startTime}, {bucketToAdd.finishTime})
    """)
    connection.commit()
