###~~File Retriver~~###
from glob import glob
def getFilePathsMatching(path):
    return glob(path);


###~~Cleaning~~###
import string
from nltk.corpus import stopwords
from nltk import word_tokenize

cached_junk = list(string.punctuation) + stopwords.words("english")

def removeStopWords(text):    
    return (i for i in word_tokenize(text.lower()) if i not in cached_junk)

