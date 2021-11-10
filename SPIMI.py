import argparse
from parser import Parser
from tokenizer import Tokenizer
from sys import argv


def main(min_length, stopwords, dataset):
    # Main function used to call the parser and tokenizer in a cleaner way
    parser = Parser(dataset)
    data = parser.parse()
    
    tokenizer = Tokenizer(data,min_length,stopwords)
    tokens = tokenizer.get_tokens()
    print(tokens)

    return

if __name__ == "__main__":
    # Command line arguments
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("dataset", help="Dataset")
    cli_parser.add_argument("-m", "--minimum", type=int, default=2, help="Minimum token length. Default 2 characets. Enter 0 to deactivate.")
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
    
        
    main(min_len,stopwords,data)
