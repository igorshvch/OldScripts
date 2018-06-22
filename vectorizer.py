import math
import pymorphy2
import re
try:
    import cd_processing.textextrconst as tec
except ModuleNotFoundError:
    import textextrconst as tec

parser = pymorphy2.MorphAnalyzer().parse

control = ['арбитражный', 'в', 'взыскание',
           'город', 'далее', 'денежный',
           'договор', 'иск', 'истец', 'к',
           'о', 'обратиться', 'общество',
           'ответственность', 'ответчик',
           'размер', 'рубль', 'с', 'средство',
           'суд', 'сумма']
control_len = len(control)

def vectorizer(string):
    split = string.split()
    length = len(split)
    clean = [word.strip('.?!,:;-()\'\"') for word in split]
    norm = [parser(word)[0][2] for word in clean]
    result = []
    vector = []
    norm_result = []
    for i in control:
        if i in norm:
            #result.append(1)
            for j in control:
                try:
                    vector.append(abs(norm.index(j)-
                                       norm.index(i)))
                except ValueError: pass
            vector_len = math.sqrt(sum([i**2 for i in vector]))
            result.append(vector_len)
            vector = []
        else:
            result.extend([0.0])#,0.1])
    m = max(result)
    for i in result:
        try:
            norm_result.append((i/m))
        except ZeroDivisionError:
            norm_result.append(0.0)
    for i in range(len(norm_result)):
        if norm_result[i] == 0:
            norm_result[i]+=0.1
    return norm_result



        
            
