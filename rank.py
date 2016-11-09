from math import log
from utilities import removeStopWords

class BM25:
    """Formula from: https://en.wikipedia.org/wiki/Okapi_BM25"""

    def __init__(self, inverted_index, doc_info):
        self.ii = inverted_index
        self.doc_info = doc_info
        #free parameters
        self.k1 = 1.2 #possibility: 1.2 or 2.0
        self.b = 0.75

    def get_score(search, term_frequency_in_doc, doc_total_words, doc_average_length):
        """returns the score by using the BM25 formula."""

        search_terms = removeStopWords(s)
        scores = {}
        avg_dl = __average_doc_length_in_collection()
        
        for doc_id in self.doc_info.iterkeys():
            score = 0
            doc_length = self.doc_info[doc_id]
            for term in search_terms:
                idf = __IDF(term)
                fqi = __term_frequency_in_doc(term, doc_id)
                top = fqi * (k1 + 1)
                bot = fqi + k1 * (1 -b + b * doc_length / avg_dl)
                s = idf * (top / bot)
                score = score + s
            scores[doc_id] = score
        return scores
                

    def __average_doc_length_in_collection(self):
        total_docs = len(self.doc_info)
        total_words = 0
        for doc_id in self.doc_info.iterkeys():
            total_words = total_words + self.doc_info[doc_id]
        return total_words / total_docs
                    
    def __term_frequency_in_doc(self, term, doc_id):
        if doc_id in self.ii[term]:
            return self.ii[term][doc_id]
        else:
            return 0
            

    def __IDF(self, term):
        """Private helper function for getting the IDF for the score"""
        N = len(self.doc_info) #total document count
        nq = len(self.ii[term]) #total documents containing term
        top = N - nq + 0.5
        bot = nq + 0.5
        return log(top/bot)
        
