import csv
from sys import argv

def tokenization(data):
    for _id, l in data.items():
        headline_list = l[0].split(" ")
        body_list = l[1].split(" ")
        print(headline_list)
        print(body_list)
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
    data = parser(dataset)
    tokenization(data)