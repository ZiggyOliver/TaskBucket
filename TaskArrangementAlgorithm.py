# Task Arrangement Algorithm AKA please-could-you-spare-a-bucket-for-my-poor-little-task-sir-He's-so-very-cold-and-hungry-sir-He-just-needs-a-bucket-sir

import shutil
import sqlite3
import os
from taskBucketObjects import Task, Bucket, TaskBucket
import epoch

connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()

def ArrangeTask(taskToPlace):
    print("ArrangeTask called for task with ID " + str(taskToPlace.taskID))
    shutil.copyfile("TaskBucket_Data.db","TaskBucket_Data_copy.db")
    #finding space this week
    
    #finding applicable buckets
    cursor.execute(f"""
        SELECT bucketID, bucketType, startTime, finishTime
        FROM Buckets
        WHERE startTime BETWEEN {epoch.now() - epoch.sow()} AND {taskToPlace.deadline - epoch.sow()}
        ORDER BY startTime ASC
    """)

    bucketsAfterCurrentTime = [] #buckets after current time is only this week

    for fetchedBucket in cursor.fetchall():
        print(fetchedBucket[0], fetchedBucket[1], fetchedBucket[2], fetchedBucket[3])
        createdBucket = Bucket(
            fetchedBucket[1],fetchedBucket[2], fetchedBucket[3]
        )
        createdBucket.setID(fetchedBucket[0])
        bucketsAfterCurrentTime.append(createdBucket)
        print("bucket found this week of type" + createdBucket.bucketType)

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
            ORDER BY sessionTimeEnd DESC
        """)
        newSessionStart = cursor.fetchone()
        if newSessionStart == None: newSessionStart = 0
        else: newSessionStart = newSessionStart[0]
        newSessionEnd = newSessionStart + requiredSpace
        newTaskBucket = TaskBucket(
            taskToPlace.taskID, bucket.bucketID, newSessionStart, newSessionEnd)
        print("line52")
        newTaskBucket.AddTaskBucketToDB(connection = connection)
        connection.commit()
        
        
    os.remove("TaskBucket_Data_copy.db")

def ArrangeUnarrangedTasks():
    print("===========ArrangeUnarrangedTasks called=================")
    cursor.execute("""
        SELECT taskID, name, compatibleBucketType, deadline, estimatedTime, description, \
                maxSessionTime, status, recursion
        FROM Tasks
    """)
    allTasksTuple = cursor.fetchall()
    for row in allTasksTuple:
        cursor.execute(f"""
            SELECT taskBucketID
            FROM TaskBuckets
            WHERE taskID = {row[0]}
        """)
        #print(cursor.fetchone())
        if cursor.fetchone() != None: continue
        
        newTask = Task(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        newTask.setID(row[0])

        ArrangeTask(newTask)
