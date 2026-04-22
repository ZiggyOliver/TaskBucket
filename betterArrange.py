import shutil
import sqlite3
import os
from taskBucketObjects import Task, Bucket, TaskBucket
import epoch

connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()

def BetterArrangeTask(taskToPlace):
    print("betterArrangeTask called for task with taskID", taskToPlace.taskID)
    shutil.copyfile("TaskBucket_Data.db", "TaskBucket_Data_copy.db")
    #fetch applicable buckets from the databse

    cursor.execute(f"""
        SELECT bucketID, bucketType, startTime, finishTime
        FROM Buckets
        WHERE bucketType = "{taskToPlace.compatibleBucketType}"
    """)
    allBuckets = []
    for row in cursor.fetchall():
        newBucket = Bucket(row[1], row[2], row[3])
        newBucket.setID(row[0])
        allBuckets.append(newBucket)

    weekWhenRun = epoch.sow() // 604800
    weekCount = weekWhenRun
    pastDeadline = False
    bucketCount = 0
    remainingTime = taskToPlace.estimatedTime
    requiredSpace = taskToPlace.maximumSessionTime
    ranOutOfSpace = False
    while pastDeadline == False:
        bucket = allBuckets[bucketCount % len(allBuckets)]

        #stop if the bucket is before the deadline
        if (bucket.startTime + weekCount*604800) >= taskToPlace.deadline:
            print(f"""
            stopped looking for buckets when bucket was found with startTime
            {bucket.startTime} in week {weekCount}
            """)
            pastDeadline = True
            break

        #find the last item in this bucket to determine the space left
        cursor.execute(f"""
            SELECT sessionTimeEnd
            FROM TaskBuckets
            WHERE bucketID = {bucket.bucketID} AND epochWeek = {weekCount}
            ORDER BY sessionTimeEnd DESC
        """)
        lastSessionTimeEndTuple = cursor.fetchone()
        if lastSessionTimeEndTuple == None: lastSessionTimeEnd = 0
        else: lastSessionTimeEnd = lastSessionTimeEndTuple[0]
        
        print(lastSessionTimeEnd)
        spaceInBucket = bucket.finishTime - bucket.startTime - lastSessionTimeEnd

        if spaceInBucket >= requiredSpace:
            newSessionStart = lastSessionTimeEnd
            newSessionEnd = newSessionStart + requiredSpace
            
            newTaskBucket = TaskBucket(
                    taskToPlace.taskID, bucket.bucketID, newSessionStart, newSessionEnd
                )
            newTaskBucket.setEpochWeek(weekCount)
            print("there is space in bucket with bucketID " + str(bucket.bucketID))
            newTaskBucket.AddTaskBucketToDB(connection = connection)
            remainingTime -= requiredSpace
            if remainingTime < taskToPlace.maximumSessionTime: requiredSpace = remainingTime
            if remainingTime <= 0: break
            

        else:
            print("there is no space in bucket with bucket ID", bucket.bucketID)
            ranOutOfSpace = True

        weekCount += 1

    if ranOutOfSpace == False: connection.commit()
