import cd_processing.textextrconst as tec
import datetime as dt
import pymorphy2
import re
import sys
import _thread as thread
import tkinter as tk
from tkinter import ttk
import writer as w

pattern_clean = r'-{66}\nКонсультантПлюс.+?-{66}\n'
pattern_sep = r'\n\n\n-{66}\n\n\n'

my_path = r'C:\Python34\1974 Acts.txt'
#OR r'C:\Python35\PROJECTS\Суды по поставке 20161219.txt'

morph = pymorphy2.MorphAnalyzer()
parser = morph.parse

lock = thread.allocate_lock()

class TextProcessor():
    def __init__(self,
                 my_path=my_path,
                 pattern_clean=pattern_clean,
                 pattern_demd_sep = tec.demand_find_pattern,
                 pattern_sep=pattern_sep):
        self.cleaned = ''
        self.demand_store = {}
        self.paragraph_holder = {}
        self.path = my_path
        self.pattern_clean = pattern_clean
        self.patterm_demd_sep = pattern_demd_sep
        self.pattern_sep = pattern_sep
        self.store = []
        self.sys_messages=[]

    def text_clean(self):
        with lock:
            with open(self.path) as file:
                text = file.read()[1:-71]
            self.cleaned = re.subn(self.pattern_clean,
                                   repl='',
                                   string=text,
                                   flags=re.DOTALL)[0]
            self.system_message('Text is cleaned. {} file was used.'.format(self.path))

    def acts_separation(self):
        with lock:
            self.store = re.split(self.pattern_sep, string=self.cleaned)[:1000]#####
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
        self.system_message('Demands search is completed. '
                            + '{} demands are found. '.format(len(self.demand_store), unfound_demd_str)
                            + 'Demands were not found in:\n{}')

    def system_message(self, message):
        self.sys_messages += [str(dt.datetime.now())[:-7]
                              + ('.'*6)
                              + message
                              + '\n']


class DocumentIndexing(TextProcessor):
    def __init__(self, *args, **kwargs):
        TextProcessor.__init__(self, *args, **kwargs)
        self.doc_set = []
        self.index_store_docs = {}
        self.index_store = {}
        self.keys = None
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
        
    def index_creation(self):
        with lock:
            acts_num = len(self.store)
            lower_case = '\n\n'.join(self.store).lower()
            keys = [word.strip('.,-:;!?()\'\"') for word in lower_case.split()]
            keys = set(keys)
            keys.discard('')
            self.keys = sorted(keys)
            self.index_store = {key: {'freq_total_acts': 0, 'freq_total_pars' : 0} for key in self.keys}
            self.index_store_docs = self.index_store.copy()
            self.system_message('Index dictionary is created. {} keys was used.'.format(len(self.keys)))

    def text_indexing_docs_and_pars(self):
        with lock:
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

    def text_indexing_docs(self):
        with lock:
            holder_set=[]
            holder_all = [act.split()
                      for act in self.lowcase_store]
            length = len(holder_all)
            for i in range(length):
                holder_all[i] = [word.strip('.,-:;!?()\'\"')
                             for word in holder_all[i]]
                holder_set.append(set(holder_all[i]))
            self.doc_set = holder_set
            for key in self.keys:
                self.index_store_docs[key]['entrances'] = {i:0 for i in range(length)
                                                           if key in self.doc_set[i]}
                for item in self.index_store_docs[key]['entrances'].keys():
                    self.index_store_docs[key]['entrances'][item] = holder_all[item].count(key)
            for key in self.keys:
                self.index_store_docs[key]['freq_total_acts'] = len(self.index_store_docs[key]['entrances'])
            self.lowcase_store = None


