import shutil
import sqlite3
import os
from taskBucketObjects import Task, Bucket, TaskBucket
import epoch


def BetterArrangeTask(taskToPlace):
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

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
    ignoreMaxSessionTime = False
    
    while True:
        bucket = allBuckets[bucketCount % len(allBuckets)]

        #stop if the bucket is before the deadline
        if (bucket.startTime + (weekCount)*604800) >= taskToPlace.deadline:
            print(f"""
            stopped looking for buckets when bucket was found with startTime
            {bucket.startTime} in week {weekCount}.
            Seconds Defecit: {remainingTime}
            Minutes Defecit: {remainingTime / 60}

            (current week is {epoch.now() // 604800})
            """)
            pastDeadline = True
            #go back to start to see if there is space leftover from maxSessionTime
            weekCount = weekWhenRun
            bucketCount = 0
            

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

            print("remainingTime in mins", remainingTime / 60)
            print("requiredSpace in mins", requiredSpace / 60)
            

        else:
            print("there is no space in bucket with bucket ID", bucket.bucketID)
            ranOutOfSpace = True

        if (bucketCount + 1) % len(allBuckets) == 0: weekCount += 1
        bucketCount += 1


    if remainingTime <= 0: connection.commit(); print("betterArrangeCommited")
    else:
        print(f"task with ID {taskToPlace.taskID} could not be scheduled")
        connection.rollback()

    del connection
        

