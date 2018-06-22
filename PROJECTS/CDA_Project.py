import re
import pymorphy2

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯёЁ'
one_char_POS = 'авиосуяАВИОСУЯ'
not_one_char_POS = 'бгдежзйклмнпртфхцчшщъыьэюёЁБГДЕЖЗЙКЛМНПРТФХЦЧШЩЪЫЬЭЮ'
RU_word_strip_pattern = (
    r'[{0}]+-?[{1}]*-?[{2}]*-?[{3}]*'.format(alph,
                                             alph,
                                             alph,
                                             alph))
el_not_one_char_POS = r'[{0}]\.[{1}]*\.*[{2}]*\.*'.format(not_one_char_POS,
                                                    not_one_char_POS,
                                                    not_one_char_POS)

morph = pymorphy2.MorphAnalyzer()
parser = morph.parse

def LCS_Length(X, Y):
    m = len(X)
    n = len(Y)
    c = [[0 for nn in range(n+1)] for mm in range(m+1)]
    b = [[0 for nn in range(n+1)] for mm in range(m+1)]
    for i in range(1, m+1):
        c[i][0] = 0
    for j in range(n+1):
        c[0][j] = 0
        for i in range(1, m+1):
            for j in range(1, n+1):
                if X[i-1] == Y[j-1]:
                    c[i][j] = c[i-1][j-1] + 1
                    b[i][j] = 'DIOG'
                else:
                    if c[i-1][j] >= c[i][j-1]:
                        c[i][j] = c[i-1][j]
                        b[i][j] = 'UP'
                    else:
                        c[i][j] = c[i][j-1]
                        b[i][j] = 'LEFT'
return c[m][n], b

def Print_LCS_num(b, X, i, j, s1, s2):
    if i == 0 or j == 0:
        return None
    if b[i][j] == 'DIOG':
        Print_LCS_num(b,X, i-1, j-1, s1, s2)
        s1.append(i-1)
        s2.append(j-1)
    elif b[i][j] == 'UP':
        Print_LCS_num(b, X, i-1, j, s1, s2)
    else:
        Print_LCS_num(b, X, i, j-1, s1, s2)
