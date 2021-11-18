import argparse
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
    def __init__(self, dataset, min_length, stopwords, limit=10000):
        self.dataset = dataset
        self.tokenizer = Tokenizer(min_length,stopwords)
        self.indexer = Indexer()
        self.chunk_limit = limit
        self.block_num = 1


    def run(self):
        # Main function
        self.indexer.merge_blocks()
        
        count = 0
        begin = time.time()
        with open(self.dataset,'r') as fd:
            rd = csv.DictReader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
            tokens = []
            print("Indexing...")
            for row in rd:                
                # Block
                if count < self.chunk_limit:   
                    #if row[2] != 'review_id':
                    #review_id, product_title, review_headline, review_body = row[2], row[5], row[12], row[13]
                    #string = product_title + " " + review_headline + " " + review_body
                    #tokens += self.tokenizer.get_tokens(string, review_id)
                    review_id, review_headline, review_body = row['review_id'], row['review_headline'], row['review_body']
                    string = review_headline + " " + review_body
                    
                    tokens = self.tokenizer.get_tokens(string, review_id)
                    
                    self.indexer.run(tokens)
                    self.indexer.getIndexedTokens()
                    count+=1
                    
                else:
                    # reaching limit - write block on disk
                    # clear memory
                    tokens = []
                    self.indexer.write_block(self.block_num)
                    self.block_num += 1
                    
                    # clear memory
                    self.indexer.clearIndex()
                    count=0
                    #break

        if tokens != []:
            self.indexer.run(tokens)
            self.indexer.write_block(self.block_num)

        print("Total indexing time before merging (min): ", round((time.time()-begin)/60, 2))
        # clear memory
        self.indexer.clearIndex()
        
        # Merge blocks    
        self.indexer.merge_blocks()
        end = time.time()

        print("Total indexing time (min): ", round((end-begin)/60, 2))
        print("Total index size on disk: ", self.indexer.getIndexSize())
        print("Vocabulary size: ", self.indexer.getVocabularySize())
        print("Number of temporary index segments written to disk: ", self.block_num)
        print("Finish!!")

if __name__ == "__main__":
    default_stopwords = stopwords.words('english')
    # Command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("dataset", help="Dataset")
    cli_parser.add_argument("-m", "--minimum", type=int, default=3, help="Minimum token length. Default 2 characets. Enter 0 to deactivate.")
    cli_parser.add_argument("-s", "--stopwords", default=default_stopwords, help="Stopword list. Enter 'D' to deactivate")
    args = cli_parser.parse_args()
    
    data = args.dataset
    #if args.minimum == 0:
    #    min_len = None
    #else:
    min_len = args.minimum
    
    # TODO: check what we want as an argument and fix the this snippet
    #if args.stopwords == ['D']:
    #    stopwords = None
    #else:
    stopwords = args.stopwords
    
    spimi = SPIMI(data, min_len,stopwords, 10000)
    spimi.run()