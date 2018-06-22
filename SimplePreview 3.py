import cd_processing.textextrconst as tec
import datetime as dt
import re
import tkinter as tk
import writer as w

pattern_clean = r'-{66}\nКонсультантПлюс.+?-{66}\n'
pattern_sep = r'\n\n\n-{66}\n\n\n'

my_path = r'C:\Python34\1974 Acts.txt' #r'C:\Python35\PROJECTS\Суды по поставке 20161219.txt'

class TextProcessor():
    def __init__(self,
                 my_path=my_path,
                 pattern_clean=pattern_clean,
                 pattern_demd_sep = tec.demand_find_pattern,
                 pattern_sep=pattern_sep):
        self.cleaned = ''
        self.demand_store = {}
        self.index_store = {}
        self.paragraph_holder = {}
        self.path = my_path
        self.pattern_clean = pattern_clean
        self.patterm_demd_sep = pattern_demd_sep
        self.pattern_sep = pattern_sep
        self.store = []
        self.sys_messages=[]

    def text_clean(self):
        with open(self.path) as file:
            text = file.read()[1:-71]
        self.cleaned = re.subn(self.pattern_clean,
                               repl='',
                               string=text,
                               flags=re.DOTALL)[0]
        self.system_message('Text is cleaned. {} file was used.'.format(self.path))

    def acts_separation(self):
        self.store = re.split(self.pattern_sep, string=self.cleaned)######
        acts_num = len(self.store)
        self.cleaned = None
        counter = 0
        for act in self.store:
            holder = [par for par in act.split('\n') if par != '']
            self.paragraph_holder[counter] = holder
            counter+=1
        self.system_message('Text is separated. '
                            +'There are {} acts. '.format(acts_num)
                            +'Paragrraphs are separeted. '
                            +'Cleaned text is deleted.')

    def index_creation(self):
        acts_num = len(self.store)
        lower_case = '\n\n'.join(self.store).lower()
        keys = [word.strip('.,-:;!?()\'\"') for word in lower_case.split()]
        keys = set(keys)
        keys.discard('')
        self.index_store = {key: {'freq_total_acts': 0, 'freq_total_pars' : 0} for key in keys}
        self.system_message('Index dictionary is created. {} keys was used.'.format(len(keys)))

    def demands_separation(self):
        re_object = re.compile(self.patterm_demd_sep)
        for i in range(len(self.store)):
            match = re_object.search(self.store[i])
            if match:
                self.demand_store[i]=match.group(0)
        unfound_demd = sorted(set(range(1, len(self.store)+1))
                              -
                              set([i+1 for i in self.demand_store.keys()]))
        unfound_demd_str = ', '.join([str(i) for i in unfound_demd])
        self.system_message('Demands search is completed. {} demands are found. Demands were not found in:\n{}'.format(len(self.demand_store), unfound_demd_str))

    def system_message(self, message):
        self.sys_messages += [str(dt.datetime.now())[:-7]
                              + ('.'*6)
                              + message
                              + '\n']


class DocumentIndexing(TextProcessor):
    def __init__(self, *args, **kwargs):
        TextProcessor.__init__(self, *args, **kwargs)
        self.lowcase_store = []
        self.low_paragraph_holder = {}

    def find_each_position(self, word, lst):
        store = []
        position = 0
        for item in lst:
            if item == word:
                store.append(lst.index(item, position))
                position = store[-1] + 1
        return store

    def lowering(self):
        self.lowcase_store = [i.lower() for i in self.store]######
        
    def low_paragraph_separation(self):
        counter = 0
        for act in self.lowcase_store:
            holder = [par for par in act.split('\n') if par != '']
            self.low_paragraph_holder[counter] = holder
            counter+=1
        self.lowcase_store = None

    def text_indexing(self):
        for act_num in self.low_paragraph_holder.keys():
            par_counter = 0
            for par in self.low_paragraph_holder[act_num]:
                parts = par.split()
                words = [word.strip('.,-:;!?()\'\"') for word in parts]
                set_words = set(words)
                set_words.discard('')
                for word in set_words:
                    if not self.index_store[word].get(act_num):
                        self.index_store[word][act_num] = {}
                        self.index_store[word]['freq_total_acts'] += 1
                    if not self.index_store[word][act_num].get(par_counter):
                        self.index_store[word][act_num][par_counter] = []
                        self.index_store[word][act_num][par_counter].extend(self.find_each_position(word, words))
                        self.index_store[word]['freq_total_pars'] += len(self.index_store[word][act_num][par_counter])
                    else:
                        self.index_store[word][act_num][par_counter].extend(self.find_each_position(word, words))
                        self.index_store[word]['freq_total_pars'] += len(self.index_store[word][act_num][par_counter])
                par_counter+=1
        self.low_paragraph_holder = None


