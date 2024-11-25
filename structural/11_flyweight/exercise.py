# Flyweight Coding Exercise

# You are given a class called Sentence , which takes a string such as 'hello world'. 
# You need to provide an interface such that the indexer returns a flyweight that can be used 
# to capitalize a particular word in the sentence.

# Typical use would be something like:

# sentence = Sentence('hello world')
# sentence[1].capitalize = True
# print(sentence)  # writes "hello WORLD"

class Sentence:
    def __init__(self, plain_text):
        self.plain_text = plain_text
        self.formatting = []  # allows to store internally the flyweight

    # flyweight class
    class TextRange:
        def __init__(self, index, capitalize=False):
            self.index = index
            self.capitalize = capitalize
    
        def covers(self, position):
            return position == self.index
        
    def __getitem__(self, index):
        range = self.TextRange(index)
        self.formatting.append(range)  # store the flyweight
        # and also return it
        return range

    def __str__(self):
        words = self.plain_text.split(' ')
        result = []
        for index, word in enumerate(words):
            for r in self.formatting:
                if r.covers(index) and r.capitalize:
                    word = word.upper()
            result.append(word)
        return ' '.join(result)


if __name__ == '__main__':
    sentence = Sentence('hello world')
    sentence[1].capitalize = True
    print(sentence)  # writes "hello WORLD"
