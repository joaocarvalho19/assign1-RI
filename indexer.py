

class Indexer:
    def __init__(self):
        self.indexed_tokens = {}

    def run(self, tokens):
        for token, _id in tokens:
            if token not in self.indexed_tokens.keys():
                self.indexed_tokens[token] = [_id]
            else:
                if _id not in self.indexed_tokens[token]:
                    self.indexed_tokens[token] += [_id]

    def write_block(self):
        sorted_index = dict(sorted(self.indexed_tokens.items()))
        with open("output.txt",'w+') as f:
            for token, value in sorted_index.items():
                string = token + ' : ' + str(value) + '\n'
                f.write(string)
        
        self.indexed_tokens = {}

