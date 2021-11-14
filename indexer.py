import os

class Indexer:
    def __init__(self):
        self.indexed_tokens = {}
        self.vocabulary_size = 0
        self.num_temp_segments = 0

    def run(self, tokens):
        for token, _id in tokens:
            if token not in self.indexed_tokens.keys():
                self.indexed_tokens[token] = [_id]
            else:
                if _id not in self.indexed_tokens[token]:
                    self.indexed_tokens[token] += [_id]
    
    def getIndexedTokens(self):
        return self.indexed_tokens
    
    def getVocabularySize(self):
        return self.vocabulary_size

    def getNumTS(self):
        return self.num_temp_segments

    def write_block(self, post_list):
        self.num_temp_segments+=1
        sorted_index = dict(sorted(post_list.items()))
        with open("output.txt",'w') as f:
            for token, value in sorted_index.items():
                string = token + ' : ' + str(value) + '\n'
                f.write(string)
        
        self.vocabulary_size = len(post_list)
        self.indexed_tokens = {}
    
    def merge_blocks(self):
        actual_list = {}

        # Check if output file exists
        if not os.path.isfile('./output.txt'):
            return self.indexed_tokens

        # Check if output file is not empty
        if not os.stat("output.txt").st_size == 0:
            with open("output.txt",'r') as f:
                for line in f.readlines():
                    line = line.replace("\n","")
                    l = line.split(" : ")
                    token = l[0]
                    id_list = [str(s) for s in l[1].replace('[', '').replace(']', '').replace("'", '').split(',')]
                    actual_list[token] = id_list
            f.close()

            for t in self.indexed_tokens.keys():
                if t in actual_list.keys():
                    list1 = self.indexed_tokens[t]
                    list2 = actual_list[t]
                    final_list = list(dict.fromkeys(list1 + list2))
                    actual_list[t] = final_list
                else:
                    actual_list[t] = self.indexed_tokens[t]

            return actual_list
        else:
            return self.indexed_tokens