import argparse
from parser import Parser
from tokenizer import Tokenizer
from indexer import Indexer
from sys import argv
import csv
import psutil

class SPIMI:
    def __init__(self, dataset, min_length, stopwords):
        self.dataset = dataset
        self.tokenizer = Tokenizer(min_length,stopwords)
        self.indexer = Indexer()


    def run(self):
        # Main function used to call the parser and tokenizer in a cleaner way

        limit = 10
        count = 0
        with open(self.dataset) as fd:
                rd = csv.reader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
                tokens = []
                for row in rd:
                    #memory = psutil.virtual_memory().available
                    #print(memory)
                    if count < limit:   #block
                        if row[2] != 'review_id':
                            review_id, review_headline, review_body = row[2], row[12], row[13]
                            string = review_headline + " " + review_body
                            tokens += self.tokenizer.get_tokens(string, review_id)
                        
                        count+=1
                    else:
                        # reaching limit - write block on disk
                        #count=0
                        self.indexer.run(tokens)
                        self.indexer.write_block()
                        # clear memory
                        tokens = []
                        break

        return

if __name__ == "__main__":
    # Command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("dataset", help="Dataset")
    cli_parser.add_argument("-m", "--minimum", type=int, default=2, help="Minimum token length. Default 2 characets. Enter 0 to deactivate.")
    cli_parser.add_argument("-s", "--stopwords", default=['the', 'a', 'to', 'of'], help="Stopword list. Enter 'D' to deactivate")
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