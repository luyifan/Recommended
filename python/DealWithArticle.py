import os
import sys
import pickle

reload ( sys )
sys.setdefaultencoding('utf-8')

def dealWithArticle ( articleFilename ):
    articleDict = {}
    nowNum = 0
    f = open ( articleFilename , "r" )
    for oneArticle in f:
        nowNum += 1
        itemList = oneArticle.split(" ")
        oneArticleDict = {}
        articleId = int ( itemList [ 0 ] )
        if articleId == -1:
            break
        oneArticleDict [ "date" ] = int ( itemList [ 1 ] )
        oneArticleDict [ "boardId" ] = int ( itemList [ 2 ] )
        oneArticleDict [ "items" ] = {}
        n = int ( itemList [ 3 ] )
        j = 4
        for i in range ( 0 , n ):
            itemId = int ( itemList [ j ] )
            itemValue = float ( itemList [ j + 1 ] )
            j = j + 2
            oneArticleDict [ "items" ][ itemId ] = itemValue
        articleDict [ articleId ] = oneArticleDict
        if ( nowNum > 100 ):
            print "."
            nowNum = 0
    return articleDict
def store_pickle ( filename , dictionary ):
    with open ( filename , "wb" ) as fPickleFile:
        pickle.dump ( dictionary , fPickleFile )
        fPickleFile.close ( )
if __name__ == "__main__":
    if len ( sys.argv ) < 2:
        print "No programPath"
        sys.exit(1)
    programPath = sys.argv [ 1 ]
    articleFilename = os.path.join ( programPath , "data/articleData" )
    articleDict = dealWithArticle ( articleFilename )
    articlePickleFilename = os.path.join ( programPath , "data/articleDict.pickle" )
    store_pickle ( articlePickleFilename , articleDict )
