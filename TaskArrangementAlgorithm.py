# Task Arrangement Algorithm AKA please-could-you-spare-a-bucket-for-my-poor-little-task-sir-He's-so-very-cold-and-hungry-sir-He-just-needs-a-bucket-sir

import shutil
import sqlite3
import os
from taskBucketObjects import Task, Bucket, TaskBucket
import epoch
from betterArrange import BetterArrangeTask


def ArrangeTask(taskToPlace):
    print("ArrangeTask called for task with ID " + str(taskToPlace.taskID))
    shutil.copyfile("TaskBucket_Data.db","TaskBucket_Data_copy.db")
    #finding space this week
    
    #finding applicable buckets
    cursor.execute(f"""
        SELECT bucketID, bucketType, startTime, finishTime
        FROM Buckets
        WHERE startTime BETWEEN {epoch.now() - epoch.sow()}
                                AND
                                {taskToPlace.deadline - epoch.sow()}
              AND bucketType == "{taskToPlace.compatibleBucketType}"
                     
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
        print("bucket found this week of type " + createdBucket.bucketType)

    remainingTime = taskToPlace.estimatedTime
    requiredSpace = remainingTime

    for bucket in bucketsAfterCurrentTime:
        if remainingTime  > taskToPlace.maximumSessionTime:
            requiredSpace = taskToPlace.maximumSessionTime

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
        if newSessionEnd <= bucket.finishTime: #implies that there is space in this bucket
            newTaskBucket = TaskBucket(
                taskToPlace.taskID, bucket.bucketID, newSessionStart, newSessionEnd
            )
            print("there is space in bucket with bucketID " + str(bucket.bucketID))
            newTaskBucket.AddTaskBucketToDB(connection = connection)
            connection.commit()
            remainingTime -= requiredSpace
            if remainingTime == 0: break

    #It seems as if we need space in future weeks
    week = epoch.sow() // 604800
    cursor.execute(f"""
        SELECT bucketID, bucketType, startTime, finishTime
        FROM Buckets
        WHERE bucketType = "{taskToPlace.compatibleBucketType}"
    """)
    allBuckets = []
    for fetchedBucket in cursor.fetchall():
        print(fetchedBucket[0], fetchedBucket[1], fetchedBucket[2], fetchedBucket[3])
        createdBucket = Bucket(
            fetchedBucket[1],fetchedBucket[2], fetchedBucket[3]
        )
        createdBucket.setID(fetchedBucket[0])
        allBuckets.append(createdBucket)
        print("bucket found in a future week of type " + createdBucket.bucketType)
    pastDeadline = False
    while remainingTime > 0:
        for bucket in allBuckets:
            if bucket.finishTime + (week*604800) >= taskToPlace.deadline:
                print("could not find enough space for task with ID " + str(taskToPlace.taskID))
                print("seconds Defecit: " + str(remainingTime))
                pastDeadline = True
                break
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
            if newSessionEnd <= bucket.finishTime: #implies that there is space in this bucket
                newTaskBucket = TaskBucket(
                    taskToPlace.taskID, bucket.bucketID, newSessionStart, newSessionEnd
                )
                newTaskBucket.setEpochWeek(week)
                print("there is space in bucket with bucketID " + str(bucket.bucketID))
                newTaskBucket.AddTaskBucketToDB(connection = connection)
                connection.commit()
                remainingTime -= requiredSpace
            week += 1
            if pastDeadline: break
        if pastDeadline: break

        
        
    os.remove("TaskBucket_Data_copy.db")

def ArrangeUnarrangedTasks():
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

    print("===========ArrangeUnarrangedTasks called=================")
    print(cursor)
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
        
        newTask = Task(row[1], row[2], row[3], row[4], row[5], row[6])
        newTask.setID(row[0])

        #ArrangeTask(newTask)
        BetterArrangeTask(newTask)

        
    
    