class SearchEngine(DocumentIndexing):
    def __init__(self, *args, **kwargs):
        DocumentIndexing.__init__(self, *args, **kwargs)

    def custom_search(self, words):
        words_len = len(words)
        occurences_holder = []
        act_par_pairs = []
        search_results = []
        string_results = ''
        for word in words:
            occurences_holder.append(self.index_store[word]['freq_total_acts']*self.index_store[word]['freq_total_pars'])
        print(occurences_holder)
        print(min(occurences_holder))
        right_word = words[occurences_holder.index(min(occurences_holder))]
        right_acts = list(self.index_store[right_word].keys())
        for word in words:
            #acts_store = list(self.index_store[i].keys())
            for act in right_acts:
                if (act != 'freq_total_acts') and act != 'freq_total_pars':
                #par_store = list(self.index_store[i][j].keys())
                    for par in self.index_store[word][act]:
                        act_par_pairs.append((act, par))
        for i in act_par_pairs:
            if act_par_pairs.count(i) == words_len:
                search_results.append(i)
        search_results = sorted(set(search_results))
        for i in search_results:
            act, par = i
            string_results += (self.paragraph_holder[act][par]
                               +'\nАкт № {0}, абзац № {1}'.format(act+1, par)
                               +'\n\n')
        acts_quant = len(set([i for  i,j in search_results]))
        return string_results, acts_quant
                            

