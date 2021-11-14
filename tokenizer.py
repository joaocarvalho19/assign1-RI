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

    def get_tokens(self, data, _id):
        #for _id, l in self.dataset.items():
        # Remove leftover HTML tags, make all words lower case and remove ,.-
        data = re.sub('<[^<]+?>', '', data)
        data = re.sub('\W',' ',data)
        #data = re.sub("[,.!-\'\?]+", ' ', data)
        # Create a clean list containing the words

        content_list = list(set(data.split()))
        #body_list = list(set(l[1].split()))

        # Minimum length filter
        if self.min_len != None:
            content_list = [x for x in content_list if (len(x) >= self.min_len)]
            #body_list = [x for x in body_list if len(x) > self.min_len]

        # Stopwords
        if self.stopwords != None:
            content_list = list(set(content_list) - set(self.stopwords))
            #body_list = list(set(body_list) - set(self.stopwords))

        # Porter stemmer
        tokens = [(self.porter_stemmer.stem(w), _id) for w in content_list if w.isascii()]
        #body_list = [self.porter_stemmer.stem(w) for w in body_list]

        return tokens