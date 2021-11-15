import argparse
from parser import Parser
from tokenizer import Tokenizer
from indexer import Indexer
from sys import argv
import csv
import nltk
from nltk.corpus import stopwords
import time
import os
#import psutil

class SPIMI:
    def __init__(self, dataset, min_length, stopwords):
        self.dataset = dataset
        self.tokenizer = Tokenizer(min_length,stopwords)
        self.indexer = Indexer()


    def run(self):
        # Main function

        limit = 50000
        count = 0
        begin = time.time()
        with open(self.dataset, 'r') as fd:
            rd = csv.reader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
            tokens = []
            for row in rd:
                #memory = psutil.virtual_memory().available
                #print(memory)
                        
                # Block
                if count <= limit:   
                    #if row[2] != 'review_id':
                    review_id, review_headline, review_body = row[2], row[12], row[13]
                    #string = review_headline + " " + review_body
                    tokens.extend(self.tokenizer.get_tokens(review_headline + " " + review_body, review_id))
                    count+=1
                    #print(count)
                else:
                    # reaching limit - write block on disk
                    print('time: ', round((time.time()-begin)/60,2))
                    self.indexer.run(tokens)
                    
                    # clear memory
                    tokens = []

                    post_list = self.indexer.merge_blocks()
                        
                    self.indexer.write_block(post_list)
                    count=0
                    #break
                    print('finished: ', round((time.time()-begin)/60, 2))

        # if it finishes reading the file before reaching the row limit
        if tokens != []:
            self.indexer.run(tokens)
            tokens = []
            post_list = self.indexer.merge_blocks()
            self.indexer.write_block(post_list)
            print('finished: ', round((time.time()-begin)/60, 2))
            
        end = time.time()

        print("Total indexing time (min): ", round((end-begin)/60, 2))
        print("Total index size on disk (bytes): ", os.path.getsize('./output.txt'))
        print("Vocabulary size: ", self.indexer.getVocabularySize())
        print("Number of temporary index segments written to disk: ", self.indexer.getNumTS())

        print("Finish!!")
        #fd.close()

if __name__ == "__main__":
    default_stopwords = stopwords.words('english')
    # Command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("dataset", help="Dataset")
    cli_parser.add_argument("-m", "--minimum", type=int, default=3, help="Minimum token length. Default 2 characets. Enter 0 to deactivate.")
    cli_parser.add_argument("-s", "--stopwords", default=default_stopwords, help="Stopword list. Enter 'D' to deactivate")
    args = cli_parser.parse_args()
    
    data = args.dataset
    if args.minimum == 0:
        min_len = None
    else:
        min_len = args.minimum
    
    # TODO: check what we want as an argument and fix the this snippet
    if args.stopwords == ['D']:
        stopwords = None
    else:
        stopwords = args.stopwords
    
    spimi = SPIMI(data, min_len,stopwords)
    spimi.run()