class WidgetGenerator(SearchEngine, tk.Frame):
    def __init__(self, *args, **kwargs):
        SearchEngine.__init__(self, *args, **kwargs)
        tk.Frame.__init__(self, *args, **kwargs)
        
        self.pack(expand='yes', fill='both')
        self.makewidgets()

        self.tech_print_flag = 0
        self.tk_act_index = 0
        self.tk_demd_index = 0
        

    def makewidgets(self):
        mainframe = tk.Frame(self)
        center = tk.Frame(mainframe)
        topcenter = tk.Frame(center)
        label_topcenter = tk.Frame(topcenter)
        top_topcenter = tk.Frame(topcenter)
        bottom_topcenter = tk.Frame(topcenter)
        
        bottomcenter = tk.Frame(center)
        
        rightBar = tk.Frame(mainframe)
        rightBarTop = tk.Frame(rightBar)
        rightBarTop_container = tk.Frame(rightBarTop)
        rightBarBottom = tk.Frame(rightBar)
        rightBarBottom_container = tk.Frame(rightBarBottom)
        
        leftBar = tk.Frame(mainframe)
        
        bottomframe = tk.Frame(self)
        bottomframe_container = tk.Frame(bottomframe)
        
        #### Left menu window
        button_pickadress = tk.Button(bottom_topcenter,
                                      text='Use custom\nfile adress',
                                      command=self.adress_get,
                                      height=2,
                                      width=10)
        button_consolecommands = tk.Button(bottom_topcenter,
                                      text='Enter\ncommand',
                                      command=self.console_commands,
                                      height=2,
                                      width=10)
        button_customsearch = tk.Button(bottom_topcenter,
                                      text='Search words',
                                      command=self.wg_custom_search,
                                      height=2,
                                      width=10)
        button_write = tk.Button(bottom_topcenter,
                                      text='Write to file',
                                      command=self.write_to_file,
                                      height=2,
                                      width=10)
        button_con_del = tk.Button(bottom_topcenter,
                                   text='Delete text',
                                   command=lambda: self.deletion('console'),
                                   height=2,
                                   width=10)
        button_txtclean = tk.Button(leftBar,
                                    text='Clean the text',
                                    command=self.wg_text_clean,
                                    width=13)
        button_txtsep = tk.Button(leftBar,
                                  text='Separate acts',
                                  command=self.wg_acts_separation,
                                  width=13)
        button_indexcreate = tk.Button(leftBar,
                                       text='Create index',
                                       command=self.wg_index_creation,
                                       width=13)
        button_indexconstr = tk.Button(leftBar,
                                       text='Fill index',
                                       command=self.index_construction,
                                       width=13)
        button_demsep = tk.Button(leftBar,
                                  text='Find demands',
                                  command=self.wg_demands_separation,
                                  width=13)
        button_tabinsert = tk.Button(leftBar,
                                     text="Insert tabs\nto acts's text",
                                     command=self.tab_insert,
                                     width=13)
        buttoon_delete = tk.Button(leftBar,
                                   text='Delete text',
                                   command=lambda: self.deletion('main_window'),
                                   width=13)
        
        #### Text window
        txtSbar = tk.Scrollbar(bottomcenter)
        self.txt = tk.Text(bottomcenter)
        txtSbar.config(command=self.txt.yview)
        self.txt.config(yscrollcommand=txtSbar.set)
        
        #### ListBox window for Acts
        lstbox_label = tk.Label(rightBarTop, text='Судебные акты:')
        lstSbar = tk.Scrollbar(rightBarTop_container)
        self.lstbox = tk.Listbox(rightBarTop_container, width=27)
        lstSbar.config(command=self.lstbox.yview)
        self.lstbox.config(yscrollcommand=lstSbar.set)
        self.lstbox.bind('<Double-1>', self.acts_extract)

        #### ListBox window for Demands
        demdlstbox_label = tk.Label(rightBarBottom, text='Требования:')
        demdlstSbar = tk.Scrollbar(rightBarBottom_container)
        self.demdlstbox = tk.Listbox(rightBarBottom_container, width=27)
        demdlstSbar.config(command=self.demdlstbox.yview)
        self.demdlstbox.config(yscrollcommand=demdlstSbar.set)
        self.demdlstbox.bind('<Double-1>', self.demands_extract)

        #### Bottom information Text window
        bottomlabel = tk.Label(bottomframe, text='Окно информации:')
        blSbar = tk.Scrollbar(bottomframe_container)
        self.bottomtext = tk.Text(bottomframe_container, height=4)
        blSbar.config(command=self.bottomtext.yview)
        self.bottomtext.config(yscrollcommand=blSbar.set)

        #### Console window
        conlabel = tk.Label(label_topcenter, text='Консоль:')
        conSbar = tk.Scrollbar(top_topcenter)
        self.contxt = tk.Text(top_topcenter, height=3)
        conSbar.config(command=self.contxt.yview)
        self.contxt.config(yscrollcommand=conSbar.set)

        #### Packing
        ######## Frame packing
        mainframe.pack(side='top', expand='yes', fill='both', padx=5, pady=5)
        
        rightBar.pack(side='right', fill='y')
        rightBarTop.pack(side='top', expand='yes', fill='y', padx=3, pady=6)
        rightBarTop_container.pack(side='bottom', expand='yes', fill='y')
        rightBarBottom.pack(side='bottom', expand='yes', fill='y', padx=3, pady=6)
        rightBarBottom_container.pack(side='bottom', expand='yes', fill='y')
        
        leftBar.pack(side='left', fill='y', padx=3, pady=3)
        
        center.pack(side='top', expand='yes', fill='both')
        topcenter.pack(side='top', expand='no', fill='x', padx=3, pady=6)
        label_topcenter.pack(side='top', fill='x')
        top_topcenter.pack(side='top', fill='x')
        bottom_topcenter.pack(side='bottom', fill='x', pady=1)
        
        bottomcenter.pack(side='top', expand='yes', fill='both', padx=3, pady=6)
        
        bottomframe.pack(side='bottom', fill='x', padx=8, pady=11)
        bottomframe_container.pack(side='bottom', fill='x')

        ######## Console window packing
        conlabel.pack(side='left')
        conSbar.pack(side='right', fill='y')
        self.contxt.pack(side='left', expand='yes', fill='x')

        ######## Main Textx Widget packing
        txtSbar.pack(side='right', fill='y')
        self.txt.pack(side='left', expand='yes', fill='both')

        ######## Listbox for Acts packing
        lstbox_label.pack(side='left')
        lstSbar.pack(side='right', fill='y')
        self.lstbox.pack(side='left', expand='yes', fill='both')

        ######## Listbox for Demands packing
        demdlstbox_label.pack(side='left')
        demdlstSbar.pack(side='right', fill='y')
        self.demdlstbox.pack(side='left', expand='yes', fill='both')

        ######## Buttons packing
        button_pickadress.pack(side='left', anchor='w')
        button_consolecommands.pack(side='left', anchor='w')
        button_customsearch.pack(side='left', anchor='w')
        button_write.pack(side='left', anchor='w')
        button_con_del.pack(side='left', anchor='w')
        button_txtclean.pack(anchor='w')
        button_txtsep.pack(anchor='w')
        button_indexcreate.pack(anchor='w')
        button_indexconstr.pack(anchor='w')
        button_demsep.pack(anchor='w')
        button_tabinsert.pack(anchor='w')
        buttoon_delete.pack(anchor='w')

        ######## Bottom Text Widget packing
        bottomlabel.pack(side='left')
        blSbar.pack(side='right', fill='y')
        self.bottomtext.pack(expand='yes', fill='x')

    def wg_text_clean(self):
        self.text_clean()
        self.tech_inf_print()

    def wg_index_creation(self):
        self.index_creation()
        self.tech_inf_print()
        
    def index_construction(self):
        self.lowering()
        self.tech_inf_print("Text is lowered")
        self.low_paragraph_separation()
        self.tech_inf_print("Paragraphs are separated. Lowered text is deleted")
        self.text_indexing()
        self.tech_inf_print("Index is constructed")

    def wg_acts_separation(self):
        self.acts_separation()
        self.tech_inf_print()
        for i in range(1, len(self.store)+1):
            self.lstbox.insert('end', i)
        self.tech_inf_print("Acts' indexing is completed.")

    def wg_demands_separation(self):
        self.demands_separation()
        self.tech_inf_print()
        for i in sorted(self.demand_store.keys()):
            self.demdlstbox.insert('end', i+1)
        self.tech_inf_print("Demands' indexing is completed.")

    def acts_extract(self, event):
        selection = self.lstbox.curselection()
        self.tk_act_index = int(self.lstbox.get(selection))
        self.txt.insert('1.0', chars=self.store[self.tk_act_index-1]+'\n\n')
        self.tech_inf_print('Act № {} is picked.'.format(self.tk_act_index))

    def demands_extract(self, event):
        selection = self.demdlstbox.curselection()
        self.tk_demd_index = int(self.demdlstbox.get(selection))
        self.txt.insert('1.0', chars=self.demand_store[self.tk_demd_index-1]+'\n\n')
        self.tech_inf_print("Act № {}: demand is picked.".format(self.tk_demd_index))

    def tab_insert(self):
        text = ''
        counter = 0
        self.txt.delete(index1='1.0', index2='end')
        splitted = self.store[self.tk_act_index-1].split('\n')
        for i in range(len(splitted)):
            if splitted[i]:
                text +=  str(counter)+'\t'+splitted[i]+'\n'
                counter += 1
            else:
                text += '\t'+splitted[i]+'\n'
        self.txt.insert('1.0', chars=text)
        self.tech_inf_print('Tabs are inserted.')

    def deletion(self, place):
        if place == 'main_window':
            self.txt.delete(index1='1.0', index2='end')
            self.tech_inf_print('Main Window: text was deleted.')
        if place == 'console':
            self.contxt.delete(index1='1.0', index2='end')
            self.tech_inf_print('Console: text was deleted.')

    def tech_inf_print(self, message=False):
        indent = '-'*5 if self.tech_print_flag != False else ''
        self.tech_print_flag = True
        if message == False:
            self.bottomtext.insert('1.0', chars=' '*2 + self.sys_messages[-1]+indent)
        else:
            self.system_message(message)
            self.bottomtext.insert('1.0', chars=' '*2 + self.sys_messages[-1]+indent)

    def adress_get(self):
        text = self.contxt.get(index1='1.0', index2='end')
        if text not in ['', ' ', '\n', ' \n', '\n ', ' \n ']:
            self.path = self.contxt.get(index1='1.0', index2='end-1c')
            self.tech_inf_print('Custom adress "{}" is used.'.format(self.path))
        else:
            self.tech_inf_print('Custom adress is not defined.')

    def console_commands(self):
        store = {
            'index_store_key_values' : self.index_store.get
            }
        text = self.contxt.get(index1='1.0', index2='end')
        if text not in ['', ' ', '\n', ' \n', '\n ', ' \n ']:
            command = text.split()
            results = str(store[command[0]](command[1])) + '\n\n'
            self.tech_inf_print('Index items for "{}" key are picked.'.format(command[1]))
            self.txt.insert('1.0', chars=results)
        else:
            self.tech_inf_print('Incorrect "{}" command detected!'.format(text))

    def write_to_file(self):
        store = {
            'index_store' : self.index_store,
            'index_store_items' : self.index_store.items(),
            'par_hold' : self.paragraph_holder,
            'par_hold_items' : self.paragraph_holder.items(),
            'sys_mesg' : self.sys_messages
            }
        text = self.contxt.get(index1='1.0', index2='end')
        if text not in ['', ' ', '\n', ' \n', '\n ', ' \n ']:
            write_inf = text.split()
            self.tech_inf_print('File name "{}" is used.'.format(write_inf[1]))
            w.writer(store[write_inf[0]], write_inf[1])
        else:
            self.tech_inf_print('File name is not defined.')

    def wg_custom_search(self):
        results = ''
        text = self.contxt.get(index1='1.0', index2='end').split()
        self.tech_inf_print('The search started. "{}" search query is used.'.format(text))
        results, results_length = self.custom_search(text)
        self.tech_inf_print('The search ended. "{}" acts was found.'.format(results_length))
        self.txt.insert('1.0', chars=results)
        

WidgetGenerator().mainloop()
