#Finds position of each enterance of the word through the list

def find_word_position (ls, word):
    store = []
    position = 0
    n = 0

    for name in ls:
        if word == name:
            store.append(ls.index(name, position))
            position = store[n] + 1
            n += 1
        else:
            continue

    return store