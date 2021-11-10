import argparse
from parser import Parser
from tokenizer import Tokenizer
from sys import argv

default_stopwords = ['a','about','above','after','again','against','all','am','an','and','any','are','aren\'t','as','at','be','because','been',
                     'before','being','below','between','both','but','by','can\'t','cannot','could','couldn\'t','did','didn\'t','do','does','doesn\'t', 
                     'doing','don\'t','down','during','each','few','for','from','further','had','hadn\'t','has','hasn\'t','have','haven\'t','having', 
                     'he','he\'d','he\'ll','he\'s','her','here','here\'s','hers','herself','him','himself','his','how','how\'s','i','i\'d','i\'ll', 
                     'i\'m','i\'ve','if','in','into','is','isn\'t','it','it\'s','its','itself','let\'s','me','more','most','mustn\'t','my','myself', 
                     'no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shan\'t', 
                     'she','she\'d','she\'ll','she\'s','should','shouldn\'t','so','some','such','than','that','that\'s','the','their','theirs','them', 
                     'themselves','then','there','there\'s','these','they','they\'d','they\'ll','they\'re','they\'ve','this','those','through','to', 
                     'too','under','until','up','very','was','wasn\'t','we','we\'d','we\'ll','we\'re','we\'ve','were','weren\'t','what','what\'s', 
                     'when','when\'s','where','where\'s','which','while','who','who\'s','whom','why','why\'s','with','won\'t','would','wouldn\'t', 
                     'you','you\'d','you\'ll','you\'re','you\'ve','your','yours','yourself','yourselves']


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
