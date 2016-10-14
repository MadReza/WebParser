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
                print key
                d[key] = {}
                if xmlText.title:
                        d[key]['title'] = removeStopWords(xmlText.title.text)
                        for word in d[key]['title'].split():
                                stemmed = stem(word)
                                if stemmed in title:
                                        if key in title[stemmed]:
                                                title[stemmed][key] += 1
                                        else:
                                                title[stemmed][key] = 1
                                else:
                                        title[stemmed] = {}
                                        title[stemmed][key] = 1
                if xmlText.date:
                        d[key]['date'] = xmlText.date.text.lower()
                        ###TODO: There is some junk in few dates need cleaning.
                if xmlText.body:
                        d[key]['body'] = removeStopWords(xmlText.body.text)
                        for word in d[key]['body'].split():
                                stemmed = stem(word)
                                if stemmed in body:
                                        if key in body[stemmed]:
                                                body[stemmed][key] += 1
                                        else:
                                                body[stemmed][key] = 1
                                else:
                                        body[stemmed] = {}
                                        body[stemmed][key] = 1


import json
with open('all_title.json', 'w') as file_name:
        json.dump(title, file_name, sort_keys=True, indent=4)
with open('all_body.json', 'w') as file_name:
        json.dump(body, file_name, sort_keys=True, indent=4)
with open('test.json', 'w') as file_name:
        json.dump(body, file_name, sort_keys=True, indent=4)


for key, value in title.items():
        for k, v in value.items():
                print key + ": " + k + " @ " + v  


                        
