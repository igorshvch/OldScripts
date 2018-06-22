import re
import pymorphy2
import textextrconst as tec
from functools import reduce
from writer import writer

parser = pymorphy2.MorphAnalyzer().parse

SOURCE = r'C:\Python36\1974 Acts.txt'
DEMAND_FIND_PAT = tec.demand_find_pattern
RU_WORD_PAT = tec.RU_word_strip_pattern


def demand(path=SOURCE, pattern=DEMAND_FIND_PAT, acts_num=25):
    '''Extracts each demand, appends it to list
    and splits it to words which are stored in lists either'''
    cleaned_demands = []
    with open(path) as file:
        text = file.read()
    sep_demands = re.findall(pattern, text)[:acts_num-1]
    for demand in sep_demands:
        demand = demand.split()
        demand = [word.strip(',.!?-():;\'"').lower() for word in demand]
        cleaned_demands.append(demand)
    for demand in cleaned_demands:
        for i in reversed(range(len(demand))):
            if not re.fullmatch(RU_WORD_PAT, demand[i]):
                del demand[i]
    return cleaned_demands

def demand_num(cleaned_demands):
    '''Returns number of all demands'''
    return len(cleaned_demands)

def normalizer(cleaned_demands, usage='Internal'):
    '''Returns normalised demand words: each demand stored
    in separate list and each word is inside the claim's list.
    Returns list or may serve as generator. Behavior depends on
    keyword argument "usage" value'''
    store = cleaned_demands
    norm = []
    if usage=='Internal':
        for demand in store:
            norm.append([parser(word)[0][2] for word in demand])
        return norm
    elif usage=='External':
        for demand in store:
            norm_demand = [parser(word)[0][2] for word in demand]
            yield norm_demand

def all_records_list(store):
    '''Returns list of all normalised words or Ngramms
    (words in Ngramms are normalised too)'''
    return [item for record in store for item in record]

def record_num(all_words_or_Ngramms_list):
    '''Returns number of all words or Ngramms in all demands'''
    return len(all_words_or_Ngramms_list)

def unite(all_words_or_Ngramms_list):
    '''Unites all words or Ngrmms into a set
    and removes repetitons. Returns the set of all used items'''
    return set(all_words_or_Ngramms_list)

def intersect(norm):
    '''Intersects all demands word sets and returns the set of common words'''
    store = norm
    first_set = set(store[0])
    return reduce(first_set.intersection, (set(record) for record in store))

def prob_count(demand_num, all_records_list, record_num, unite):
    '''Counts simple probability of word occurence
    to the number of all words and to the number of
    all claims'''
    all_words = sorted(all_records_list)
    uniqe_words = sorted(unite)
    words_prob = [(word,
                   all_words.count(word)/record_num,
                   all_words.count(word)/demand_num)
                  for word in uniqe_words]
    return words_prob

def demands_bigrams(norm):
    '''Returns the list of lists of all bigrams
    in each demand (words are normalised)'''
    store = norm
    bigr_store = []
    temp_store = []
    for record in norm:
        for counter in range(1, len(record)):
            temp_store.append((record[counter-1],
                               record[counter]))
        bigr_store.append(temp_store)
        temp_store = []
    return bigr_store

def prob_count_bigr(demand_num, record_num, all_records_list, unite, sorting=None):
    '''Counts simple probability of bigrams occurence
    to the number of all bigrams (record_num var)
    and to the number of all demands'''
    all_bigrams = all_records_list
    if sorting == None:
        all_bigrams = sorted(all_records_list, key=lambda record: record[0])
    uniqe_bigrams = sorted(unite, key=lambda record: record[0])
    bigr_prob = [(bigram,
                   all_bigrams.count(bigram)/record_num,
                   all_bigrams.count(bigram)/demand_num)
                  for bigram in uniqe_bigrams]
    if sorting == 'Claim':
        bigr_prob = sorted(bigr_prob, key=lambda record: record[2], reverse=True)
    elif sorting == 'Bigram':
        bigr_prob = sorted(bigr_prob, key=lambda record: record[1], reverse=True)
    return bigr_prob
'''
def word_bag (Ngramm_prob, len_list=None, prob_border=None, sorting=True):
    store = [[Ngramm, prob_to_claim_num]
             for Ngramm, _, prob_to_claim_num
             in Ngramm_prob]
    if sorting == None:
        store = sorted(store, key=lambda record: record[1], revese=True)
    if (len_list or prob_border) == True:
        if len_list != None:
            store = store[:len_list]
        if prob_border != None:
            store = [record for record in store if record[1]>=prob_border]
    else:
        store = store[:30]
    for i in range(1, len(store)):
'''        
    

############################################
############################################
############################################
            
def selftest(filename_word,
             filename_bigr,
             path=SOURCE,
             acts=25,
             sort_order=None,
             ret_val=None):
    '''Module's "main()" functon, tests all module's functions
    and prints results of probability estimation'''
    print('Demands storing')
    cl_dem = demand(path=path, acts_num=acts)
    print('Demands counting')
    dem_num = counter = demand_num(cl_dem)
    print('Total demands number: {0}'.format(dem_num))
    print('Words normalisation')
    norm = []
    percent = list(range(101))
    iterator = normalizer(cl_dem, usage='External')
    while counter:
        norm.append(next(iterator))
        if (len(norm)/dem_num*100) in percent:
            print('#', end='')
        counter -=1
    print()
    print('Demands concatenation')
    all_words_list = all_records_list(norm)
    print('Words counting')
    word_num = record_num(all_words_list)
    print('Removing doubled words')
    union = unite(all_words_list)
    print('Probability estimating')
    word_prob = prob_count(dem_num, all_words_list, word_num, union)

    print('Bigrams extracting')
    dem_bigrams = demands_bigrams(norm)
    print('Demands concatenation (bigrmas step)')
    all_bigram_list = all_records_list(dem_bigrams)
    print('Bigrams counting')
    bigr_num = record_num(all_bigram_list)
    print('Removing doubled bigrams')
    union_bigr = unite(all_bigram_list)
    print('Bigrmas probability estimating')
    bigr_prob = prob_count_bigr(dem_num,
                                bigr_num,
                                all_bigram_list,
                                union_bigr,
                                sorting=sort_order)
    if ret_val:
        if sort_order == 'Claim':
            return bigr_prob[:40]
        else:
            return bigr_prob
    else:
        print('-'*30)
        print('Word_prob printing')
        writer(word_prob, filename_word)
        print('Bigr_prob printing')
        writer(bigr_prob, filename_bigr)
        print ('OK!')
