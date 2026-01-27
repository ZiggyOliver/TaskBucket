# Task Arrangement Algorithm AKA please-could-you-spare-a-bucket-for-my-poor-little-task-sir-He's-so-very-cold-and-hungry-sir-He-just-needs-a-bucket-sir

import shutil
import sqlite3
import epoch
import os
import AddBucket
import

shutil.copyfile("TaskBucket_Data.db","TaskBucket_Data_copy.db")

connection = sqlite3.connect("TaskBucket_Data.db")
cursor = connection.cursor()

#finding next buckets
cursor.execute(f"""
SELECT bucketType, startTime, finishTime
FROM Buckets
WHERE startTime > {epoch.now()}

""")

bucketsAfterCurrentTime = []

for fetchedBucket in cursor.fetchall():
    createdBucket = AddBucket.Bucket(fetchedBucket[0],fetchedBucket[1],fetchedBucket[2])
    bucketsAfterCurrentTime.append(createdBucket)

#main loop
for bucket in BucketsAfterCurrentTime:
    if bucket


    
os.remove("TaskBucket_Data_copy.db")
