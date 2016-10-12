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
from stemming.porter2 import stem
##Empty Dict to store

d = {}
title = {}
body = {}
for file in fileNames:
	f = open(file, "r")
        xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
        for xmlText in xmlTextList:
                key = xmlText.get('newid')
                d[key] = {}
                if xmlText.title:
#                        print key + ": " + xmlText.title.text
                        d[key]['title'] = removeStopWords(xmlText.title.text)
#                        print d[key]['title']
#                        print d[key]['title'].split()
                        for word in d[key]['title'].split():
                                stemmed = stem(word)
                                title[stemmed] = {}
								if key in title[stemmed]:	#more efficient.
                                #if title[stemmed].has_key(key):
                                        title[stemmed][key] = title[stemmed][key] + 1
                                else:
                                        title[stemmed][key] = 1
                if xmlText.date:
                        d[key]['date'] = xmlText.date.text.lower()
                if xmlText.body:
                        d[key]['body'] = removeStopWords(xmlText.body.text)
                        for word in d[key]['body'].split():
                                stemmed = stem(word)
                                body[stemmed] = {}
                                if body[stemmed].has_key(key):
                                        body[stemmed][key] = body[stemmed][key] + 1
                                else:
                                        body[stemmed][key] = 1


for key, value in title.items():
        for k, v in value.items():
                print key + ": " + k + "@"  


                        
