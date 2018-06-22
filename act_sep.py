try:
    import cd_processing.textextrconst as tec
except ModuleNotFoundError:
    import textextrconst as tec
import re
import math
from datetime import datetime as dt
from sys import version_info
from writer import writer

PyVer = version_info[1]

pattern_clean = r'-{66}\nКонсультантПлюс.+?-{66}\n'
pattern_sep = r'\n\n\n-{66}\n\n\n'

try:
    open('C:\\Python3{}\\test.txt'.format(PyVer))
    ex_path = r'C:\Python3{}\1974 Acts.txt'.format(PyVer)
except:
    ex_path = 'AP\\АС МО 1023 2017-2303-0106.txt'

my_path = 'AP\\АС МО 1023 2017-2303-0106.txt' #r'C:\Python3{}\1974 Acts.txt'.format(PyVer)

class ActSep():
    def __init__(self,
                 my_path=my_path,
                 pattern_clean=pattern_clean,
                 pattern_demd_sep = tec.demand_find_pattern,
                 pattern_sep=pattern_sep,
                 auto_mode = False):
        self.cleaned = ''
        self.demand_store = []
        self.path = my_path
        self.pattern_clean = pattern_clean
        self.patterm_demd_sep = pattern_demd_sep
        self.pattern_sep = pattern_sep
        self.store = []
        self.text_clean()
        self.acts_separation()
        if auto_mode == True:
            self.act_clean()
            self.voc_create()
            self.voc_fill()
        

    def text_clean(self):
        with open(self.path) as file:
            text = file.read()[1:-71]
        self.cleaned = re.subn(self.pattern_clean,
                               repl='',
                               string=text,
                               flags=re.DOTALL)[0]
        print('Text is cleaned. {} file was used.'.format(self.path))

    def acts_separation(self):
        store = re.split(self.pattern_sep, string=self.cleaned)
        self.store = [re.subn('\n', repl=' ннннн ', string=act)[0]
                      for act
                      in store]
        del store
        acts_num = len(self.store)
        self.cleaned = None
        self.N = len(self.store)
        print('Text is separated.',
              'There are {} acts.'.format(acts_num),
              'Cleaned text is deleted.',
              'Total number of documents in the collection saved to'
              +' .N attribute',
              '\nActs are stored in the .store attribute',
              '\nAccessible methods:\n.act_clean()',
              '\n.voc_create()\n.voc_fill()')

    def act_clean(self, remove_raw_text=True):
        pattern = tec.RU_word_strip_pattern
        if remove_raw_text==True:
            self.store = [re.findall(pattern, item.lower())
                          for item in self.store]
            print('Each stored act is splitted into words,',
                  'each word is lowerd and cleaned from punctuation.',
                  '\nRaw text of each act is removed')
        elif remove_raw_text==False:
            self.store_cleaned = [re.findall(pattern, item.lower())
                                  for item in self.store]
            print('Each stored act is splitted into words,',
                  'each word is lowerd and cleaned from punctuation.',
                  '\nRaw text of each act is accessible from .store attribute',
                  '\nCleaned text of each act is accessible',
                  'from .store_cleaned attribute')

    def voc_create(self, remove_raw_text=True, write=False):
        buf = []
        if remove_raw_text==True:
            for item in self.store:
                buf.extend(item)
        elif remove_raw_text==False:
            for item in self.store_cleaned:
                buf.extend(item)
        com_words = set(buf)
        self.com_dict = {key:{} for key in sorted(com_words)}
        print('Vocabulary is created! Accessible through .com_dict attribute')
        if write:
            writer(sorted(com_words), 'com_words')
            print('Vocabulary is written to the external file!')

    def voc_fill(self, remove_raw_text=True):
        d = self.com_dict
        start = dt.now()
        print('Start time is {}'.format(start))
        if remove_raw_text==True:
            for act_num in range(len(self.store)):
                act = self.store[act_num]
                for word_num in range(len(act)):
                    word = act[word_num]
                    if not d[word].get(act_num):
                        self.com_dict[word][act_num] = [word_num]
                    elif type(d[word].get(act_num))== type(list()):
                        self.com_dict[word][act_num].append(word_num)
            end = dt.now()
            print('End time is {}'.format(end))
            del d
        elif remove_raw_text==False:
            for act in self.store_cleaned:
                for word in act:
                    if d.get(word, None)!=None:
                        self.com_dict[word].append(counter)
                counter+=1
            end = dt.now()
            print('End time is {}'.format(end))
            del d
        time_spent = end-start
        print('The vocabulary is filled.',
              'Time spent: {}'.format(time_spent),
              'Accessible through the .com_dict attribute', sep='\n')

    def cf(self, word):
        if self.com_dict.get(word, None) != None:
            counter = 0
            for docID in self.com_dict[word].keys():
                counter += len(self.com_dict[word][docID])
            return counter
        else:
            print('Word "{}" is not in the collection!'.format(word))
        
    def df(self, word):
        if self.com_dict.get(word, None) != None:
            return len(self.com_dict[word].keys())
        else:
            print('Word "{}" is not in the collection!'.format(word))

    def tf(self, word, docID):
        if self.com_dict.get(word, None) != None:
            if docID in self.com_dict[word]:
                return len(self.com_dict[word][docID])
            else:
                print('Word "{}" is not in the doc # {}'.format(word, docID))
        else:
            print('Word "{}" is not in the collection!'.format(word))

    def idf(self, word):
        df = self.df(word)
        if type(df) == int:
            idf = math.log10(self.N/df)
            return idf
        else:
            return df

    def tf_idf(self, word, docID):
        tf = self.tf(word, docID)
        if type(tf) != int:
            return tf
        else:
            return tf*self.idf(word)

    def print_tf_idf_for_act(self, act_num, print_q):
        act = self.store[act_num]
        s_act = set(act)
        holder = []
        for word in s_act:
            holder.append((word, self.tf_idf(word, act_num)))
        s_holder = sorted(holder, key=lambda x: x[1], reverse=True)
        for i in range(print_q):
            print(s_holder[i])


