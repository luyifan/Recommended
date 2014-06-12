import os
import sys
import getopt
import pickle
import math
import random
from DealWithArticle import store_pickle
from GetAllTrainData import load_pickle
reload ( sys )
ZERO = 0.00001
sys.setdefaultencoding ( 'utf-8' )
def initializeArgv ( opts ):
    global K
    global sigma
    global Lambda
    global iterations
    global times
    global learn_rate
    global sigma_sq
    K = 128
    sigma = 0.1
    Lambda = 0.02
    iterations = 1000
    times = 10
    learn_rate = 0.1
    for opt , arg in opts:
        if opt in ( "-k", "--K" ):
            K =  int ( arg )
        elif opt in ( "-s", "--sigma" ):
            sigma = float ( arg )
        elif opt in ( "-l" , "--lambda" ):
            Lambda = float ( arg )
        elif opt in ( "-i" , "--iterations" ):
            iterations = int ( arg )
        elif opt in ( "-t" , "--times" ):
            times = int ( arg )
        elif opt in ( "-r" , "--learn_rate" ):
            learn_rate = float ( arg )
    #print ( K )
    #print ( sigma )
    #print ( Lambda )
    #print ( iterations )
    #print ( times )
    sigma_sq = sigma * sigma

def initialList ( ):
    global itemList
    global boardList
    global userIdList
    itemList = []
    boardList = []
    userIdList = []
    for articleId in articleDict:
        boardId = articleDict [ articleId ][ "boardId" ]
        items = articleDict [ articleId ][ "items" ]
        if not ( boardId in boardList ):
            boardList.append ( boardId )
        for itemId in items:
            if not ( itemId in itemList):
                itemList.append ( itemId )
    for userId in trainDict:
        if not ( userId in userIdList):
            userIdList.append( userId )
    #print userIdList
def ran_gaussian ( mean , stdev ):
    while True:
        while True:
            u = random.random ( )
            if math.fabs ( u ) > ZERO:
                break
        v = 1.7156 * ( random.random() - 0.5 )
        x = u - 0.449871
        y = math.fabs ( v ) + 0.386595
        Q = x*x + y*(0.19600*y-0.25472*x)
        if Q< 0.27597:
            break
        if Q <= 0.27846 and  v*v > ( -4.0*u*u*math.log(u)):
            break
    return v/u
def initialAllParameter():
    global parameter
    parameter = {}
    parameter [ "Witem" ] = {}
    for item in itemList:
        parameter [ "Witem" ][ item ] = ran_gaussian ( 0 , sigma_sq )
    parameter [ "Wboard" ] = {}
    for board in boardList:
        parameter [ "Wboard" ][ board ] = ran_gaussian ( 0 , sigma_sq )

    parameter [ "Vuser" ] = []
    for k in range ( K ):
        oneKparameter = {}
        for user in userIdList:
            oneKparameter [ user ] = ran_gaussian ( 0 , sigma_sq )
        parameter[ "Vuser" ].append ( oneKparameter )

    parameter [ "Vitem" ] = []
    for k in range ( K ):
        oneKparameter = {}
        for item in itemList:
            oneKparameter [ item ] = ran_gaussian ( 0 , sigma_sq )
        parameter [ "Vitem" ].append ( oneKparameter )

    for i in range ( 0 , 3 ):
        parameter [ i ] = {}
        parameter [ i ][ "Vitem" ] = []
        for k in range ( K ):
            oneKparameter = {}
            for item in itemList:
                oneKparameter [ item ] = ran_gaussian ( 0 , sigma_sq )
            parameter [ i ][ "Vitem" ].append ( oneKparameter )

    parameter [ "Vboard" ] = []
    for k in range ( K ):
        oneKparameter = {}
        for board in boardList:
            oneKparameter [ board ] = ran_gaussian ( 0 , sigma_sq )
        parameter [ "Vboard" ].append ( oneKparameter )

    for i in range ( 0 , 3 ):
        parameter [ i ][ "Vboard" ] = []
        for k in range ( K ):
            oneKparameter = {}
            for board in boardList:
                oneKparameter [ board ] = ran_gaussian ( 0 , sigma_sq )
            parameter [ i ][ "Vboard" ].append ( oneKparameter )

    #for line in parameter:
    #    print line
    #    print parameter [ line ]

def calculateEta ( userId , oneRecord ):
    global eta
    eta = []
    for f in range ( K ):
        eta.append ( parameter [ "Vuser" ][ f ][ userId ] )

    for theType in range ( 0 , 3):
        for board in oneRecord[ theType ][ "boards" ]:
            value = oneRecord [ theType ][ "boards" ][ board ]
            for f in range ( K ):
                eta [ f ] += parameter [ theType ][ "Vboard" ][ f ][ board ]*value
        for item in oneRecord [ theType ][ "items" ]:
            value =oneRecord [ theType ][ "items" ][ item ]
            for f in range ( K ):
                eta [ f ] += parameter [ theType ][ "Vitem" ][ f ][ item ]*value

def calculatePuti ( item , board ):
    puti = parameter [ "Witem" ][ item ] + parameter [ "Wboard" ][ board ]
    for f in range ( K ):
        puti += eta [ f ]*( parameter [ "Vitem" ][ f ][ item ] + parameter[ "Vboard" ][ f ][ board ] )
        puti += parameter [ "Vitem" ][ f ][ item ]*parameter [ "Vboard" ][ f ][ board ]

    return puti