class SearchEngine(DocumentIndexing):
    def __init__(self, *args, **kwargs):
        DocumentIndexing.__init__(self, *args, **kwargs)

    def custom_search(self, words):
        with lock:
            words_len = len(words)
            occurences_holder = []
            act_par_pairs = []
            search_results = []
            string_results = ''
            for word in words:
                occurences_holder.append(self.index_store[word]['freq_total_acts']
                                         *self.index_store[word]['freq_total_pars'])
            print(occurences_holder)
            print(min(occurences_holder))
            right_word = words[occurences_holder.index(min(occurences_holder))]
            right_acts = list(self.index_store[right_word].keys())
            for word in words:
                for act in right_acts:
                    if ((type(act) == int)
                        and self.index_store[word].get(act)):
                        for par in self.index_store[word][act]:
                            act_par_pairs.append((act, par))
            search_results = [i for i in act_par_pairs
                              if act_par_pairs.count(i) == words_len]
            search_results = sorted(set(search_results))
            for i in search_results:
                act, par = i
                string_results += (self.paragraph_holder[act][par]
                                   +'\nАкт № {0}, абзац № {1}'.format(act+1, par)
                                   +'\n\n')
            acts_quant = len(set([i for  i,j in search_results]))
        return string_results, acts_quant


class ComparisonEngin():
    def __init__(self):
        self.ce_holder=''

    def common_words_finding(self, strings):
        with lock:
            store = []
            for i in strings:
                split = i.split()
                clean = [word.strip('.?!,:;-()\'\"') for word in split]
                norm = [parser(word)[0][2] for word in clean]
                store.append(set(norm))
            holder = set(store[0]).intersection(*store[1:])
            result = ' '.join(holder)
        return result
                            

