###~~File Retriver~~###
from glob import glob
def getFilePathsMatching(path):
    return glob(path);


###~~Cleaning~~###
import string
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
#from nltk import wordpunct_tokenize, Text

cachedStopWords = stopwords.words("english")
cachedPunctuation = list(string.punctuation)


def removeStopWords(text):
    text = text.lower().encode('utf8', 'ignore')
    text = word_tokenize(text)
    text = [re.sub(r'\b\d+\.?\d*\b', '', token) for token in text] #removing numbers
    text = [token for token in text if token not in cachedPunctuation]
    text = ''.join([word + " " for word in text if word not in cachedStopWords])
    return text.split()
#    text = wordpunct_tokenize(text)
#    text = Text(text)
#    return (a for a in text if a not in cachedPunctuation)