####################################
####################################
    def demands_separation(self, border_list):
        re_object = re.compile(self.patterm_demd_sep)
        for i in range(border_list[0], border_list[1], 1):
            match = re_object.search(self.store[i])
            if match:
                self.demand_store.append(match.group(0))
        print('Demands\' search is completed. '+
              '{} demands are found. '.format(len(self.demand_store)))
        return self.demand_store

    def other_parts(self, border_list, par_num):
        holder = []
        for i in self.store[slice(border_list[0],border_list[1])]:
            i = i.split('\n')
            try:
                holder.append(i[par_num])
            except IndexError:
                pass
        print ('{} parts were extracted'.format(len(holder)))
        return holder

class TxtPars():
    def __init__(self, border_list=[0, 1974]):
        self.demands = [i.lower()
                        for i
                        in ActSep().demands_separation(border_list)]
        print(len(self.demands))
        self.dem_sep = []
        self.max_length = None
        #print(self.max_length)
        self.voc = self.indexation()
        print(len(self.voc))
    
    def unite_list(self):
        print('unification started')
        holder = []
        counter = 1
        for demand in self.demands:
            if (counter % 100) == 0:
                print (counter, end=', ')
            splitted = [word.strip('.?!,:;-()\'\"') for  word in demand.split()]
            holder.extend(splitted)
            counter+=1
            self.dem_sep.append(splitted)
        self.max_length = max(len(i) for  i in self.dem_sep)
        print('\nMax length: '+str(self.max_length))
        return set(holder)

    def indexation(self):
        print('indexation started')
        return [[i,0] for i in sorted(self.unite_list())]

    def tree_constr(self):
        print('tree_constr started')
        holder = []
        val = None
        matrix = [{} for i in range(self.max_length)]
        for demand in self.dem_sep:
            for i in range(self.max_length):
                try:
                    demand[i]
                    val = demand[i]
                except:
                    continue
                if matrix[i].get(val):
                    matrix[i][val]+=1
                else:
                    matrix[i][val] = 1
        return matrix
