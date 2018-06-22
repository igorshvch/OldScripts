import datetime as dt
import re
import tkinter as tk

pattern_clean = r'-{66}\nКонсультантПлюс.+?-{66}\n'
pattern_sep = r'\n\n\n-{66}\n\n\n'

my_path = r'C:\Python34\1974 Acts.txt'

class Main(tk.Frame):
    def __init__(self, my_path=my_path, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pack(expand='yes', fill='both')
        self.makewidgets()
        self.path=my_path
        self.store=[]
        self.index=0

    def makewidgets(self):
        mainframe = tk.Frame(self)
        center = tk.Frame(mainframe)
        rightBar = tk.Frame(mainframe)
        leftBar = tk.Frame(mainframe)
        bottomframe = tk.Frame(self)
        
        #### Left menu window
        button_txtclean = tk.Button(leftBar,
                                    text='Clean the text',
                                    command=self.text_clean,
                                    width=13)
        button_txtsep = tk.Button(leftBar,
                                  text='Separate acts',
                                  command=self.acts_separation,
                                  width=13)
        button_tabinsert = tk.Button(leftBar,
                                     text='Insert tabs',
                                     command=self.tab_insert,
                                     width=13)
        buttoon_delete = tk.Button(leftBar,
                                   text='Delete text',
                                   command=self.deletion,
                                   width=13)
        
        #### Text window
        txtSbar = tk.Scrollbar(center)
        self.txt = tk.Text(center)
        txtSbar.config(command=self.txt.yview)
        self.txt.config(yscrollcommand=txtSbar.set)
        
        #### ListBox window
        lstSbar = tk.Scrollbar(rightBar)
        self.lstbox = tk.Listbox(rightBar)
        lstSbar.config(command=self.lstbox.yview)
        self.lstbox.config(yscrollcommand=lstSbar.set)
        self.lstbox.bind('<Double-1>', self.acts_extract)

        #### Bottom information Text window
        blSbar = tk.Scrollbar(bottomframe)
        self.bottomtext = tk.Text(bottomframe, height=4)
        blSbar.config(command=self.bottomtext.yview)
        self.bottomtext.config(yscrollcommand=blSbar.set)

        #### Packing
        ######## Frame packing
        mainframe.pack(side='top', expand='yes', fill='both')
        rightBar.pack(side='right', fill='y', padx=3, pady=3)
        leftBar.pack(side='left', fill='y', padx=3, pady=3)
        center.pack(side='top', expand='yes', fill='both', padx=3, pady=3)
        bottomframe.pack(side='bottom', fill='x', padx=3, pady=3)

        ######## Main Textx Widget packing
        txtSbar.pack(side='right', fill='y')
        self.txt.pack(side='left', expand='yes', fill='both')

        ######## Listbox packing
        lstSbar.pack(side='right', fill='y')
        self.lstbox.pack(side='left', expand='yes', fill='both')

        ######## Buttons packing
        button_txtclean.pack(anchor='w')
        button_txtsep.pack(anchor='w')
        button_tabinsert.pack(anchor='w')
        buttoon_delete.pack(anchor='w')

        ######## Bottom Text Widget packing
        blSbar.pack(side='right', fill='y')
        self.bottomtext.pack(expand='yes', fill='x')

    def acts_extract(self, event):
        selection = self.lstbox.curselection()
        self.index = int(self.lstbox.get(selection))
        self.txt.insert('1.0', chars=self.store[self.index-1])
        self.tech_inf_print('Act № {} is picked'.format(self.index))

    def text_clean(self):
        with open(self.path) as file:
            text = file.read()[1:-71]
        self.cleaned = re.subn(pattern_clean, repl='', string=text, flags=re.DOTALL)[0]
        self.tech_inf_print('Text is cleaned')

    def acts_separation(self):
        self.store = re.split(pattern_sep, string=self.cleaned)
        acts_num = len(self.store)
        self.tech_inf_print('Text is separated')
        self.tech_inf_print('There are {} acts'.format(acts_num))
        del self.cleaned
        self.tech_inf_print('Cleaned text is deleted')
        for i in range(1, acts_num+1):
            self.lstbox.insert('end', i)
        self.tech_inf_print('Indexing complete')

    def tab_insert(self):
        self.txt.delete(index1='1.0', index2='end')
        splitted = self.store[self.index].split('\n')
        text = '\t' + splitted[0] + '\n\t'.join(splitted[1:])
        self.txt.insert('1.0', chars=text)
        self.tech_inf_print('Tabs inserted')

    def deletion(self):
        self.txt.delete(index1='1.0', index2='end')
        self.tech_inf_print('Text deleted')

    def tech_inf_print(self, message):
        string = (str(dt.datetime.now())[:-7] + ('.'*6) + message + '\n')
        self.bottomtext.insert('end', chars=string)

Main().mainloop()
