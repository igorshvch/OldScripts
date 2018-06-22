import re
import tkinter as tk

FONT = ('times', 14, 'bold')

def find(string):
    pattern = r'(?<=ID=)[0-9]+(?=&)'
    try:
        return re.search(pattern, string).group(0)
    except:
        return 'Wrong input format!'

class SimpleGui(tk.Frame):
    def __init__(self, parent=None, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, **kargs)
        self.master.title('Определение ID задачи')
        self.pack(expand='yes', fill='both')
        self.makewidgets()
        self.tempstore=['', '']
    def makewidgets(self):
        top = tk.Frame(self)
        top.pack(side='top', expand='yes', fill='both')
        mid = tk.Frame(self)
        mid.pack(side='left', fill='x')
        bottom = tk.Frame(self)
        bottom.pack(side='right', expand='yes', fill='x')
        self.txt = tk.Text(top, relief='sunken')
        self.txt.bind('<Return>', self.find)
        self.txt.pack(expand='yes', fill='both')
        button_find = tk.Button(mid, text='ID find', command=self.find, height=3, width=30)
        button_find.pack(side='left')
        button_delete = tk.Button(mid, text='Delete', command=lambda:self.txt.delete('1.0', 'end'), height=3, width=30)
        button_delete.pack(side='left')
        self.label_1 = tk.Label(bottom, font=FONT)
        self.label_1.pack(side='top', expand='yes')
        self.label_2 = tk.Label(bottom)
        self.label_2.pack(side='top', expand='yes')
    def find(self, event):
        string = self.txt.get('1.0', 'end-1c')
        if not string:
            self.tempstore[1] = self.tempstore[0]
            self.tempstore[0] = 'empty'
            self.label_1.config(text=self.tempstore[0])
            self.label_2.config(text=self.tempstore[1])
            self.tempstore[0] = 'Previous = ' + self.tempstore[0]
        else:
            store = find(string)
            self.tempstore[1] = self.tempstore[0]
            self.tempstore[0] = store
            self.label_1.config(text=self.tempstore[0])
            self.label_2.config(text=self.tempstore[1])
            self.tempstore[0] = 'Previous = ' + store

SimpleGui().mainloop()