class WidgetGenerator(SearchEngine, ComparisonEngin, tk.Tk):
    def __init__(self, *args, **kwargs):
        SearchEngine.__init__(self, *args, **kwargs)
        ComparisonEngin.__init__(self)
        tk.Tk.__init__(self, *args, **kwargs)
        self.tech_print_flag = 0
        self.tk_act_index = 0
        self.tk_demd_index = 0
        self.contxt = None # Console text widget
        self.txt = None # Main text widget
        self.bottomtext = None # Information text widget at the bottom of the GUI
        self.notebook = None
        left_b_buttons = [['Clean the text', lambda: thread.start_new_thread(self.wg_text_clean, ())], #threaded
                          ['Separate acts', lambda: thread.start_new_thread(self.wg_acts_separation, ())], #threaded
                          ['Create index', lambda: thread.start_new_thread(self.wg_index_creation, ())], #threaded
                          ['Fill index', lambda: thread.start_new_thread(self.index_construction, ())], #threaded
                          ['Find demands', self.wg_demands_separation],
                          ['Insert tabs', self.tab_insert],
                          ['Find common\nwords', lambda: thread.start_new_thread(self.wg_common_words_finding, ())], #threaded
                          ['Delete text', lambda: self.deletion('main_window')]]
        self.left_bar_buttons = {key:lst for key,lst
                                 in zip(range(len(left_b_buttons)), left_b_buttons)}
        cons_buttons = [['Use custom\nfile adress', self.adress_get],
                        ['Execute', self.console_commands],
                        ['Search words', lambda: thread.start_new_thread(self.wg_custom_search, ())], #threaded
                        ['Write to file', self.write_to_file],
                        ['Delete text', lambda: self.deletion('console')]]
        self.console_buttons = {key:lst for key,lst
                                in zip(range(len(cons_buttons)), cons_buttons)}
        radio_values = [['Indexing: pars', 'pars'],
                        ['Indexing: docs', 'docs']]
        self.radiobuttons_values = {key:lst for key,lst
                                    in zip(range(len(radio_values)), radio_values)}
        self.commands_for_writing = {
            'index_store' : (lambda: self.index_store),
            'index_store_docs' : (lambda: self.index_store_docs),
            'index_store_items' : (lambda: self.index_store.items()),
            'index_store_docs_items' : (lambda: self.index_store_docs.items()),
            'par_hold' : (lambda: self.paragraph_holder()),
            'par_hold_keys' : (lambda:self.paragraph_holder.keys()),
            'sys_mesg' : (lambda: self.sys_messages),
            'simple_write' : (lambda: self.txt.get(index1='1.0', index2='end'))
            }
        self.commands_for_console = {
            'index_store_key_values' : (lambda x: self.index_store.get(x)),
            'print_tk_var' : (lambda: None),
            'size_of_index_store' : (lambda: sys.getsizeof(self.index_store)),
            'size_of_store' : (lambda: sys.getsizeof(self.store)),
            'size_of_par_holder' : (lambda: sys.getsizeof(self.paragraph_holder))
            }
        self.tk_var = tk.StringVar()
        self.make_widgets()

    def make_text_with_scroll(self, parent=None, widget_height=None,
                              widget_side='left', widget_expand='yes',
                              widget_fill='both', scroll_side='right',
                              scroll_fill='y'):
        scroll_bar = tk.Scrollbar(master=parent)
        if widget_height:
            widget_var = tk.Text(master=parent, height=widget_height)
        else:
            widget_var = tk.Text(master=parent)        
        scroll_bar.config(command=widget_var.yview)
        widget_var.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=scroll_side, fill=scroll_fill)
        widget_var.pack(side=widget_side, expand=widget_expand, fill=widget_fill)
        return widget_var
        
                                
    def make_buttons(self, parent=None, button_text_command_dict=None,
                     height=1, width=None, side='top', anchor='w'):
        for i in sorted(button_text_command_dict):
            text, command = button_text_command_dict[i]
            if width:
                tk.Button(master=parent,
                          text=text,
                          command=command,
                          height=height if len(text) < 15 else 2,
                          width=width).pack(side=side, anchor=anchor)
            else:
                tk.Button(master=parent,
                          text=text,
                          command=command,
                          height=height if len(text) < 15 else 2).pack(side=side,
                                                                       expand='yes',
                                                                       fill='x',
                                                                       anchor=anchor)

    def make_listbox(self, parent=None, action_argument=None,
                     binded_function=None, listbox_width=27):
        scroll = tk.Scrollbar(master=parent)
        listbox = tk.Listbox(master=parent, width=listbox_width)
        scroll.config(command=listbox.yview)
        listbox.config(yscrollcommand=scroll.set)
        listbox.bind(action_argument, binded_function)
        scroll.pack(side='right', fill='y')
        listbox.pack(side='left', expand='yes', fill='both')
        return listbox

    def make_radiobuttons(self, parent=None,
                          values_dict=None):
        for i in range(len(values_dict)):
            tk.Radiobutton(master=parent, text=values_dict[i][0],
                           variable=self.tk_var,
                           value=values_dict[i][1]).pack(anchor='nw')
        

    def make_widgets(self):
        buffer = tk.Frame(self)
        
        mainframe = tk.Frame(buffer, relief='sunken', bd=1)
        
        center = tk.Frame(mainframe)
        center_top = tk.Frame(center, relief='raised', bd=1)
        center_top_label_holder = tk.Frame(center_top)
        center_top_constext_container = tk.Frame(center_top)
        center_top_cons_buttons_container = tk.Frame(center_top)
        center_maintext_container = tk.Frame(center)
        
        rightBar = tk.Frame(mainframe)
        rightBar_top = tk.Frame(rightBar)
        rightBar_bottom = tk.Frame(rightBar)
        rightBarTop_label_holder = tk.Frame(rightBar_top)
        rightBarTop_listbox_container = tk.Frame(rightBar_top)
        rightBarBottom_label_holder = tk.Frame(rightBar_bottom)
        rightBarBottom_listbox_container = tk.Frame(rightBar_bottom)
        
        leftBar = tk.Frame(mainframe, relief='solid', bd=1)
        leftBar_buttons_container = tk.Frame(leftBar)
        leftBar_notebook_container = tk.Frame(leftBar)
        
        bottomframe = tk.Frame(buffer, relief='sunken', bd=1)
        bottomframe_label_holder = tk.Frame(bottomframe)
        bottomframe_inftext_container = tk.Frame(bottomframe)
        bottomframe_progress_bar = tk.Frame(bottomframe)

        ######## Frame packing
        buffer.pack(side='top', expand='yes', fill='both')
        
        mainframe.pack(side='top', expand='yes', fill='both', padx=1, pady=1)
        
        rightBar.pack(side='right', fill='y', padx=3, pady=3)
        rightBar_top.pack(side='top', expand='yes', fill='y')
        rightBar_bottom.pack(side='bottom', expand='yes', fill='y')
        rightBarTop_label_holder.pack(side='top', expand='no', fill='x')
        rightBarTop_listbox_container.pack(side='bottom', expand='yes', fill='y')
        rightBarBottom_label_holder.pack(side='top', expand='no', fill='x')
        rightBarBottom_listbox_container.pack(side='bottom', expand='yes', fill='y')
        
        leftBar.pack(side='left', fill='y', padx=3, pady=3)
        leftBar_buttons_container.pack(side='top', fill='y', pady=3)
        leftBar_notebook_container.pack(side='bottom', expand='no', fill='y', padx=3, pady=3)
        
        center.pack(side='top', expand='yes', fill='both', padx=6, pady=3)
        center_top.pack(side='top', expand='no', fill='x', padx=0, pady=3)
        center_top_label_holder.pack(side='top', fill='x', padx=3, pady=0)
        center_top_cons_buttons_container.pack(side='top', fill='x', padx=3, pady=1)
        center_top_constext_container.pack(side='bottom', fill='x', padx=3, pady=3)
        center_maintext_container.pack(side='top', expand='yes', fill='both')
        
        bottomframe.pack(side='bottom', fill='x', padx=1, pady=1)
        bottomframe_label_holder.pack(side='top', fill='x', padx=3)
        bottomframe_inftext_container.pack(side='top', fill='x', padx=3)
        bottomframe_progress_bar.pack(side='bottom', fill='x', padx=3, pady=6)

        ######## Console window creation
        tk.Label(center_top_label_holder, text='Консоль:').pack(side='left')
        self.contxt = self.make_text_with_scroll(parent=center_top_constext_container,
                                                 widget_height=4)

        ######## Main Textx Widget creation
        self.txt = self.make_text_with_scroll(parent=center_maintext_container)

        ######## Information Text Widget creation
        tk.Label(bottomframe_label_holder, text='Окно информации:').pack(side='left')
        self.bottomtext = self.make_text_with_scroll(parent=bottomframe_inftext_container,
                                                     widget_height=5)
        ######## ProgressBar creation
        self.progress = ttk.Progressbar(master=bottomframe_progress_bar,
                                           orient='horizontal',
                                           length=200,
                                           mode='determinate')
        self.progress.pack(side='left')

        ######## Listbox for Acts making
        tk.Label(rightBarTop_label_holder, text='Судебные акты:').pack(side='left')
        self.lstbox = self.make_listbox(parent=rightBarTop_listbox_container,
                                        action_argument='<Double-1>',
                                        binded_function=self.acts_extract)

        ######## Listbox for Demands packing
        tk.Label(rightBarBottom_label_holder, text='Требования:').pack(side='left')
        self.demdlstbox = self.make_listbox(parent=rightBarBottom_listbox_container,
                                        action_argument='<Double-1>',
                                        binded_function=self.demands_extract)

        ######## Buttons creation
        self.make_buttons(parent=leftBar_buttons_container,
                          button_text_command_dict=self.left_bar_buttons,
                          width=13)
        self.make_buttons(parent=center_top_cons_buttons_container,
                          button_text_command_dict=self.console_buttons,
                          height=2,
                          width=10, side='left')

        ######## Making Notebook
        self.notebook=ttk.Notebook(master=leftBar_notebook_container)
        nbframe1 = tk.Frame(self.notebook)
        nbframe2 = tk.Frame(self.notebook)
        self.notebook.add(nbframe1, text='Index\noptions')
        self.notebook.add(nbframe2, text='Not\nready')
        self.notebook.pack(side='bottom', expand='yes', fill='y')
        self.notebook.tab(nbframe2, state='disabled')

        ######## Radiobuttons creation:
        self.make_radiobuttons(parent=nbframe1,
                               values_dict=self.radiobuttons_values)
        self.tk_var.set('pars')

        ######## Menu making
        top = tk.Menu(self)
        self.config(menu=top)
        file = tk.Menu(top, tearoff=False)
        file.add_command(label='Show all commands',
                         command=self.show_all_commands,
                         underline=0)
        file.add_command(label='Quit', command=self.destroy, underline=0)
        top.add_cascade(label='Main', menu=file, underline=0)

    def wg_text_clean(self):
        self.progress.start()
        self.text_clean()
        self.tech_inf_print()
        self.progress.stop()

    def wg_acts_separation(self):
        self.progress.start()
        self.acts_separation()
        self.tech_inf_print()
        for i in range(1, len(self.store)+1):
            self.lstbox.insert('end', i)
        self.tech_inf_print("Acts' indexing is completed.")
        self.progress.stop()

    def wg_index_creation(self):
        self.progress.start()
        self.index_creation()
        self.tech_inf_print()
        self.progress.stop()

    def index_construction(self):
        if self.tk_var.get() == 'pars':
            self.progress.start()
            self.lowering()
            self.tech_inf_print("Text is lowered")
            self.low_paragraph_separation()
            self.tech_inf_print("Paragraphs are separated. Lowered text is deleted")
            self.text_indexing_docs_and_pars()
            self.tech_inf_print("Index is constructed")
            self.progress.stop()
        elif self.tk_var.get() == 'docs':
            self.progress.start()
            self.tech_inf_print("Text indexing with docs only is used")
            self.lowering()
            self.tech_inf_print("Text is lowered")
            self.text_indexing_docs()
            self.progress.stop()

    def wg_demands_separation(self):
        self.progress.start()
        self.demands_separation()
        self.tech_inf_print()
        for i in sorted(self.demand_store.keys()):
            self.demdlstbox.insert('end', i+1)
        self.tech_inf_print("Demands' indexing is completed.")
        self.progress.stop()

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

    def wg_common_words_finding(self):
        self.progress.start()
        text = self.txt.get(index1='1.0', index2='end-1c')
        split = text.split('\n\n')[:-1]
        result = self.common_words_finding(split)
        print('THIS IS RESULT:\n', result)
        self.txt.delete(index1='1.0', index2='end')
        self.txt.insert('1.0', chars=result)
        self.progress.stop()

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
            self.bottomtext.insert('1.0',
                                   chars=' '*2 + self.sys_messages[-1]+indent)
        else:
            self.system_message(message)
            self.bottomtext.insert('1.0',
                                   chars=' '*2 + self.sys_messages[-1]+indent)

    def adress_get(self):
        text = self.contxt.get(index1='1.0', index2='end-1c')
        if text not in ['', ' ', '\n', ' \n', '\n ', ' \n ']:
            self.path = text
            self.tech_inf_print('Custom adress "{}" is used.'.format(self.path))
        else:
            self.tech_inf_print('Custom adress is not defined.')

    def console_commands(self):
        text = self.contxt.get(index1='1.0', index2='end-1c')
        if 'index_store_key_values' in text:
            command = text.split()
            results = str(self.commands_for_console[command[0]](command[1])()) + '\n\n'
            self.tech_inf_print('Index items for "{}" key are picked.'.format(command[1]))
            self.txt.insert('1.0', chars=results)
        elif ((text == 'size_of_index_store')
              or (text == 'size_of_store')
              or (text == 'size_of_par_holder')):
            self.txt.insert('1.0', chars=self.commands_for_console[text]())
            self.tech_inf_print('Measured size is "{}" (in bytes).'.format(self.commands_for_console[text]()))
        elif text == 'print_tk_var':
            print(self.tk_var.get())
        else:
            self.tech_inf_print('Incorrect "{}" command detected!'.format(text))

    def write_to_file(self):
        text = self.contxt.get(index1='1.0', index2='end')
        if text not in ['', ' ', '\n', ' \n', '\n ', ' \n ']:
            write_inf = text.split()
            self.tech_inf_print('File name "{}" is used.'.format(write_inf[1]))
            content = self.commands_for_writing[write_inf[0]]()
            w.writer(content, write_inf[1])
        else:
            self.tech_inf_print('File name is not defined.')

    def wg_custom_search(self):
        self.progress.start()
        results = ''
        text = self.contxt.get(index1='1.0', index2='end').split()
        self.tech_inf_print('The search started. "{}" search query is used.'.format(text))
        results, results_length = self.custom_search(text)
        self.tech_inf_print('The search ended. "{}" acts were found.'.format(results_length))
        self.txt.insert('1.0', chars=results)
        self.progress.stop()

    def show_all_commands(self):
        string = ('This is a list of all console and writing commands\n\n1. Console commands:\n\n'
                  + '\n'.join(('-'+word) for word in sorted(self.commands_for_console.keys())))
        string += ('\n\n2. Writing commands:\n\n'
                   + '\n'.join(('-'+word) for word in sorted(self.commands_for_writing.keys())))
        new_window = tk.Toplevel(self)
        new_window.title('All commands')
        text = self.make_text_with_scroll(parent=new_window, widget_height=None,
                                          widget_side='left', widget_expand='yes',
                                          widget_fill='both', scroll_side='right',
                                          scroll_fill='y')
        text.insert('1.0', chars=string)
                

WidgetGenerator().mainloop()
