import csv

class Parser:
    ''' 
    Initialize the Parser.
    ARGUMENTS: dataset - dataset to be parsed    
    '''
    def __init__(self,dataset):
        self.dataset = dataset
    
    '''
    Parse the dataset and return the data in a dictionary.
    RETURN: data_dict - dictionary mapping the 'review_headline' and 'review_body' to the 'review_id'
    '''
    def parse(self):
        data_dict = {}  # key = "review_id"; value = list with "review_headline" and "review_body"
        with open(self.dataset) as fd:
            rd = csv.reader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in rd:
                if row[2] != 'review_id':
                    review_id, review_headline, review_body = row[2], row[12], row[13]
                    data_dict[review_id] = [review_headline, review_body]
        return data_dict
