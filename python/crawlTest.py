import requests
import sys
import urllib
import urllib2
URL = 'http://www.cc98.org/login.asp'
URL2 ='http://www.cc98.org/dispbbs.asp?boardID=422&ID=4060965&page='
def main():
    data = urllib.urlencode ( {'usename' : 'luyifan'
            ,'password':'luyifan1993'
            ,'conntinue':URL2,
            'submit':u'\xe7\x99\xbb \xe5\xbd\x95'.encode('utf-8'),
            'userhidden' : '2' })
    opener = urllib2.build_opener ( urllib2.HTTPHandler )
    print ( opener.open ( URL , data ).read ( ))

if __name__ == '__main__':

    main()
