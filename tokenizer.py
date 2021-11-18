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

        #content_list = re.sub("[^0-9a-zA-Z]+"," ",data).lower().split(" ")
        data = re.sub('\W+', ' ', _data).lower().split()
        #body_list = list(set(l[1].split()))

        # Minimum length filter, stopwords and Porter stemmer
        if self.min_len != 0:
            data = [x for x in data if len(x) >= self.min_len]
            
        if self.stopwords != 'D':
            data = [x for x in data if x not in self.stopwords]
    
        #tokens = [(self.porter_stemmer.stem(w), _id) for w in content_list if (len(w) >= self.min_len) and (w not in self.stopwords)]
        #body_list = [w for w in body_list if len(w) > self.min_len]

        # Porter stemmer
        tokens = [(self.porter_stemmer.stem(t), _id) for t in data if t.isalpha()]
        #body_list = [self.porter_stemmer.stem(w) for w in body_list]
        return tokens