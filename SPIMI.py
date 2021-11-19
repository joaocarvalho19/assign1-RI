import argparse
from tokenizer import Tokenizer
from indexer import Indexer
from sys import argv
import csv
import nltk
from nltk.corpus import stopwords
import time
import os



class SPIMI:
    def __init__(self, dataset, min_length, stopwords, limit=10000):
        self.dataset = dataset
        self.tokenizer = Tokenizer(min_length,stopwords)
        self.indexer = Indexer()
        self.chunk_limit = limit
        self.block_num = 1


    def run(self):
        # Main function
        count = 0
        begin = time.time()
        with open(self.dataset,'r') as fd:
            rd = csv.DictReader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
            tokens = []
            print("Indexing...")
            for row in rd:                
                # Shorter blocks mean a faster execution
                if count < self.chunk_limit:
                    review_id, product_title, review_headline, review_body = row['review_id'], row["product_title"], row['review_headline'], row['review_body']
                    string = product_title + " " + review_headline + " " + review_body
                    
                    tokens = self.tokenizer.get_tokens(string, review_id)
                    self.indexer.run(tokens)
                    count+=1
                     
                # reaching limit - write block on disk
                else:
                    # clear memory
                    tokens = []
                    self.indexer.write_block(self.block_num)
                    self.block_num += 1
                    
                    # clear memory
                    self.indexer.clear_index()
                    count=0
                    #break

        if tokens != []:
            self.indexer.run(tokens)
            self.indexer.write_block(self.block_num)
        
        # clear memory
        tokens = []
        self.indexer.clear_index()
        
        # Merge blocks
        
        self.indexer.merge_blocks()
        
        #self.indexer.merge_indexes()
        
        print("Total indexing time (min): ", round((time.time()-begin)/60, 2))
        print("Total index size on disk: ", self.indexer.get_index_size())
        print("Vocabulary size: ", self.indexer.get_vocabulary_size())
        print("Number of temporary index segments written to disk: ", self.block_num)
        
        print("Loading index into memory...")
        begin = time.time()
        #self.indexer.load_index()
        #print("Loading time: ", round((time.time()-begin)/60, 5))
        
        """while True:
            term = input('Term to be searched: ')
            if term in self.indexer.get_final_index().keys():
                print(self.indexer.get_final_index()[term])
            elif term == 'Quit':
                break
            else:
                print('No such term on the index')
        print("Finish!!")"""

if __name__ == "__main__":
    default_stopwords = stopwords.words('english')
    # Command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("dataset", help="Dataset")
    cli_parser.add_argument("-m", "--minimum", type=int, default=3, help="Minimum token length. Default 2 characets. Enter 0 to deactivate.")
    cli_parser.add_argument("-s", "--stopwords", default=None, help="Stopword list. Enter 'D' to deactivate")
    args = cli_parser.parse_args()
    
    data = args.dataset
    min_len = args.minimum
    
    if args.stopwords == None:
        stopwords = default_stopwords
    else:
        if args.stopwords == 'D':
            stopwords = args.stopwords
        else:
            stopwords = []
            with open(args.stopwords, 'r') as _file:
                for row in _file:
                    stopwords.append(row.strip())
    
    spimi = SPIMI(data, min_len,stopwords, 20000)
    spimi.run()
