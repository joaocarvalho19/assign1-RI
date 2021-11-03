import csv
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sys import argv

def tokenizer(data, min_len, stopwords, ps):
    for _id, l in data.items():
        headline_list = list(set(l[0].split()))
        body_list = list(set(l[1].split()))

        # Minimum length filter
        if min_len:
            headline_list = [ x for x in headline_list if len(x) > min_len ]
            body_list = [ x for x in body_list if len(x) > min_len ]

        # Stopwords
        if stopwords:
            headline_list = list(set(headline_list) - set(stopwords))
            body_list = list(set(body_list) - set(stopwords))

        # Porter stemmer
        headline_list = [ps.stem(w) for w in headline_list]
        body_list = [ps.stem(w) for w in body_list]
        
        print(headline_list)
        print(body_list)

        # Only first row
        break

def parser(dataset):
    data_dict = {}          #key = "review_id"; value = list with "review_headline" and "review_body"
    with open(dataset) as fd:
        rd = csv.reader(fd, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in rd:
            if row[2] != 'review_id':
                review_id, review_headline, review_body = row[2], row[12], row[13]
                data_dict[review_id] = [review_headline, review_body]
    return data_dict

if __name__ == "__main__":
    stopwords = ['the', 'a', 'to', 'of']
    dataset = argv[1]
    min_len = 1
    ps = PorterStemmer()

    data = parser(dataset)
    tokenizer(data, min_len, stopwords, ps)