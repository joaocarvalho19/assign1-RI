from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class Tokenizer:
    '''
    Initialize the Tokenizer.
    ARGUMENTS:
        dataset - dataset to be tokenized
        min_length - minimum token length
        stopwords - list containing the stopwords
    '''
    def __init__(self, dataset, min_length, stopwords): 
        self.dataset = dataset
        self.min_len = min_length
        self.stopwords = stopwords
        self.porter_stemmer = PorterStemmer()
    
    '''
    Runs the tokenizer and returns the tokens.
    RETURNS:
        list containing the tokens
    '''
    def get_tokens(self):
        for _id, l in self.dataset.items():
            headline_list = list(set(l[0].split()))
            body_list = list(set(l[1].split()))

            # Minimum length filter
            if self.min_len != None:
                headline_list = [x for x in headline_list if len(x) > self.min_len]
                body_list = [x for x in body_list if len(x) > self.min_len]

            # Stopwords
            if self.stopwords != None:
                headline_list = list(set(headline_list) - set(self.stopwords))
                body_list = list(set(body_list) - set(self.stopwords))

            # Porter stemmer
            headline_list = [self.porter_stemmer.stem(w) for w in headline_list]
            body_list = [self.porter_stemmer.stem(w) for w in body_list]

            print(headline_list)
            print(body_list)

            # Only first row
            break
        return