import re
try:
    import cd_processing.textextrconst as tec
except ModuleNotFoundError:
    import textextrconst as tec


def find_tagged_string(tag, user_string, user_flags):
    '''
    Finds tagget string and returns it without tags
    '''
    pattern = r'(?<={0} ).*(?= \/{1})'.format(tag, tag)
    match = re.compile(pattern, flags = user_flags)
    string = match.search(user_string).group(0)
    return string

def text_cleaning(string):
    pattern = tec.RU_word_strip_pattern
    lst = re.findall(pattern, string)
    return lst

class Bag():
    def __init__(self):
        self.length = 0
        self.chain = []
        self.container = []
        
    def append(self, new_words_list):
        length = len(new_words_list)
        if length > self.length:
            dif = length - self.length
            for i in range(dif):
                self.chain.append({})
            self.length = length
        for j in range(len(new_words_list)):
            word = new_words_list[j]
            if self.chain[j].get(word):
                self.chain[j][word]+=1
            else:
                self.chain[j][word]=1

    def output(self):
        container = []
        for i in self.chain:
            ordered = sorted(i.items(), key=lambda x: x[1], reverse=True)
            container.append(ordered[0])
        self.container = container
        

            
            

