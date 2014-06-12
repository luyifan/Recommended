import sys
import os
import pickle
from DealWithArticle import store_pickle
reload ( sys )
sys.setdefaultencoding('utf-8')

def dealWithRecord ( filename ):
    recordDict = {}
    f = open ( filename , "r" )
    nowNum = 0
    for oneRecord in f:
        itemList = oneRecord.split(" ")
        userId = int ( itemList [ 0 ] )
        if userId == -1:
            break
        oneRecordDict = {}
        oneRecordDict [ "date" ] = int ( itemList [ 1 ] )
        oneRecordDict [ "type" ] = int ( itemList [ 2 ] )
        oneRecordDict [ "articleId" ] = int ( itemList [ 3 ] )
        if not (userId in recordDict):
            recordDict [ userId ] = []
        recordDict [ userId ].append ( oneRecordDict )
    return  recordDict

if __name__ == "__main__":
    if len ( sys.argv ) < 2:
        print "No programPath"
        sys.exit ( 1 )
    programPath = sys.argv [ 1 ]
    recordFilename = os.path.join ( programPath , "data/recordData" )
    recordDict = dealWithRecord ( recordFilename )
    recordPickleFilename = os.path.join ( programPath , "data/recordDict.pickle" )
    store_pickle ( recordPickleFilename , recordDict )


