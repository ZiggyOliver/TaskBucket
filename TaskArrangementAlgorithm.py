import shutil
import sqlite3
import epoch
import os

shutil.copyfile("./TaskBucket_Data.db","./TaskBucket_Data_copy.db")

connection = sqlite3.connect("TaskBucket_Data")
cursor = connection.cursor()

#finding next buckets
print(cursor.execute(f"""
SELECT bucketID
FROM Buckets
WHERE sessionTimeStart > {epoch.now()}

"""))


os.remove("./TaskBucket_Data_copy")

