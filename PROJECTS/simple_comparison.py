import pymorphy2

morph = pymorphy2.MorphAnalyzer()
parser = morph.parse

def compare():
    breaker = 1
    while breaker:
        store = []
        string1 = input('Введите строку 1:\n')
        string2 = input('Введите строку 2:\n')
        for i in string1, string2:
            split = i.split()
            clean = [word.strip('.?!,:;-()\'\"') for word in split]
            norm = [parser(word)[0][2] for word in clean]
            store.append(set(norm))
        holder = store[0] & store[1]
        result = ' '.join(holder)
        print('\n'+('-'*20)+'\n'+result+'\n'+('-'*20)+'\n')
        breaker = input('Чтобы прододжить,'
                        +'введите значение, чтобы '
                        +'прервать, нажмите "Enter":\n')
