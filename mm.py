from utilities import getFilePathsMatching
from utilities import removeStopWords
from helper import get_cmd_args
##Retrieve the file Names and location from current location
fileNames = getFilePathsMatching("reut/*.sgm")

##---------------------------
import time
import sys
sys.path.append('beautifulsoup4-4.5.1')
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

##Empty Dict to store
title = {}
date = {}
body = {}
t = time.clock()

def spimi_invert(token_stream, file_name):
        def write_block_to_disk(obj, output_file):
                json.dump(obj, output_file, sort_keys=True, indent=4)
        
        with open(file_name, "wb") as output_file:
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

def add_to_dictionary(dictionary,term):
        dictionary[term] = []
        return dictionary[term]

def get_postings_list(dictionary,term):
        return dictionary[term]                

def add_to_postings_list(postings_list,docid):
        postings_list.insert(0,docid) if docid not in postings_list else postings_list

def sort_terms(dictionary):
        return OrderedDict(sorted(dictionary.items()))

def read_from_disk(file_name):
        with open(source,'rb') as input_file:
                obj = load(input_file)
        input_file.close()
        return obj

def merge(file_names):
        

def get_all_term_id_from(file_names):
        d = []
        for file in file_names:
                f = open(file, "r")
                xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
                for xmlText in xmlTextList:
                        term_id = xmlText.get('newid')
                        if xmlText.title:
                                for word in removeStopWords(xmlText.title.text):
                                        d += [(word, term_id)]
                        if xmlText.body:
                                for word in removeStopWords(xmlText.body.text):
                                        d += [(word, term_id)]
        return d

if __name__ == '__main__':
        args = get_cmd_args()
        block = get_all_term_id_from(fileNames)
        block_id = 0
        files_to_merge = []
        while len(block) != 0:
                if args.block_size == 0:
                        stream = [block.pop() for x in xrange(len(block))]
                else:
                        try: stream = [block.pop() for x in xrange(args.block_size)]
                        except IndexError as ie: pass

                file_name = "Block" + `block_id`
                spimi_invert(stream, file_name)
                files_to_merge.append(file_name)
                block_id += 1

print `time.clock() - t`

                        
