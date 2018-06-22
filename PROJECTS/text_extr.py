import re
pattern = r'\S* *\S* *\S* *\S* *[сС]тат\w{1,4} \d{1,4}\.?\d{0,3} *\S* *\S* *\S* *\S* *\S* *\S* *\S*'

def text_extraction(path):
    '''
    This function extracts text without additional decoding from the file
    on which path variable points. After extraction text is striped from
    blank lines in the string literals embeded in the list object. All
    blank entries are removed too. List object is returned in the end
    '''
    with open(path) as file:
        text = [line.strip() for line in file]
    for i in reversed(range(len(text))):
        if text[i] == '': del text[i]
    return text

def simple_court_decision_analysis(list_of_strings):
    '''
    This function uses the result of text_extraction() to proceed the text of
    court decision. It returns the plaintiff's demands, list of related legal
    articles which are pointed out through the decision's text, final court
    decision
    '''
    storage = []
    for line in list_of_strings:
        match = re.search(r'с* (иском|заявлением) (о\w?|к)', line)
        if match:
            print (line)

    print('\n')

    for line in list_of_strings:
        match = re.findall(pattern, line)
        if match:
            storage.extend(match)

    print('\n')

    for i in range(len(storage)):
        print(i, '.-> ', storage[i])

    print('\n')

    for j in range(len(list_of_strings)):
        match = re.search(r'^(постановил\w+|ПОСТАНОВИЛ\w+):$|^(определил\w+|ОПРЕДЕЛИЛ\w+):$|^(решил\w+|РЕШИЛ\w+):$', list_of_strings[j])
        if match:
            for s in list_of_strings[j:]:
                print (s)

def full_court_decision_analysis(path):
    '''
    This function combines text_extraction() and
    simple_court_decision_analysis() together.
    '''
    storage = []

    with open(path) as file:
        list_of_strings = [line.strip() for line in file]
    for i in reversed(range(len(list_of_strings))):
        if list_of_strings[i] == '': del list_of_strings[i]

    for line in list_of_strings:
        match = re.search(r'с* (иском|заявлением) (о\w?|к)', line)
        if match:
            print (line)

    print('\n')

    for line in list_of_strings:
        match = re.findall(pattern, line)
        if match:
            storage.extend(match)

    print('\n')

    for i in range(len(storage)):
        print(i+1, '.-> ', storage[i])

    print('\n')

    for j in range(len(list_of_strings)):
        match = re.search(r'^(постановил\w+|ПОСТАНОВИЛ\w+):$|^(определил\w+|ОПРЕДЕЛИЛ\w+):$|^(решил\w+|РЕШИЛ\w+):$', list_of_strings[j])
        if match:
            for s in list_of_strings[j:]:
                print (s)
