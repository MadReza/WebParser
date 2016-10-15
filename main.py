print "Start of Script"

from utilities import getFilePathsMatching
from utilities import removeStopWords

##Retrieve the file Names and location from current location
fileNames = getFilePathsMatching("reut/*.sgm")

##---------------------------
import time
import sys
sys.path.append('beautifulsoup4-4.5.1')
from bs4 import BeautifulSoup
#from stemming.porter2 import stem

##Empty Dict to store
title = {}
date = {}
body = {}
t = time.clock()

for file in fileNames:
	f = open(file, "r")
        xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
        for xmlText in xmlTextList:
                key = xmlText.get('newid')
                if xmlText.title:
                        for word in removeStopWords(xmlText.title.text):
                                stemmed = word   #removed stem(word)
                                if stemmed in title:
                                        if key in title[stemmed]:
                                                title[stemmed][key] += 1
                                        else:
                                                title[stemmed][key] = 1
                                else:
                                        title[stemmed] = {}
                                        title[stemmed][key] = 1
                if xmlText.date:
                        d = xmlText.date.text.lower()
                        if d in date:
                                if key in date[d]:
                                        date[d][key] += 1
                                else:
                                        date[d][key] = 1
                        else:
                                date[d] = {}
                                date[d][key] = 1
                if xmlText.body:
                        for word in removeStopWords(xmlText.body.text):
                                stemmed = word  #removed stem(word)
                                if stemmed in body:
                                        if key in body[stemmed]:
                                                body[stemmed][key] += 1
                                        else:
                                                body[stemmed][key] = 1
                                else:
                                        body[stemmed] = {}
                                        body[stemmed][key] = 1
        #break

print `time.clock() - t`

import json
with open('all_title.json', 'w') as file_name:
        json.dump(title, file_name, sort_keys=True, indent=4)
with open('all_body.json', 'w') as file_name:
        json.dump(body, file_name, sort_keys=True, indent=4)
with open('all_title.json', 'w') as file_name:
        json.dump(title, file_name, sort_keys=True, indent=4)

"""
for key, value in title.items():
        for k, v in value.items():
                print `key` + ": " + `k` + " @ " + `v`  
"""

                        
