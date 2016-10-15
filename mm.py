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
from stemming.porter2 import stem
import json

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
        return sorted(dictionary,key = lambda tup: tup[0],reverse=True)

def read_from_disk(file_name):
        with open(source,'rb') as input_file:
                obj = load(input_file)
        input_file.close()
        return obj

if __name__ == '__main__':
        args = get_cmd_args()
        for file in fileNames:
                f = open(file, "r")
                xmlTextList = BeautifulSoup(f, "html.parser").findAll("reuters")
                for xmlText in xmlTextList:
                        key = xmlText.get('newid')
                        block = []
                        if xmlText.title:
                                for word in removeStopWords(xmlText.title.text):
                                        block += [(word, key)]
                        if xmlText.body:
                                for word in removeStopWords(xmlText.body.text):
                                        block += [(word, key)]
                        break
        block_id = 0
        while len(block) != 0:
                if args.block_size == 0:
                        stream = block
                else:
                        try: stream = [block.pop() for x in xrange(args.block_size)]
                        except IndexError as ie: pass

                file_name = "Block" + `block_id`
                spimi_invert(stream, file_name)
                block_id += 1

print `time.clock() - t`

                        
