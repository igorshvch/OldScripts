import re

def fid():
    counter = True
    while counter == True:
        sample = input('--->')
        m = re.search('(?<=ID=)\d{1,5}', sample)
        print ('\n' + m.group(0) + '\n')
        counter = bool(int(input('do you whant to proceed? (Y = 1; N = 0) --->')))
