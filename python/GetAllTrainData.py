import os
import sys
import pickle
from DealWithArticle import store_pickle
reload ( sys )
sys.setdefaultencoding ('utf-8')
DIFFERENCEDATE = 1440
FRONTRECORD = 5
def load_pickle ( filename ):
    with open ( filename , "rb" ) as f:
        dictionary  = pickle.load ( f )
        f.close()
    return dictionary

def getAllTrainData ( recordFilename , articleFilename ):
    recordDict = load_pickle ( recordFilename )
    articleDict = load_pickle ( articleFilename )
    trainDict = {}
    for userId in recordDict:
        trainDict [ userId ] = [];
        lastleft = 0
        nowNum = 0
        listLen = len ( recordDict [ userId ] )
        for right in range ( 0 , listLen ):
            oneTrainRecord = {}
            articleId = recordDict [ userId ][ right ][ "articleId" ]
            #print ( articleId )
            if not ( articleId in articleDict ):
                print "No such articleId: " + str ( articleId )
                continue
            oneTrainRecord [ "items" ] = articleDict [ articleId ][ "items" ]
            oneTrainRecord [ "boardId" ] = articleDict [ articleId ][ "boardId" ]
            left = lastleft
            while recordDict [ userId ][ right ][ "date" ] - recordDict [ userId ][ left ][ "date" ] >  DIFFERENCEDATE:
                left += 1
            if left == right:
                left = right - FRONTRECORD
                if left < 0:
                    left = 0
            lastleft = left
            for i in range ( 0 , 3 ):
                oneTrainRecord [ i ] = {}
                oneTrainRecord [ i ][ "boards" ] = {}
                oneTrainRecord [ i ][ "items" ] = {}
            count = 0
            for ll in range ( left , right ):
                theType = recordDict [ userId ][ ll ][ "type" ]
                articleId = recordDict [ userId ][ ll ][ "articleId" ]
                if not ( articleId in articleDict ):
                    continue
                items = articleDict [ articleId ][ "items" ]
                board = articleDict [ articleId ][ "boardId" ]
                if board in oneTrainRecord [ theType ][ "boards" ]:
                    oneTrainRecord [ theType ][ "boards" ][ board ] += 1.0
                else:
                    oneTrainRecord [ theType ][ "boards" ][ board ] = 1.0
                for item in items:
                    if item in oneTrainRecord [ theType ][ "items" ]:
                        oneTrainRecord [ theType ][ "items" ][ item ] += articleDict [ articleId ][ "items" ][ item ]
                    else:
                        oneTrainRecord [ theType ][ "items" ][ item ] = articleDict [ articleId ][ "items" ][ item ]
                count += 1
            #print count
            if count != 0:
                for i in range ( 0 , 3 ):
                    for board in oneTrainRecord [ i ][ "boards" ]:
                        oneTrainRecord [ i ][ "boards" ][ board ] /= count
                    for item in oneTrainRecord [ i ][ "items" ]:
                        oneTrainRecord [ i ][ "items" ][ item ] /= count
                    #print oneTrainRecord [ i ][ "boards" ]
                    #print oneTrainRecord [ i ][ "items" ]
            trainDict[ userId ].append ( oneTrainRecord )
            if nowNum > 100:
                print ( "." )
                nowNum = 0
    print trainDict
    return trainDict

if __name__ ==  "__main__":
    if len ( sys.argv ) < 2:
        print "No programPath"
        sys.exit(1)
    if len ( sys.argv ) >= 3:
        FRONTRECORD = int ( sys.argv [ 2 ] )
    programPath = sys.argv [ 1 ]
    recordPickleFilename = os.path.join ( programPath , "data/recordDict.pickle" )
    articlePickleFilename = os.path.join ( programPath , "data/articleDict.pickle" )
    trainDict = getAllTrainData ( recordPickleFilename , articlePickleFilename)
    trainPickleFilename = os.path.join ( programPath , "data/recordTrain.pickle" )
    store_pickle ( trainPickleFilename , trainDict )
