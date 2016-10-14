
###~~File Retriver~~###
from glob import glob
def getFilePathsMatching(path):
    return glob(path);

###~~Cleaning~~###
import string
from nltk.corpus import stopwords
cachedStopWords = stopwords.words("english")
cachedPunctuation = list(string.punctuation)

def removeStopWords(str):
    str = str.lower()
    #str = ''.join((char for char in word + " " if char not in cachedPunctuation) for word in str.split() if word not in cachedStopWords)
    str = ''.join(char for char in str if char not in cachedPunctuation)
    str = ''.join([word + " " for word in str.split() if word not in cachedStopWords])
    return str