def logistic ( delta ):
    return 1/( 1 + math.exp( -delta ) );

def sgd ( userId , item , iboard , jtem , jboard , oneRecord ):
    #print ( item , iboard , jtem , jboard , oneRecord )
    delta = calculatePuti ( item , iboard )  - calculatePuti ( jtem , jboard )
    delta = 1 - logistic( delta )

    parameter[ "Witem" ][ item ] += learn_rate*( delta - Lambda*parameter[ "Witem" ][ item ] );
    parameter[ "Witem" ][ jtem ] += learn_rate*( -delta - Lambda*parameter [ "Witem" ][ jtem ] );

    parameter [ "Wboard" ][ iboard ] += learn_rate*( delta - Lambda*parameter[ "Wboard" ][ iboard ] );
    parameter [ "Wboard" ][ jboard ] += learn_rate*( -delta - Lambda*parameter [ "Wboard" ][ jboard ] ) ;

    for f in range ( K ):
        parameter [ "Vitem" ][ f ][ item ] += learn_rate*( delta*( eta [ f ] + parameter [ "Vboard" ][ f ][ iboard ] )  - Lambda*parameter [ "Vitem" ][ f ][ item ] )
        parameter [ "Vitem" ][ f ][ jtem ] += learn_rate*( -delta*( eta [ f ] + parameter [ "Vboard" ][ f ][ jboard ] ) - Lambda*parameter [ "Vitem" ][ f ][ jtem ] )
        parameter [ "Vboard" ][ f ][ iboard ] += learn_rate*( delta*( eta [ f ] + parameter [ "Vitem" ][ f ][ item ] ) - Lambda*parameter [ "Vboard" ][ f ][ iboard ] )
        parameter [ "Vboard" ][ f ][ jboard ] += learn_rate*( -delta*( eta [ f ] + parameter [ "Vitem" ][ f ][ jtem ] ) - Lambda* parameter [ "Vboard" ][ f ][ jboard ] )
        beta = ( parameter [ "Vitem" ][ f ][ item ] + parameter [ "Vboard" ][ f ][ iboard ] - parameter [ "Vitem" ][ f ][ jtem ] - parameter [ "Vboard" ][ f ][ jboard ] )* delta
        parameter [ "Vuser" ][ f ][ userId ] += learn_rate *( beta - Lambda*parameter [ "Vuser" ][ f ][ userId ] )
        for theType in range ( 3 ):
            for board in oneRecord [ theType ][ "boards" ]:
                parameter [ theType ][ "Vboard" ][ f ][ board ] += learn_rate*( beta* oneRecord [ theType ][ "boards" ][ board ] - Lambda* parameter [ theType ][ "Vboard" ][ f ][ board ] )
            for item in oneRecord [ theType ][ "items" ]:
                parameter [ theType ][ "Vitem" ][ f ][ item ] += learn_rate*( beta*oneRecord [ theType ][ "items" ][ item ] - Lambda*parameter [ theType ][ "Vitem" ][ f ][ item ] )

def trainParameter():
    boardListLen = len ( boardList ) -1
    itemListLen = len ( itemList ) - 1
    for iterTime in range ( iterations ):
        for userId in trainDict:
            nowNum = 0
            for oneRecord in trainDict [ userId ]:
                calculateEta ( userId , oneRecord )
                items = oneRecord [ "items" ]
                board = oneRecord [ "boardId" ]
                for item in items:
                    for oneTime in range ( times ):
                        while True:
                            j = random.randint( 0  , itemListLen  )
                            if not ( itemList [ j ] in items ):
                                break
                        jtem = itemList [ j ]
                        sgd ( userId ,  item , board , jtem , board , oneRecord )
                for oneTime in range ( times/4 ):
                    while True:
                        j = random.randint ( 0 , boardListLen )
                        if not ( board == boardList [ j ] ):
                            break
                    jboard = boardList [ j ]
                    for item in items:
                        sgd ( userId , item , board , jtem , jboard , oneRecord )
                print ( "One Record " + str ( nowNum ) + " finish" )
                nowNum +=1
            print ( "One UserId " + str ( userId ) + " finish" )
        print ( "The iteration " + str ( iterTime ) + " finish" )
if __name__ == "__main__":
    random.seed()
    if len ( sys.argv ) < 2:
        print "No programPath"
        sys.exit(1)
    opts , args = getopt.getopt ( sys.argv[ 2: ] , "k:s:l:i:t:r:" , [ "K" , "sigma" , "lambda" , "iterations" , "times" , "learn_rate" ] )
    initializeArgv ( opts )
    programPath = sys.argv [ 1 ]
    articleFilename = os.path.join ( programPath , "data/articleDict.pickle" )
    trainFilename = os.path.join ( programPath , "data/recordTrain.pickle" )

    articleDict = load_pickle ( articleFilename )
    trainDict = load_pickle ( trainFilename )

    initialList (  )
    itemListFilename = os.path.join ( programPath , "data/itemList.pickle" )
    store_pickle ( itemListFilename , itemList )
    boardListFilename = os.path.join ( programPath , "data/boardList.pickle" )
    store_pickle ( boardListFilename , boardList )
    userIdListFilename = os.path.join ( programPath , "data/userIdList.pickle" )
    store_pickle ( userIdListFilename , userIdList )

    initialAllParameter()

    trainParameter ( )
    parameterFilename = os.path.join ( programPath , "data/parameter.pickle" )
    store_pickle (parameterFilename,parameter )
    print ( parameter )
