print "Start of Script"

from utilities import getFilePathsMatching
from utilities import removeStopWords

fileNames = ""

##Retrieve the file Names and location from current location
fileNames = getFilePathsMatching("reut/*.sgm")

##---------------------------

import sys
sys.path.append('beautifulsoup4-4.5.1')
from bs4 import BeautifulSoup

##Empty Dict to store

d = {}

for file in fileNames:
	f = open(file, "r")
        xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
        for xmlText in xmlTextList:
                key = xmlText.get('newid')
                d[key] = {}                
                if xmlText.title:
                        d[key]['title'] = removeStopWords(xmlText.title.text)
                if xmlText.date:
                        d[key]['date'] = xmlText.date.text.lower()
                if xmlText.body:
                        d[key]['body'] = removeStopWords(xmlText.body.text)


for key, value in d.items():
        for k, v in value.items():
                if k == 'title':
                        print key + ": " + v
                        
