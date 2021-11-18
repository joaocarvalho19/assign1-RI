import ast
import os
import re
from typing import cast

import psutil

class Indexer:
    def __init__(self):
        self.indexed_tokens = {}
        self.vocabulary_size = 0
        self.index_size = 0
        self.index_num = 1

    def run(self, tokens):
        for token, _id in tokens:
            if token not in self.indexed_tokens.keys():
                temp_dict = dict()            
                temp_dict[_id] = tokens.count((token, _id))
                self.indexed_tokens[token] = temp_dict
            else:
                self.indexed_tokens[token][_id] = tokens.count((token, _id))
                #if _id not in self.indexed_tokens[token].keys():
                #    self.indexed_tokens[token][_id] = tokens.count((token, _id))
                #else:
                #    self.indexed_tokens[token][_id] = tokens.count((token, _id))
    
    def clearIndex(self):
        self.indexed_tokens = {}
    
    def getIndexedTokens(self):
        return self.indexed_tokens
    
    def getVocabularySize(self):
        return self.vocabulary_size

    def getIndexSize(self):
        return self.index_size

    def write_block(self, number):
        print("Writing block...")
        sorted_index = dict(sorted(self.indexed_tokens.items()))
        with open("output/output_" + str(number) + ".txt",'w') as f:
            for token, value in sorted_index.items():
                string = token + ' : ' + str(value) + '\n'
                f.write(string)
        
        self.indexed_tokens = {}

    
    def merge_blocks(self):
        print("Merging...")
        temp_index = {}
        output_files = os.listdir("output")
        output_files = [open("output/"+block_file) for block_file in output_files]
        print(output_files)
        lines = [(block_file.readline()[:-1], i) for i, block_file in enumerate(output_files)]
        initial_mem = psutil.virtual_memory().available
        while lines:
            for line, i in lines:                
                line = line.split(" : ")
                term = line[0]
                postings = line[1]
                postings_list = [str(s) for s in postings.replace('[', '').replace(']', '').replace("'", '').split(',')]

                used_mem = initial_mem - psutil.virtual_memory().available                
                # changed to use 300mb insted of just 3mb
                if used_mem > 3000000000:
                    print("Writing part of index...")
                    self.write_index(temp_index)
                    temp_index = {}
                    self.index_num+=1
                    initial_mem = psutil.virtual_memory().available
        
                if term in temp_index.keys():
                    temp_index[term] = list(set(temp_index[term] + postings_list))

                else:
                    temp_index[term] = postings_list

            lines = [(block_file.readline()[:-1], i) for i, block_file in enumerate(output_files)]

            for line, i in lines:
                if not line:
                    output_files.pop(i)
                    lines.pop(i)

        print("Writing part of index...")
        self.write_index(temp_index)
        temp_index = {}
        self.index_num+=1


    def write_index(self, temp_index):
        ordered_dict = dict(sorted(temp_index.items()))
        with open("index_"+str(self.index_num)+".txt",'w+') as f:
            for term, value in ordered_dict.items():
                string = term + ' : ' + str(value) + '\n'
                f.write(string)
        
        self.index_size += os.path.getsize('./index_' + str(self.index_num) + '.txt')
        self.vocabulary_size += len(ordered_dict)
        f.close()