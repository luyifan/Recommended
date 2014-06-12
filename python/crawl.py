import os
import sys
import pickle
import urllib2
import requests
import re
from DealWithArticle import store_pickle
reload ( sys )
sys.setdefaultencoding ( "utf-8" )
def getOneUrl ( url ):
    content = urllib2.urlopen ( url , timeout = 120 ).read()
    #print ( content )
    start = content.find ( "<blockquote>" )
    final = content.find ( "</blockquote>" , start )
    content = content [ start : final ]
    titleStart = content.find ( "<b>" )
    titleFinal = content.find ( "</b>" , titleStart )
    title = content [ titleStart + 3 : titleFinal ]
    contentStart = content.find ( "<span" , titleFinal )
    contentStart = content.find ( ">" , contentStart )
    contentFinal = content.find ( "</span>"  , contentStart )
    content = content[ contentStart + 1: contentFinal ]
    return ( title , content )
def cc98login ( url ):
    session = requests.session()

    login_data = { 'username': 'luyifan', 'password':'luyifan1993' , 'userhidden' : '2' , 'submit' : 'submit' }
    re = session.post ( url , data = login_data )
    re = session.get ("http://www.cc98.org/dispbbs.asp?boardID=146&ID=4376374&page=")
    print ( re.text )
    return re
if __name__ == "__main__":
    boardIdList =[]
    idList = []
    articleList = []
    #cc98login ( "http://www.cc98.org/login.asp" )
    programPath  = sys.argv [ 1 ]
    filename = os.path.join ( programPath , "data/postAbsence.txt" )
    f = open ( filename , "r" )
    testname = os.path.join ( programPath , "data/test.txt" )
    ftest = open ( testname , "w" )
    for line in f:
        lineList = line.split(" ")
        if ( lineList [ 1 ].find ( "NULL" ) != -1 ):
            continue
        idList.append ( int ( lineList [ 0 ] ) )
        boardIdList.append ( int ( lineList [ 1 ] ) )
    f.close ( )
    listLen = len ( idList )
    ok = False
    for i in range ( listLen ):
        if ( ok == False ):
            if  boardIdList [ i ] == 193 and idList [ i ] == 4253967:
                ok = True
            else:
                continue
        url = "http://www.cc98.org/dispbbs.asp?boardID=" + str ( boardIdList [ i ] ) + "&ID=" + str ( idList [ i ] )
        #print ( url )
        ( title , content ) = getOneUrl( url )
        if title.strip() == "" and content.strip() == "":
            print ( "RootID " + str ( idList [ i ] ) + " BoardID " + str ( boardIdList [ i ] ) )
            continue
        #print ( title )
        #print ( content )
        oneArticle = {}
        oneArticle[ "RootID" ] = idList [ i ]
        oneArticle[ "BoardID" ] = boardIdList [ i ]
        oneArticle [ "title" ] = title
        oneArticle [ "content" ] = content
        ftest.write ( "RootID " + str ( idList [ i ] ) + " BoardID " + str ( boardIdList [ i ] ) )
        ftest.write ( '\n' )
        ftest.write ( title )
        ftest.write ( '\n' )
        ftest.write ( content )
        ftest.write ( '\n' )
        articleList.append ( oneArticle )
        print ( i )
    filename = os.path.join ( programPath , "data/newArticle.pickle" )
    store_pickle ( filename , articleList )
    ftest.close ( )

