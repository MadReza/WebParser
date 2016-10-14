
###~~File Retriver~~###
from glob import glob
def getFilePathsMatching(path):
    return glob(path);

###~~Cleaning~~###
import string
from nltk.corpus import stopwords
from nltk import word_tokenize

cached_junk = list(string.punctuation) + stopwords.words("english")
#cachedStopWords = stopwords.words("english")
#cachedPunctuation = list(string.punctuation)

def removeStopWords(text):
    return [i for i in word_tokenize(text.lower()) if i not in cachedJunk]


    #str = str.lower()
    #str = ''.join((char for char in word + " " if char not in cachedPunctuation) for word in str.split() if word not in cachedStopWords)
    #str = ''.join(char for char in str if char not in cachedPunctuation)
    #str = ''.join([word + " " for word in str.split() if word not in cachedStopWords])
    return str
