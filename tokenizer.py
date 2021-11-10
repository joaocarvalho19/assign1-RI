import re
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
            # Remove leftover HTML tags, make all words lower case and remove ,.-
            l = re.sub('<[^<]+?>', '', l)
            l = l.lower()
            l = re.sub("[,.-]+", ' ', l)
            # Create a clean list containing the words
            content_list = list(set(l.split()))
            #content_list = [x.lower() for x in content_list]
            #content_list = [re.sub("[,.-]+", ' ', x) for x in content_list]
            #print(content_list)
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
            #content_list = [self.porter_stemmer.stem(w) for w in content_list]
            #body_list = [self.porter_stemmer.stem(w) for w in body_list]

            #print(content_list)
            #print(body_list)

            # Only first row
            break
        return content_list