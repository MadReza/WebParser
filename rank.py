from math import log10
from utilities import removeStopWords

class BM25:
    """Formula from: https://en.wikipedia.org/wiki/Okapi_BM25"""

    def __init__(self, inverted_index, doc_info):
        self.ii = inverted_index
        self.doc_info = doc_info
        #free parameters
        self.k1 = 1.2 #possibility: 1.2 or 2.0
        self.b = 0.75

    def get_scores(self, search_terms):
        """returns the score by using the BM25 formula."""
        
        scores = {}
        avg_dl = self.__average_doc_length_in_collection()
        
        for doc_id in self.doc_info.iterkeys():
            score = 0
            doc_length = self.doc_info[doc_id]
            for term in [t for t in search_terms if t in self.ii]:
                idf = self.__IDF(term)
                fqi = self.__term_frequency_in_doc(term, doc_id)
                top = fqi * (self.k1 + 1)
                bot = fqi + self.k1 * (1 - self.b + self.b * doc_length / avg_dl)
                s = idf * (top / bot)
                score = score + s
            scores[doc_id] = score
        return self.__remove_useless(scores)

    def __remove_useless(self, scores):
        """remove all documents with 0 scores"""
        filtered_scores = {}
        for doc_id, score in scores.iteritems():
            if score > 0:
                filtered_scores[doc_id] = score
        return filtered_scores

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

    def __total_docs_contain_term(self, term):
        if term in self.ii:
            return len(self.ii[term])
        else:
            return 0

    def __IDF(self, term):
        """Private helper function for getting the IDF for the score"""
        N = len(self.doc_info) #total document count
        nq = self.__total_docs_contain_term(term)
        top = N - nq + 0.5
        bot = nq + 0.5
        return log10(top/bot)
        
