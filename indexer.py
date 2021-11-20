import ast
import os
import re
import fnmatch
import psutil
from typing import cast


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
    
    def get_final_index(self):
        return self.final_index
    
    def clear_index(self):
        self.indexed_tokens = {}
    
    def get_indexed_tokens(self):
        return self.indexed_tokens
    
    def get_vocabulary_size(self):
        return self.vocabulary_size

    def get_index_size(self):
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
        output_files = [open("output/"+block_file,'r') for block_file in output_files if block_file != '.DS_Store']
        lines = [(block_file.readline()[:-1], i) for i, block_file in enumerate(output_files)]
        initial_mem = psutil.virtual_memory().available

        while lines:
            for line, i in lines:

                line = line.split(" : ")
                if len(line) > 1:
                    term = line[0]
                    postings_dict = ast.literal_eval(line[1])

                    used_mem = initial_mem - psutil.virtual_memory().available                
                    # changed to use 300mb insted of just 3mb
                    if used_mem > 300000000:
                        print("Writing part of index...")
                        self.write_index(temp_index)
                        temp_index = {}
                        self.index_num+=1
                        initial_mem = psutil.virtual_memory().available

                    # Update index
                    if term in temp_index.keys():
                        for _id in postings_dict.keys():
                            if _id in temp_index[term]:
                                temp_index[term][_id] += postings_dict[_id]
                            else:
                                temp_index[term][_id] = postings_dict[_id]

                    else:
                        temp_index[term] = postings_dict

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
        with open("index/index_"+str(self.index_num)+".txt",'w') as f:
            for term, value in ordered_dict.items():
                string = term + ' : ' + str(value) + '\n'
                f.write(string)
        
        self.index_size += os.path.getsize('./index/index_' + str(self.index_num) + '.txt')
        self.vocabulary_size += len(ordered_dict)
        f.close()
        
    def merge_indexes(self):
        final_index = {}
        indexes = fnmatch.filter(os.listdir('index'), 'index_*.txt')
        #print(indexes)
        if len(indexes) == 1:
            os.rename(indexes[0],'final_index.txt')
        else:
            indexes = [open("index/"+idx_file, 'r') for idx_file in indexes]
            lines = [(idx_file.readline()[:-1], i) for i, idx_file in enumerate(indexes)]
            while lines:
                pass
    
    def load_index(self):
        self.final_index = {}
        with open('final_index.txt','r') as f:
            for line in f:
                row = line.split(' : ')
                key = row[0]
                val = row[1]
                val.strip('\n')
                self.final_index[key] = val
        