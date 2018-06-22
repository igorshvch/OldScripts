import re
import pymorph2
from functools import reduce

parser = pymorph2.MorphAnalyzer().parse

SOURCE = r'PROJECTS\Суды по поставке 20161219.txt'
STR_PAT = r'(?<=(установил|Установил|УСТАНОВИЛ):\n\n).*(?=\n)

def claim(path=SOURCE, pattern=STR_PAT):
    '''Extracts claim' parts and store them to list'''
    with open(path) as file:
        text = file.read()
    return re.findall(pattern, text)

def normalizer(claim):
    '''Returns normalised claim words: each claim stored
    in separate list and each word is inside the claim's list'''
    store = claim
    for record in store:
        record = [parser(word.strip(',.!?-()\\:;'))[0][2] for word in record]
    return store
################################
def unite(claim):
    '''Returns number of all words in all claims'''
    return len(' '.join(claim))
################################
def unite_s(norm):
    '''Unites all words' sets and returns the set of all used words'''
    store = norm
    first_set = set(store[0])
    return reduce(first_set.union, (set(record) for record in store))

def intersect(norm):
    '''Intersects all words' sets and returns the set of coomon words'''
    store = norm
    first_set = set(store[0])
    return reduce(first_set.intersection, (set(record) for record in store))

def prob_count(unite_s, claim):
    '''Counts simple probability of word occurence
    in reflection to the claim'''
    all_words = unite
    return zip()
    
    
