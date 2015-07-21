import feedparser
import os.path
import sys, getopt
import time
import socket
from urllib2 import urlopen
from urllib2 import URLError, HTTPError
from datetime import datetime
from datetime import timedelta
import re
import ftplib

mainDir = '/edgar/daily-index/'
localDir = '/Users/macbookair/8K/'
formtype = ['8-K']
#formtype = ['D/A']

now = datetime.now()
yesterday = datetime.now() - timedelta(hours=24)
datestr = yesterday.strftime('%Y%m%d')
#date = datetime.datetime.strptime(line[1],'%m/%d/%Y %I:%M:%S %p')
#Read Index file
ftp = 'ftp://ftp.sec.gov/'
edgarIndex = ftp + 'edgar/daily-index/form.' + datestr + '.idx'
indexFile = urlopen( edgarIndex )
indexData = indexFile.readlines()

#match_start = re.search('<edgarSubmission>', lines)
#i = match_start.start()
#print indexData[1:20]
idrow = []

for line in indexData:
    if line[:3].strip() in formtype:
#        print line
#        field = re.split(r'\t+', line)
        field = re.split(r"\s{2,}", line)
        idrow.append(field)

print idrow
#Index 0 = Form type
#Index 1 = Company name
#Index 2 = CIK
#Index 3 = Filing Date
#Index 4 = Edgar link
ftpdownload = ftplib.FTP('ftp.sec.gov','anonymous','none@none.com')

for filing in idrow:
    link = filing[4].split('/')
    curr_dir = '/' + link[0] + '/' + link[1] + '/' + link[2] + '/'
    filename = link[3]
    ftpdownload.cwd(curr_dir)
    local_path = localDir + filename
    print "Retrieving", curr_dir 
    ftpdownload.retrbinary('RETR '+ filename, open(local_path, 'wb').write)

