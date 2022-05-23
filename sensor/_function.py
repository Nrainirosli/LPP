from collections import defaultdict
from ast import literal_eval
from pymongo import MongoClient
from calendar import monthrange
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

username_mongo = 'r0ot2o2o'
password_mongo = 'peroton919'
database_mongo = 'PADDY'


def dataframeRaw(site_mbusid,start,end):
    global username_mongo, password_mongo, database_mongo
    startnew = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    endnew = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    username = username_mongo
    password= password_mongo

    conn = MongoClient("mongodb://0.0.0.0:27017/", waitQueueTimeoutMS=2000)
    # conn = MongoClient("mongodb://mongo:27017/",username=username, password=password, waitQueueTimeoutMS=2000)

    #conn = MongoClient() 
    mydb_mongo = conn[database_mongo]
    mytable = mydb_mongo[site_mbusid]
    df = list(mytable.find({
        "datecreated": {
            "$gte": startnew,
            "$lte": endnew
        }
    }, {'_id': False}).sort([("datecreated", 1)]))
    return df

def dataframeOneSite(site_mbusid,start,end):
    conn = MongoClient("mongodb://0.0.0.0:27017/", waitQueueTimeoutMS=2000)
    # conn = MongoClient("mongodb://mongo:27017/",username=username, password=password, waitQueueTimeoutMS=2000)

    #conn = MongoClient()
    startnew = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    endnew = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    mydb_mongo = conn[database_mongo]
    mytable = mydb_mongo[site_mbusid]
    df = list(mytable.find({}, {'_id': False}).sort([("datecreated", -1)]).limit(1))
    return df

def checkDatabase(tb):
    conn = MongoClient("mongodb://0.0.0.0:27017/", waitQueueTimeoutMS=2000)

    db = conn.database

    db_mongo = conn[database_mongo]
    collection = db_mongo[tb]

    return collection

def insertDataframe(df, tb):
    conn = MongoClient("mongodb://0.0.0.0:27017/", waitQueueTimeoutMS=2000)

    db = conn.database

    db_mongo = conn[database_mongo]
    collection = db_mongo[tb]

    collection.insert_one(df)

def updateOneItem(old_value, new_value, tb):
    conn = MongoClient("mongodb://0.0.0.0:27017/", waitQueueTimeoutMS=2000)

    db = conn.database

    db_mongo = conn[database_mongo]
    collection = db_mongo[tb]

    collection.update_one(old_value, new_value)