print "Start of Script"

fileNames = ""

##Retrieve the file Names and location from current location
from glob import glob
fileNames = glob("reut/*.sgm")

##---------------------------

import sys
import string
sys.path.append('beautifulsoup4-4.5.1')
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

#cache

cachedStopWords = stopwords.words("english")
cachedPunctuation = list(string.punctuation)

##Empty Dict to store

d = {}

for file in fileNames:
	f = open(file, "r")
        xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
        for xmlText in xmlTextList:
                key = xmlText.get('newid')
                d[key] = {}                
                if xmlText.title:
                        t = xmlText.title.text.lower()
                        t = ''.join(ch for ch in t if ch not in cachedPunctuation)
                        d[key]['title'] = ' '.join([word for word in t.split() if word not in cachedStopWords])
                if xmlText.date:
                        d[key]['date'] = xmlText.date.text.lower()
                if xmlText.body:
                        t = xmlText.body.text.lower()
                        t = ''.join(ch for ch in t if ch not in cachedPunctuation)
                        d[key]['body'] = ' '.join([word for word in t.split() if word not in cachedStopWords])


for key, value in d.items():
        for k, v in value.items():
                if k == 'title':
                        print key + ": " + v
                        
