# Task Arrangement Algorithm AKA please-could-you-spare-a-bucket-for-my-poor-little-task-sir-He's-so-very-cold-and-hungry-sir-He-just-needs-a-bucket-sir

import shutil
import sqlite3
import epoch
import os
import AddBucket
import AddTaskBucket

connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()

def ArrangeTask(taskToPlace):
    shutil.copyfile("TaskBucket_Data.db","TaskBucket_Data_copy.db")

    #finding next buckets
    cursor.execute(f"""
        SELECT bucketID, bucketType, startTime, finishTime
        FROM Buckets
        WHERE startTime BETWEEN {epoch.now()} AND {taskToPlace.deadline}
        ORDER BY startTime ASC
    """)

    bucketsAfterCurrentTime = []

    for fetchedBucket in cursor.fetchall():
        print(fetchedBucket[0], fetchedBucket[1], fetchedBucket[2], fetchedBucket[3])
        createdBucket = AddBucket.Bucket(
            fetchedBucket[0],fetchedBucket[1],fetchedBucket[2], fetchedBucket[3]
        )
        bucketsAfterCurrentTime.append(createdBucket)

    for bucket in bucketsAfterCurrentTime:
        if taskToPlace.estimatedTime > taskToPlace.maximumSessionTime:
            requiredSpace = taskToPlace.maximumSessionTime
        else:
            requiredSpace = taskToPlace.estimatedTime

        #finding space in current bucket
        print("bucketID: " + str(bucket.bucketID))
        cursor.execute(f"""
            SELECT sessionTimeEnd
            FROM TaskBuckets
            WHERE bucketID == {bucket.bucketID}
            ORDER BY sessionTimeEnd
        """)
        newSessionStart = cursor.fetchone()
        if newSessionStart == None: newSessionStart = bucket.startTime
        newSessionEnd = newSessionStart + taskToPlace.estimatedTime
        newTaskBucket = AddTaskBucket.TaskBucket(
            taskToPlace.taskID, bucket.bucketID, newSessionStart, newSessionEnd)
        AddTaskBucket.AddTaskBucketToDB(newTaskBucket)
        
        
    os.remove("TaskBucket_Data_copy.db")
