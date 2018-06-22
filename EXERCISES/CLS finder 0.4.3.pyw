#import datetime as dt
import re
#import pymorphy2
import sys
import _thread as thread
import tkinter as tk
from tkinter import ttk

HEADERFONT = ("Verdana", 14)
SIMFONT = ("Verdana", 12, "bold")
INFOFONT = ("Verdana", 11)

#morph = pymorphy2.MorphAnalyzer()
#parser = morph.parse

#tk.Tk().selection_get(selection = "CLIPBOARD")

sys.setrecursionlimit(200000)

lock = thread.allocate_lock()

class CustomTextWidget(tk.Text):

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        #The following below code was taken from: http://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=True):
        #Apply the given tag to all text that matches the given pattern

        #If 'regexp' is set to True, pattern will be treated as a regular
        #expression according to Tcl's regular expression syntax.
        

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

class MainWin(tk.Tk):#, CustomTextWidget):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #CustomTextWidget.__init__(self, *args, **kwargs)
        self.entry_txt1 = None
        self.entry_txt2 = None
        self.output_txt1 = None
        self.output_txt2 = None
        self.text_store = {key:None for key in ['string1', 'string2', 'num_box1', 'num_box2']} #Storing all text data
        self.title("Поиск различий в текстах")
        self.tk_rb_values_comparaison = [['Поиск различий', 'diff'],
                                         ['Поиск общих слов', 'siml']]
        self.tk_rb_values_morphology = [['Учитывать морфологию', 'with_morph'],
                                        ['Не учитывать морфологию', 'without_morph']]
        self.tk_rb_var_comparaison = tk.StringVar()#Radiobutton var
        self.tk_rb_var_morphology = tk.StringVar()#Radiobutton var
        #frames initiation:start
        f_buffer = tk.Frame(master=self)
        f_radiobuttons_container = tk.Frame(master=f_buffer)
        f_radiobuttons_label = tk.Frame(master=f_radiobuttons_container)
        f_radiobuttons_box_comparasion = tk.Frame(master=f_radiobuttons_container)
        f_radiobuttons_box_morphology = tk.Frame(master=f_radiobuttons_container)
        f_first_entry_line = tk.Frame(master=f_buffer)
        f_first_entry_line_label = tk.Frame(master=f_first_entry_line)
        f_first_entry_line_text_button = tk.Frame(master=f_first_entry_line)
        f_first_entry_line_text = tk.Frame(master=f_first_entry_line_text_button)
        f_first_entry_line_button = tk.Frame(master=f_first_entry_line_text_button)
        f_second_entry_line = tk.Frame(master=f_buffer)
        f_second_entry_line_label = tk.Frame(master=f_second_entry_line)
        f_second_entry_line_text_button = tk.Frame(master=f_second_entry_line)
        f_second_entry_line_text = tk.Frame(master=f_second_entry_line_text_button)
        f_second_entry_line_button = tk.Frame(master=f_second_entry_line_text_button)
        f_information_box_container = tk.Frame(master=f_buffer)        
        f_first_output_container = tk.Frame(master=f_buffer)
        f_first_output_ocntainer_label = tk.Frame(master=f_first_output_container)
        f_first_output_container_text = tk.Frame(master=f_first_output_container)
        f_second_output_container = tk.Frame(master=f_buffer)
        f_second_output_container_label = tk.Frame(master=f_second_output_container)
        f_second_output_container_text = tk.Frame(master=f_second_output_container)      
        #frames storing
        self.frames_store = {}
        self.frames = [['buffer', {'f_object':f_buffer,
                                   'f_padx' : 3, 'f_pady' : 3}],
                       ['radiobuttons_container', {'f_object':f_radiobuttons_container, 'f_fill':'x'}],
                       ['radiobuttons_label', {'f_object':f_radiobuttons_label, 'f_fill':'x'}],
                       ['radiobuttons_box_comparasion', {'f_object':f_radiobuttons_box_comparasion, 'f_fill':'x',
                                                         'f_padx' : 3, 'f_pady' : 3}],
                       ['radiobuttons_box_morphology', {'f_object':f_radiobuttons_box_morphology, 'f_fill':'x',
                                                        'f_padx' : 3, 'f_pady' : 3}],
                       ['first_entry_line', {'f_object':f_first_entry_line, 'f_fill':'x',
                                             'f_padx' : 3, 'f_pady' : 3}],
                       ['first_entry_line_label', {'f_object':f_first_entry_line_label, 'f_fill':'x'}],
                       ['first_entry_line_text_button', {'f_object':f_first_entry_line_text_button,
                                                         'f_fill':'x'}],
                       ['first_entry_line_text', {'f_object':f_first_entry_line_text,
                                                  'f_side':'left', 'f_fill':'x'}],
                       ['first_entry_line_button', {'f_object':f_first_entry_line_button,
                                                    'f_side':'right', 'f_expand':'no', 'f_fill':'x'}],
                       ['second_entry_line', {'f_object':f_second_entry_line, 'f_fill':'x',
                                              'f_padx' : 3, 'f_pady' : 3}],
                       ['second_entry_line_label', {'f_object':f_second_entry_line_label, 'f_fill':'x'}],
                       ['second_entry_line_text_button', {'f_object':f_second_entry_line_text_button, 'f_fill':'x'}],
                       ['second_entry_line_text', {'f_object':f_second_entry_line_text,
                                                   'f_side':'left', 'f_fill':'x'}],
                       ['second_entry_line_button', {'f_object':f_second_entry_line_button,
                                                     'f_side':'right', 'f_expand':'no', 'f_fill':'x'}],
                       ['information_box_container', {'f_object':f_information_box_container, 'f_fill':'x'}],
                       ['first_output_container', {'f_object':f_first_output_container,
                                                   'f_padx' : 3, 'f_pady' : 3}],
                       ['first_output_container_label', {'f_object':f_first_output_ocntainer_label, 'f_fill':'x'}],
                       ['first_output_container_text', {'f_object':f_first_output_container_text}],
                       ['second_output_container', {'f_object':f_second_output_container,
                                                    'f_padx' : 3, 'f_pady' : 3}],
                       ['second_output_container_label', {'f_object':f_second_output_container_label,
                                                          'f_fill':'x'}],
                       ['second_output_container_text', {'f_object':f_second_output_container_text}]]
        #frames initiation:end
        self.make_widgets()

    def frame_maker(self, frames):
        frames_dict = {}
        for i in range(len(frames)):
            frames_dict[frames[i][0]] = frames[i][1]['f_object']
            frames_dict[frames[i][0]].config(relief=frames[i][1].get('f_relief', 'flat'),
                                            bd=frames[i][1].get('f_bd', 0))
            frames_dict[frames[i][0]].pack(side=frames[i][1].get('f_side', 'top'),
                                           expand=frames[i][1].get('f_expand', 'yes'),
                                           fill=frames[i][1].get('f_fill', 'both'),
                                           padx=frames[i][1].get('f_padx', 0),
                                           pady=frames[i][1].get('f_pady', 0))
        return frames_dict

    def make_text_with_scroll(self, widget=None,
                              parent=None, widget_height=None,
                              widget_side='left', widget_expand='yes',
                              widget_fill='both', scroll_side='right',
                              scroll_fill='y'):
        scroll_bar = tk.Scrollbar(master=parent)
        if widget:
            tk_object = CustomTextWidget
        else:
            tk_object = tk.Text
        if widget_height:
            widget_var = tk_object(master=parent, height=widget_height)
        else:
            widget_var = tk_object(master=parent)        
        scroll_bar.config(command=widget_var.yview)
        widget_var.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=scroll_side, fill=scroll_fill)
        widget_var.pack(side=widget_side, expand=widget_expand, fill=widget_fill)
        return widget_var

    def make_radiobuttons(self, parent=None,
                          values=None,
                          pack_side='top',
                          tk_var=None,
                          wdg_state='normal'):
        for i in range(len(values)):
            tk.Radiobutton(master=parent, text=values[i][0],
                           variable=tk_var,
                           value=values[i][1],
                           state=wdg_state).pack(side=pack_side, anchor='nw')
        tk_var.set(values[0][1])

    #def make_notebook(self, parent, pad_names=[]):
    #        notebook = ttk.Notebook(master=parent)
    #        pad_store = {i:tk.Frame(master=notebook) for i in range(len(pad_names))}
    #        for i in sorted(pad_store.keys()):
    #            notebook.add(pad_store[i], text=pad_names[i])
    #        notebook.pack(side='top', expand='yes', fill='both')
    #        return pad_store

    def make_widgets(self):
        self.frames_store = self.frame_maker(self.frames)
        self.entry_txt1 = self.make_text_with_scroll(parent=self.frames_store['first_entry_line_text'],
                                                     widget_height=4)
        self.entry_txt2 = self.make_text_with_scroll(parent=self.frames_store['second_entry_line_text'],
                                                     widget_height=4)
        self.output_txt1 = self.make_text_with_scroll(widget='custom', parent=self.frames_store['first_output_container_text'])
        self.output_txt1.tag_configure("green", background="#00ff00", overstrike=1)
        self.output_txt2 = self.make_text_with_scroll(widget='custom', parent=self.frames_store['second_output_container_text'])
        self.output_txt2.tag_configure("yellow", background="yellow")
        tk.Button(master=self.frames_store['first_entry_line_button'],
                  text='Сравнить',
                  command=lambda: thread.start_new_thread(self.LCS_main, ()),
                  height=1).pack()
        tk.Button(master=self.frames_store['second_entry_line_button'],
                  text='Очистить',
                  command=lambda: thread.start_new_thread(self.wdg_clean, ()),
                  height=1).pack()
        self.make_radiobuttons(parent=self.frames_store['radiobuttons_box_comparasion'],
                               values=self.tk_rb_values_comparaison,
                               pack_side='left',
                               tk_var=self.tk_rb_var_comparaison,
                               wdg_state='disabled')
        self.make_radiobuttons(parent=self.frames_store['radiobuttons_box_morphology'],
                               values=self.tk_rb_values_morphology,
                               pack_side='left',
                               tk_var=self.tk_rb_var_morphology,
                               wdg_state='disabled')
        self.progress = ttk.Progressbar(master=self.frames_store['information_box_container'],
                                           orient='horizontal',
                                           length=200,
                                           mode='indeterminate')
        self.progress.pack(padx=3, pady=3)
                                        

    def wdg_clean(self):
        self.entry_txt1.delete(index1='1.0', index2='end')
        self.entry_txt2.delete(index1='1.0', index2='end')
        self.output_txt1.delete(index1='1.0', index2='end')
        self.output_txt2.delete(index1='1.0', index2='end')

    def LCS_Length(self, norm_text1, norm_text2):
        m = len(norm_text1)
        n = len(norm_text2)
        c = [[0 for nn in range(n+1)] for mm in range(m+1)]
        b = [[0 for nn in range(n+1)] for mm in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if norm_text1[i-1] == norm_text2[j-1]:
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

    def return_LCS_num(self,
                       result_b_table,
                       norm_text1,
                       len_norm_text1, len_norm_text2,
                       num_box1, num_box2):
        if len_norm_text1 == 0 or len_norm_text2 == 0:
            return None
        if result_b_table[len_norm_text1][len_norm_text2] == 'DIOG':
            self.return_LCS_num(result_b_table,
                                norm_text1,
                                len_norm_text1-1, len_norm_text2-1,
                                num_box1, num_box2)
            num_box1.append(len_norm_text1-1)
            num_box2.append(len_norm_text2-1)
        elif result_b_table[len_norm_text1][len_norm_text2] == 'UP':
            self.return_LCS_num(result_b_table,
                                norm_text1,
                                len_norm_text1-1, len_norm_text2,
                                num_box1, num_box2)
        else:
            self.return_LCS_num(result_b_table,
                                norm_text1,
                                len_norm_text1, len_norm_text2-1,
                                num_box1, num_box2)

    def LCS_main(self):
        #self.lists_similarity.set('')
        #self.string_1_p.set('')
        #self.string_2_p.set('')
        #self.lenlist1.set('')
        #self.lenlist2.set('')
        #self.lenLCS.set('')
        #self.frame.text_str1.delete('1.0', 'end')
        #self.frame.text_str2.delete('1.0', 'end')

        with lock:
            self.progress.start()
            string1 = self.entry_txt1.get(index1='1.0', index2='end-1c')
            string1 = string1.replace('\n', ' replaced ')
            list1 = re.sub("[^\w]", " ", string1).lower().split()
            string2 = self.entry_txt2.get(index1='1.0', index2='end-1c')
            string2 = string2.replace('\n', ' replaced ')
            list2 = re.sub("[^\w]", " ", string2).lower().split()
            len_LCS, result_b_tab = self.LCS_Length(list1, list2)
            num_box_list1 = []
            num_box_list2 = []
            resultlist1 = []
            resultlist2 = []

            self.return_LCS_num(result_b_tab, list1, len(list1), len(list2), num_box_list1, num_box_list2)

            if len(list1) == len(list2) == len_LCS :
                self.output_txt1.insert(index='1.0', chars='Отрывки идентичны')
                #self.lists_similarity.set('Отрывки не содержат различий')
                #self.lenlist1.set('Длина первого отрывка: %d' % len(list1))
                #self.lenlist2.set('Длина второго отрывка: %d' % len(list2))
                #self.lenLCS.set('Количество схожих фрагментов: %d' % lenLCS)
            else:
                resultlist1 = list1[:]
                for i in range(len(resultlist1)):
                    if i not in num_box_list1:
                        resultlist1[i] = resultlist1[i] if resultlist1[i]=='replaced' else '*'+resultlist1[i].upper()+'*'        
                resultlist2 = list2[:]
                for i in range(len(resultlist2)):
                    if i not in num_box_list2:
                        resultlist2[i] = resultlist2[i] if resultlist2[i]=='replaced' else '*'+resultlist2[i].upper()+'*'   
                result_string1 = ' '.join(resultlist1)
                result_string1 = ' '*5 + result_string1.replace('replaced', ('\n'+' '*4))
                result_string2 = ' '.join(resultlist2)
                result_string2 = ' '*5 + result_string2.replace('replaced', ('\n'+' '*4))
                self.output_txt1.insert(index='1.0', chars=result_string1)
                self.output_txt1.highlight_pattern('\*\w+\*', 'green')
                self.output_txt2.insert(index='1.0', chars=result_string2)
                self.output_txt2.highlight_pattern('\*\w+\*', 'yellow')
                #self.lenlist1.set('Длина первого отрывка: %d' % len(resultlist1))
                #self.lenlist2.set('Длина второго отрывка: %d' % len(resultlist2))
                #self.lenLCS.set('Количество схожих фрагментов: %d' % lenLCS)
                #self.frame.text_str1.insert('1.0', self.string_1_p.get())
                #self.frame.text_str1.highlight_pattern('\*\w+\*', 'green')
                #self.frame.text_str2.insert('1.0', self.string_2_p.get())
                #self.frame.text_str2.highlight_pattern('\*\w+\*', 'yellow')   
                self.progress.stop()
            
    
MainWin().mainloop()
