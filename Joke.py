import random as rd
from tkguilib import GUI_Manager, tk, ttk

path = r'C:\Users\EA-ShevchenkoIS\Desktop\ПиН.txt'
encoding = 'utf_8'

class Joke():
    def __init__(self, path=path, encoding=encoding):
        self.path = path
        self.encoding = encoding
        self.text=self.open_up() #Store for the list of text strings

    def key_gen(self, digits, counter, delimiter='::'):
        num = str(counter)
        return ('0'*(digits-len(num))+num+delimiter+' ')

    def open_up(self, path=None, encoding=None, count_num=None):
        path = path if path else self.path
        encoding = encoding if encoding else self.encoding
        counter = count_num if count_num else 1
        store = []
        key_gen = self.key_gen
        with open(path, encoding=encoding) as file:
            for line in file:
                if line == '\n':
                    pass
                else:
                    line = key_gen(4, counter)+line[:-1]
                    store.append(line)
                    counter+=1
        return store

    def extractor(self, pointer=None):
        length = len(self.text)
        if pointer == None:
            return rd.choice(self.text)
        elif pointer <= length:
            return self.text[pointer-1]
        else:
            return 'pointer error'

    def add_text(self, path, encoding=None):
        encoding = encoding if encoding else self.encoding
        store = self.open_up(path=path,
                             encoding=encoding,
                             count_num=len(self.text))
        self.text.extend(store)

class GUI(GUI_Manager):
    def __init__(self):
        self.joke = Joke()
        self.text = None
        self.buttons = None
        self.pointer = None
        self.priv_pointer = None
        self.next_pointer = None
        self.make_interface()

    def make_interface(self):
        buttons_list = [['Priv', self.priv_extr_first],
                        ['%%%', self.rand_extr],
                        ['Next', self.next_extr_first],
                        ['Del', self.custom_del]]
        buffer = tk.Frame()
        left_fr = tk.Frame(master=buffer)
        right_fr = tk.Frame(master=buffer)
        for i,j in zip([buffer, left_fr, right_fr],
                       [['top', 'yes', 'both'],
                        ['left', 'yes', 'both'],
                        ['right', 'no', 'y']]):
            k, l, m = j
            i.pack(side=k, expand=l, fill=m)
        self.text = self.make_text_with_scroll(parent=left_fr)
        #self.text['wrap']='word'
        self.buttons = self.make_buttons(parent=right_fr,
                                         buttons_list=buttons_list,
                                         width=10)
        tk.mainloop()

    def rand_extr(self):
        if self.pointer:
            self.pointer=None
            string = self.joke.extractor()+'\n'
            self.pointer = int(string[:4])
            self.text.insert(index='1.0', chars=string)
            self.text.see(index='1.0')
            for i,j in zip(['Priv', 'Next'],
                           [self.priv_extr_first,
                            self.next_extr_first]):
                self.buttons[i]['command'] = j
        else:
            string = self.joke.extractor()+'\n'
            self.pointer = int(string[:4])
            self.text.insert(index='1.0', chars=string)

    def priv_extr_first(self):
        if self.pointer:
            string = self.joke.extractor(self.pointer-1)+'\n'
            self.priv_pointer = int(string[:4])
            self.text.insert(index='1.0', chars=string)
            self.buttons['Priv']['command'] = self.priv_extr_next
            self.text.see(index='1.0')
        else:
            string = 'priv pointer error!'+'\n'
            self.text.insert(index='1.0', chars=string)

    def priv_extr_next(self):
        string = self.joke.extractor(self.priv_pointer-1)+'\n'
        self.priv_pointer = int(string[:4])
        self.text.insert(index='1.0', chars=string)
        self.text.see(index='1.0')

    def next_extr_first(self):
        if self.pointer:
            string = self.joke.extractor(self.pointer+1)+'\n'
            self.next_pointer = int(string[:4])
            self.text.insert(index='end', chars=string)
            self.buttons['Next']['command'] = self.next_extr_next
            self.text.see(index='end')
        else:
            string = 'next pointer error!'+'\n'
            self.text.insert(index='end', chars=string)
            self.text.see(index='end')

    def next_extr_next(self):
        string = self.joke.extractor(self.next_pointer+1)+'\n'
        self.next_pointer = int(string[:4])
        self.text.insert(index='end', chars=string)
        self.text.see(index='end')

    def custom_del(self):
        self.pointer = None
        self.priv_pointer = None
        self.next_pointer = None
        self.text.delete(index1='1.0', index2='end')
        for i,j in zip(['Priv', 'Next'],
                       [self.priv_extr_first,
                        self.next_extr_first]):
            self.buttons[i]['command'] = j
