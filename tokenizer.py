import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

class Tokenizer:
    '''
    Initialize the Tokenizer.
    ARGUMENTS:
        dataset - dataset to be tokenized
        min_length - minimum token length
        stopwords - list containing the stopwords
    '''
    def __init__(self, min_length, stopwords): 
        self.min_len = min_length
        self.stopwords = stopwords
        self.porter_stemmer = PorterStemmer()
    
    '''
    Runs the tokenizer and returns the tokens.
    RETURNS:
        list containing the tokens
    '''

    def get_tokens(self, _data, _id):
        # Remove non ASCII characters
        data = re.sub('\W+', ' ', _data).lower().split()


        # Minimum length filter
        if self.min_len != 0:
            data = [x for x in data if len(x) >= self.min_len]
            
        # Stopwords filter
        if self.stopwords != 'D':
            data = [x for x in data if x not in self.stopwords]

        # Porter stemmer
        tokens = [(self.porter_stemmer.stem(t), _id) for t in data if t.isalpha()]
        
        return tokens