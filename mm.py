from utilities import getFilePathsMatching
from utilities import removeStopWords
from helper import get_cmd_args
from rank import BM25
##Retrieve the file Names and location from current location
fileNames = getFilePathsMatching("reut/*.sgm")

##---------------------------
import time
import os
import sys
import operator
sys.path.append('beautifulsoup4-4.5.1')
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

##Empty Dict to store
t = time.clock()

def spimi_invert(token_stream, file_name):
        with open(file_name, "w") as output_file:
                dictionary = {}
                for term, doc_id in token_stream:
                        if term not in dictionary:
                                postings_list = add_to_dictionary(dictionary, term)
                        else:
                                postings_list = get_postings_list(dictionary, term)
                        #if full(postings_list):
                        #        postings_list = double_postings_list(dictionary, term)
                        add_to_postings_list(postings_list, doc_id)
                sorted_terms = sort_terms(dictionary)
                write_block_to_disk(sorted_terms, output_file)
        output_file.close()
        return output_file

def save_doc_info(info, file_name):
        with open(file_name, "w") as output_file:
                write_block_to_disk(info, output_file)
        output_file.close()

def add_to_dictionary(dictionary,term):
        dictionary[term] = {}
        return dictionary[term]

def get_postings_list(dictionary,term):
        return dictionary[term]                

def add_to_postings_list(postings_list,docid):
        if docid in postings_list:
                postings_list[docid] = postings_list[docid] + 1
        else:
                postings_list[docid] = 1
        #postings_list.insert(0,docid) if docid not in postings_list else postings_list

def sort_terms(dictionary):
        return OrderedDict(sorted(dictionary.items()))

def write_block_to_disk(obj, output_file):
        json.dump(obj, output_file, sort_keys=True, indent=4)

def read_from_disk(file_name):
        with open(file_name,'r') as input_file:
                obj = json.load(input_file)
        input_file.close()
        return obj

def merge_dicts(x, y):
        '''Given two dicts, merge them into a new dict as a shallow copy.'''
        z = x.copy()
        z.update(y)
        return z

def merge_files(file_names, final_file_name):
        d = {}
        for file in file_names:
                d = merge_dicts(d, read_from_disk(file))

        #combine to file
        with open(final_file_name, "w") as output_file:
                write_block_to_disk(d, output_file)

        return d

def delete_files(file_names):
        for file in file_names:
                os.remove(file)

def get_all_term_id_from(file_names):
        d = []
        docs = {} #Word count in each doc
        for file in file_names:
                f = open(file, "r").read()
                for xmlText in BeautifulSoup(f, "html.parser").findAll("reuters"):
                        term_id = int(xmlText.get('newid'))
                        docs[term_id] = 0
                        if xmlText.title:
                                for word in removeStopWords(xmlText.title.text):
                                #for word in xmlText.title.text.split():
                                        d += [(word, term_id)]
                                        docs[term_id] = docs[term_id] + 1
                        if xmlText.body:
                                for word in removeStopWords(xmlText.body.text):
                                #for word in xmlText.body.text.split():
                                        d += [(word, term_id)]
                                        docs[term_id] = docs[term_id] + 1
        return d, docs

def spimi_block_caller(block):
        block_id = 0
        files_created = []
        while len(block) != 0:
                if args.block_size == 0:
                        stream = [block.pop() for x in xrange(len(block))]
                else:
                        try: stream = [block.pop() for x in xrange(args.block_size)]
                        except IndexError as ie: pass

                file_name = "./Temp/Block" + `block_id`
                spimi_invert(stream, file_name)
                files_created.append(file_name)
                block_id += 1
        return files_created

def get_most_matching_terms(d):
        return max((len(v), k) for k,v in d.iteritems())

def search(s):
        i = read_from_disk("indexed_file")
        doc = read_from_disk("indexed_docs")
        search_terms = removeStopWords(s)

        bm25_ranking = BM25(i, doc)
        
        doc_scores = bm25_ranking.get_scores(search_terms)
        sorted_scores = sorted(doc_scores.items(), key=operator.itemgetter(1))

        print "Found: " + `len(sorted_scores)` +  " documents with the specified search:"
        while sorted_scores:
                k,v = sorted_scores.pop()
                print k
                print v
                print "Document: " + str(k) + " scored: " + str(v) + " contains:"
                #TODO add words in relevant documents
                #print "Terms: " + str(v)
        return None

def deprecated_search(s):
        """keeping for history relevance"""
        i = read_from_disk("indexed_file")
        search_terms = removeStopWords(s)
        found = {}
        for term in [t for t in search_terms if t in i]:
                for doc_id in i[term]:
                        if not found.has_key(doc_id):
                                found[doc_id] = []
                        found[doc_id].append(term)

        print "Found: " + `len(found)` +  " documents with the specified search:"
        while found:
                k = get_most_matching_terms(found)[1]
                v = found.pop(k)
                print "Document: " + str(k) + " contains:"
                print "Terms: " + str(v)
        return None

if __name__ == '__main__':
        args = get_cmd_args()

        if args.search_term:
                print "Searching...."
                search(args.search_term)
        else:
                block, docs = get_all_term_id_from(fileNames)
                save_doc_info(docs, "indexed_docs")
                raw_input()
                files_to_merge = spimi_block_caller(block)
                merge_files(files_to_merge, "indexed_file")
                delete_files(files_to_merge)
print `time.clock() - t`

                        
