import sqlite3

def GenerateDatabase():
    connection = sqlite3.connect("TaskBucket_Data.db")
    cursor = connection.cursor()

    #Task table generation
    cursor.execute("""
    CREATE TABLE Tasks(
        taskID INTEGER PRIMARY KEY,
        name TEXT,
        compatibleBucketType TEXT,
        deadline INTEGER,
        description TEXT,
        estimatedTime INTEGER,
        maxSessionTime INTEGER,
        status TEXT,
        recursion TEXT)
    """)

    #Bucket table generation
    cursor.execute("""
    CREATE TABLE Buckets(
        bucketID INTEGER PRIMARY KEY,
        bucketType TEXT,
        startTime INTEGER,
        finishTime INTEGER)
    """)

    #TaskBucket table Generation
    cursor.execute("""
    CREATE TABLE TaskBuckets(
        taskBucketID INTEGER PRIMARY KEY,
        taskID INTEGER REFERENCES Tasks (taskID),
        bucketID INTEGER REFERENCES Buckets (bucketID),
        sessionTimeStart INTEGER,
        sessionTimeEnd INTEGER)
    """)


