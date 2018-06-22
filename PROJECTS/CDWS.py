import re
import pymorphy2

###CONSTANTS

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯёЁ'
cap_alph = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЁ'
low_alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюяё'

RU_word_strip_pattern = (
    r'[{0}]+-?[{1}]*-?[{2}]*-?[{3}]*'.format(alph,
                                             alph,
                                             alph,
                                             alph))

RU_word_strip_pattern_with_marks = (
    r'[{0}]+-?[{1}]*-?[{2}]*-?[{3}]*|<S>|</S>'.format(alph,
                                                      alph,
                                                      alph,
                                                      alph))

RU_word_strip_pattern_with_marks_n_articles = (
    r'[{0}]+-?[{1}]*-?[{2}]*-?[{3}]*|<S>|</S>|[0-9]+[.]*[0-9]*'.format(
        alph,
        alph,
        alph,
        alph))

word_strip_pattern = (
    r'[{0}]+-?[{1}]*-?[{2}]*-?[{3}]*|'
    r'[A-Za-z]+-?[A-Za-z]*-?[A-Za-z]*-?[A-Za-z]*|'
    r'[0-9]+[-.,]*[0-9]*[-.,]*[0-9]*[-.,]*[0-9]*[-.,]*[{4}]*'.format(alph,
                                                                     alph,
                                                                     alph,
                                                                     alph,
                                                                     alph))
sentence_breaker_pattern = (
    r'(?<=[\w][\w\)])\.\s+(?=[%s]\s|[%s][%s])'
                            % (cap_alph, cap_alph, alph))

###FUNCTIONS

##FIRST

def CD_word_stripper(PATH = r'PROJECTS\АС МО по поставке.txt',
                     counter=1,
                     reverse=False):
    '''Function gets the path string, a court decision act number as 'counter'
(equal to 1 by default) and a flag 'reverse' (equal to False by default, sorting
by word occurence number) and returns list of lines, list of stripped words,
set of words in the document and list with tuples of word and number of times
of its occurences in the list of stripped words.'''

    x = ''
    y = ''
    lines_list = []
    word_stripped_list = []

    with open(PATH, mode='r') as file:
        if counter > 1:
            while counter > 1:
                x = file.readline()
                if x[0:4] == '----':
                    counter -= 1

        while y[0:4] != '----':
            y = file.readline()
            lines_list.append(y)

    lines_list = lines_list[:-1]

    for i in lines_list:
        l = re.findall(word_strip_pattern, i)
        for w in l:
            w = w.lower()
            word_stripped_list.append(w)

    word_set = set(word_stripped_list)

    word_count_list = word_estimator(word_stripped_list, word_set)
    if reverse:
        word_count_list = sorted(word_count_list,
                                 key=lambda line: line[1],
                                 reverse=True)

    return lines_list, word_stripped_list, word_set, word_count_list

def CD_word_stripper_advanced(list_object, counter=1, reverse=False):
    '''Function gets a list object, a court decision act number as 'counter'
(equal to 1 by default) and a flag 'reverse' (equal to False by default, sorting
by word occurence number) and returns list of stripped words, set of words in
the document and list with tuples of word and number of times of its occurences
in the list of stripped words.'''

    word_stripped_list = []

    l = re.findall(word_strip_pattern, list_object[counter-1])
    for w in l:
        w = w.lower()
        word_stripped_list.append(w)

    word_set = set(word_stripped_list)

    word_count_list = word_estimator(word_stripped_list, word_set)
    
    if reverse:
        word_count_list = sorted(word_count_list,
                                 key=lambda item: item[1],
                                 reverse=True)

    return word_stripped_list, word_set, word_count_list

def CDWS_automatisation(PATHin = r'PROJECTS\АС МО по поставке.txt',
                        acts_number=1,
                        start_number=1):
    '''Function automatise word stripping process.'''
    
    index_store = list(range(start_number, start_number+acts_number))
    storage = dict()
    for j in index_store:
        key = 'act'+str(j)
        storage[key] = CD_word_stripper(PATH=PATHin, counter=j, reverse=True)

    return storage

def CDWS_advanced_automatisation(list_object,
                                  acts_number=1,
                                  start_number=1):
    '''Function automatise advanced word stripping process.'''
    
    index_store = list(range(start_number, start_number+acts_number))
    storage = dict()
    for j in index_store:
        key = 'act'+str(j)
        storage[key] = CD_word_stripper_advanced(list_object,
                                                 counter=j,
                                                 reverse=True)

    return storage

##SECOND

def CD_WS_NORM(FILE_NAME):
    '''Function gets the file name string and returns list splitted words,
list of stripped words, set of words in the document and list with tuples
of word and number of times of its occurences in the list of stripped words.'''

    storage = list()
    morph = pymorphy2.MorphAnalyzer()

    with open(r'PROJECTS\{}.txt'.format(FILE_NAME), mode='r') as file:
        text = file.read()

    sent_split = re.split(sentence_breaker_pattern, text)

    sent_marked = ['<S> ' + i + ' </S>' for i in sent_split]

    for i in sent_marked:
        match = re.findall(RU_word_strip_pattern_with_marks, i)
        normalised = [morph.parse(i)[0][2] for i in match]
        storage.extend(normalised)

    common_set = set(storage)

    est_word_list = word_estimator(storage, common_set)
    srt_est_word_list = sorted(est_word_list,
                               key=lambda item: item[1],
                               reverse=True)

    return storage, common_set, srt_est_word_list

####Utils

def word_estimator(splitted_words_list, vocabulary_set):
    return [(i, splitted_words_list.count(i)) for  i in vocabulary_set]

####Some optimisation needed
'''
def word_normaliser(list_of_words):
    morph = pymorphy2.MorphAnalyzer()
    return [morph.parse(i)[0][2] for i in list_of_words]
'''
