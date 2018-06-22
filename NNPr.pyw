import act_sep
import vectorizer as vct
import SNN
import tkinter as tk
from tkinter import ttk

class CustomTextWidget(tk.Text):

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, wrap='word', **kwargs)
        #self.tag_configure('center', justify='left')
        #self.tag_add('center', 1.0, 'end')

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

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames_names = ['buffer', 'main_text_label_holder', 'main_label_holder',
                             'main_text_holder', 'right_buttons_label_holder', 'right_label_holder',
                             'right_buttons_holder']
        self.frames = {}
        self.frames['buffer'] = {'f_object':tk.Frame(master=self)}
        self.frames['main_text_label_holder'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                                 'f_side':'left', 'f_expand':'yes', 'f_fill':'both',
                                                 'f_padx':3, 'f_pady':3}
        self.frames['main_label_holder'] = {'f_object':tk.Frame(master=self.frames['main_text_label_holder']['f_object']),
                                            'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['main_text_holder'] = {'f_object':tk.Frame(master=self.frames['main_text_label_holder']['f_object']),
                                           'f_side':'top', 'f_expand':'yes', 'f_fill':'both'}
        self.frames['right_buttons_label_holder'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                                     'f_side':'right', 'f_expand':'no', 'f_fill':'y',
                                                     'f_padx':3, 'f_pady':3}
        self.frames['right_label_holder'] = {'f_object':tk.Frame(master=self.frames['right_buttons_label_holder']['f_object']),
                                             'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['right_buttons_holder'] = {'f_object':tk.Frame(master=self.frames['right_buttons_label_holder']['f_object']),
                                               'f_side':'top', 'f_expand':'yes', 'f_fill':'y'}
        self.right_bar_buttons = [['Добавить\nкрасную строку', lambda: self.insert_tabs()],
                                 ['Анализировать', lambda: self.analayzer()],
                                  ['Очистить', lambda: self.txt.delete(index1='1.0', index2='end')]]
        self.splitted = []
        self.txt = None
        self.make_widgets()

    def frame_maker(self, frames_dict, frames_names):
        for i in frames_names:
            frames_dict[i]['f_object'].config(relief=frames_dict[i].get('f_relief', 'flat'),
                                            bd=frames_dict[i].get('f_bd', 0))
            frames_dict[i]['f_object'].pack(side=frames_dict[i].get('f_side', 'top'),
                                           expand=frames_dict[i].get('f_expand', 'yes'),
                                           fill=frames_dict[i].get('f_fill', 'both'),
                                           padx=frames_dict[i].get('f_padx', 0),
                                           pady=frames_dict[i].get('f_pady', 0))

    def make_text_with_scroll(self, widget=None,
                              parent=None, widget_height=None,
                              widget_side='left', widget_expand='yes',
                              widget_fill='both', scroll_='yes',
                              scroll_side='right',
                              scroll_fill='y'):
        if scroll_ == 'yes':
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
        else:
            if widget:
                tk_object = CustomTextWidget
            else:
                tk_object = tk.Text
            if widget_height:
                widget_var = tk_object(master=parent, height=widget_height)
            else:
                widget_var = tk_object(master=parent)
            widget_var.pack(side=widget_side, expand=widget_expand, fill=widget_fill)
            return widget_var

    def make_buttons(self, parent=None, buttons_list=None,
                     height=1, width=None, side='top', anchor='w'):
        for i in buttons_list:
            text, command = i
            if width:
                tk.Button(master=parent,
                          text=text,
                          command=command,
                          height=height if len(text) > 13 else 2,
                          width=width).pack(side=side, anchor=anchor)
            else:
                tk.Button(master=parent,
                          text=text,
                          command=command,
                          height=height if len(text) > 13 else 2).pack(side=side,
                                                                       expand='no',
                                                                       fill='x',
                                                                       anchor=anchor)

    def custom_insert(self, event):
        self.txt.insert(index='1.0', chars=self.selection_get(selection = "CLIPBOARD"))

    def make_widgets(self):
        self.frame_maker(self.frames, self.frames_names)
        self.txt = self.make_text_with_scroll(parent = self.frames['main_text_holder']['f_object'],
                                              widget = 'cusotm')
        self.txt.tag_configure("green", background="#00ff00")
        self.txt.bind('<Control-igrave>', self.custom_insert)
        self.make_buttons(parent = self.frames['right_buttons_holder']['f_object'],
                          buttons_list = self.right_bar_buttons,
                          height = 3)

    def insert_tabs(self, mode=None):
        string = ''
        counter = 0
        if mode == None:
            text = self.txt.get(index1='1.0', index2='end-1c')
            self.txt.delete(index1='1.0', index2='end')
            splitted = text.split('\n')
        elif mode == 'analyze':
            splitted = self.splitted
        for i in range(len(splitted)):
            if splitted[i]:
                if splitted[i][0] == '<':
                    string +=  str(counter)+' - '+splitted[i]+'\n'
                else:
                    string +=  str(counter)+(' '*(6-len(str(counter))))+splitted[i]+'\n'
                counter += 1
            else:
                string += str(counter)+(' '*(6-len(str(counter))))+'\n'#' '*6+splitted[i]+'\n'
                counter += 1
        self.txt.insert('1.0', chars=string)

    def analayzer(self):
        vvec = vct.vectorizer
        #Neural Net initializing
        net = SNN.NetCnstr(21,12,2)
        net.load_weights(r'C:\Python34\Weights_store\Demands\input_to_hidden.npy', 'input_to_hidden')
        net.load_weights(r'C:\Python34\Weights_store\Demands\hidden_to_output.npy', 'hidden_to_output')
        print('Weights are loaded successfully')
        
        text = self.txt.get(index1='1.0', index2='end-1c')
        self.txt.delete(index1='1.0', index2='end-1c')
        splitted = text.split('\n')
        estimation_holder = []
        for i in splitted:
            marks = net.query(vvec(i))
            if marks[0] > marks[1]:
                estimation_holder.append(marks[0])
            else:
                estimation_holder.append(0)
        print(list(enumerate(estimation_holder)))
        result = estimation_holder.index(max(estimation_holder))
        splitted[result] = '<DEM '+ splitted[result] +' /DEM>'
        self.splitted = splitted
        self.insert_tabs(mode='analyze')
        self.txt.highlight_pattern('\<.+\>', 'green')
        

################################################################
GUI().mainloop()
