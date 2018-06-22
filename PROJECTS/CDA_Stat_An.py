import pymorhpy2
from functools import reduce

morph = pymorphy2.MorphAnalyzer()
parser = morph.parse

def word_normaliser(string):
    cleaned = [i.rstrip(',.:;-').lower() for i in string.split()]
    normalised = [parser(i)[0][2] for i in cleaned]
    grouped = [(clean_word, norm_word, position)
               for clean, norm, position
               in zip(cleaned, normalised, range(len(cleaned)))]
    return cleaned, normalised, grouped

def set_operations(*args):
    return reduce(lambda x, y: x&y, (set(i) for i in args))
    #return set(args[0]).intersection((set(i) for i in args[0:]))

