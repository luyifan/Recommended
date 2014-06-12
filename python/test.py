import os
import sys
import pickle
import urllib2
import requests
import re
from DealWithArticle import store_pickle
reload ( sys )
sys.setdefaultencoding ( "utf-8" )
if __name__ == "__main__":
    #cc98login ( "http://www.cc98.org/login.asp" )
    programPath  = sys.argv [ 1 ]
    filename = os.path.join ( programPath , "data/postAbsence.txt" )
    f = open ( filename , "r" )
    i = 0
    for line in f:
        i+=1
        lineList = line.split(" ")
        if ( lineList [ 1 ].find ( "NULL" ) != -1 ):
            continue
    print i
