import re
import tkinter as tk
from tkinter import ttk

'''
string_1 = MainPage().string_1
string_2 = MainPage().string_2
lists_similarity = MainPage().lists_similarity
string_1_p = MainPage().string_1_p
string_2_p = MainPage().string_2_p
lenlist1 = MainPage().lenlist1
lenlist2 = MainPage().lenlist2
lenLCS = MainPage().lenLCS
'''

HEADERFONT = ("Verdana", 14)
SIMFONT = ("Verdana", 12, "bold")
INFOFONT = ("Verdana", 11)

'''
string_1 = tk.StringVar()
string_2 = tk.StringVar()
lists_similarity = tk.StringVar()
string_1_p = tk.StringVar()
string_2_p = tk.StringVar()
lenlist1 = tk.StringVar()
lenlist2 = tk.StringVar()
lenLCS = tk.StringVar()


def LCS_Length(X, Y):
    m = len(X)
    n = len(Y)
    c = [[None for nn in range(n+1)] for mm in range(m+1)]
    b = [[None for nn in range(n+1)] for mm in range(m+1)]
    for i in range(1, m+1):
        c[i][0] = 0
        for j in range(n+1):
            c[0][j] = 0
            for i in range(1, m+1):
                for j in range(1, n+1):
                    if X[i-1] == Y[j-1]:
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


def Print_LCS_num(b, X, i, j, s1, s2):
    if i == 0 or j == 0:
        return None
    if b[i][j] == 'DIOG':
        Print_LCS_num(b,X, i-1, j-1, s1, s2)
        s1.append(i-1)
        s2.append(j-1)
    elif b[i][j] == 'UP':
        Print_LCS_num(b, X, i-1, j, s1, s2)
    else:
            Print_LCS_num(b, X, i, j-1, s1, s2)


def LCS_main():
    lists_similarity.set('')
    string_1_p.set('')
    string_2_p.set('')
    lenlist1.set('')
    lenlist2.set('')
    lenLCS.set('')
    
    string1 = string_1.get()
    list1 = re.sub("[^\w]", " ", string1).lower().split()
    string2 = string_2.get()
    list2 = re.sub("[^\w]", " ", string2).lower().split()
    lenLCS, b_tab = LCS_Length(list1, list2)
    num_box_list1 = []
    num_box_list2 = []

    Print_LCS_num(b_tab, list1, len(list1), len(list2), num_box_list1, num_box_list2)

    if len(list1) == len(list2) == lenLCS :
        lists_similarity.set('Фрагменты не содержат различий')
    else:
        resultlist1 = list1[:]
        for i in range(len(resultlist1)):
            if i not in num_box_list1:
                resultlist1[i] = '*'+resultlist1[i].upper()+'*'
        resultlist2 = list2[:]
        for i in range(len(resultlist2)):
            if i not in num_box_list2:
                resultlist2[i] = '*'+resultlist2[i].upper()+'*'
        string_1_p.set(' '.join(resultlist1))
        string_2_p.set(' '.join(resultlist2))
        lenlist1.set('The length of the 1 list is: %d' % len(resultlist1))
        lenlist2.set('The length of the 2 list is: %d' % len(resultlist2))
        lenLCS.set('The length of LCS is: %d' % lenLCS)


def clean():
    string_1.set('')
    string_2.set('')
    lists_similarity.set('')
    string_1_p.set('')
    string_2_p.set('')
    lenlist1.set('')
    lenlist2.set('')
    lenLCS.set('')
'''


class GUIContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        title = self.title("Поиск различий в текстах")
        container = ttk.Frame(self)
        container.grid(sticky='nsew')

        self.string_1 = tk.StringVar()
        self.string_2 = tk.StringVar()
        self.lists_similarity = tk.StringVar()
        self.string_1_p = tk.StringVar()
        self.string_2_p = tk.StringVar()
        self.lenlist1 = tk.StringVar()
        self.lenlist2 = tk.StringVar()
        self.lenLCS = tk.StringVar()

        self.frame = MainPage(container, self)
        self.frame.grid(sticky='nsew')
        self.frames = {}
        self.frames['MainPage'] = self.frame

        self.show_frame('MainPage')
      
    def show_frame(self, page_name):
        frame = self.frames['MainPage']
        frame.tkraise

    def LCS_Length(self, X, Y):
        m = len(X)
        n = len(Y)
        c = [[0 for nn in range(n+1)] for mm in range(m+1)]
        b = [[0 for nn in range(n+1)] for mm in range(m+1)]
        for i in range(1, m+1):
            c[i][0] = 0
        for j in range(n+1):
            c[0][j] = 0
            for i in range(1, m+1):
                for j in range(1, n+1):
                    if X[i-1] == Y[j-1]:
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

    def Print_LCS_num(self, b, X, i, j, s1, s2):
        if i == 0 or j == 0:
            return None
        if b[i][j] == 'DIOG':
            self.Print_LCS_num(b,X, i-1, j-1, s1, s2)
            s1.append(i-1)
            s2.append(j-1)
        elif b[i][j] == 'UP':
            self.Print_LCS_num(b, X, i-1, j, s1, s2)
        else:
            self.Print_LCS_num(b, X, i, j-1, s1, s2)

    def LCS_main(self):
        self.lists_similarity.set('')
        self.string_1_p.set('')
        self.string_2_p.set('')
        self.lenlist1.set('')
        self.lenlist2.set('')
        self.lenLCS.set('')
        self.frame.text_str1.delete('1.0', 'end')
        self.frame.text_str2.delete('1.0', 'end')

        string1 = self.string_1.get()
        list1 = re.sub("[^\w]", " ", string1).lower().split()
        string2 = self.string_2.get()
        list2 = re.sub("[^\w]", " ", string2).lower().split()
        lenLCS, b_tab = self.LCS_Length(list1, list2)
        num_box_list1 = []
        num_box_list2 = []
        resultlist1 = []
        resultlist2 = []

        self.Print_LCS_num(b_tab, list1, len(list1), len(list2), num_box_list1, num_box_list2)

        if len(list1) == len(list2) == lenLCS :
            self.lists_similarity.set('Отрывки не содержат различий')
            self.lenlist1.set('Длина первого отрывка: %d' % len(list1))
            self.lenlist2.set('Длина второго отрывка: %d' % len(list2))
            self.lenLCS.set('Количество схожих фрагментов: %d' % lenLCS)
        else:
            resultlist1 = list1[:]
            for i in range(len(resultlist1)):
                if i not in num_box_list1:
                    resultlist1[i] = '*'+resultlist1[i].upper()+'*'
            resultlist2 = list2[:]
            for i in range(len(resultlist2)):
                if i not in num_box_list2:
                    resultlist2[i] = '*'+resultlist2[i].upper()+'*'
            self.string_1_p.set(' '.join(resultlist1))
            self.string_2_p.set(' '.join(resultlist2))
            self.lenlist1.set('Длина первого отрывка: %d' % len(resultlist1))
            self.lenlist2.set('Длина второго отрывка: %d' % len(resultlist2))
            self.lenLCS.set('Количество схожих фрагментов: %d' % lenLCS)
            self.frame.text_str1.insert('1.0', self.string_1_p.get())
            self.frame.text_str1.highlight_pattern('\*\w+\*', 'green')
            self.frame.text_str2.insert('1.0', self.string_2_p.get())
            self.frame.text_str2.highlight_pattern('\*\w+\*', 'yellow')


    def clean(self):
        self.string_1.set('')
        self.string_2.set('')
        self.lists_similarity.set('')
        self.string_1_p.set('')
        self.string_2_p.set('')
        self.lenlist1.set('')
        self.lenlist2.set('')
        self.lenLCS.set('')
        self.frame.text_str1.delete('1.0', 'end')
        self.frame.text_str2.delete('1.0', 'end')


class MainPage(ttk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_top = ttk.Label(text='Поиск различающихся слов и обозначений', font = HEADERFONT)
        label_top.grid(row=0, column=0, columnspan=2)
        
        entry_str1 = ttk.Entry(textvariable=controller.string_1, width=75)
        entry_str1.grid(row=1, column=0, sticky='w')

        button1_process = ttk.Button(text='Сравнить', command=lambda: controller.LCS_main())
        button1_process.grid(row=1, column=1, sticky='e')

        entry_str2 = ttk.Entry(textvariable=controller.string_2, width=75)
        entry_str2.grid(row=2, column=0, sticky='w')
        
        button2_clean = ttk.Button(text='Очистить', command=lambda: controller.clean())
        button2_clean.grid(row=2, column=1, sticky='e')

        label_mid_inform_1 = ttk.Label(textvariable=controller.lists_similarity, font=SIMFONT)
        label_mid_inform_1.grid(row=3, column=0, columnspan=2, sticky='w', pady=10)
        label_mid_inform_2 = ttk.Label(textvariable=controller.lenlist1, font=INFOFONT)
        label_mid_inform_2.grid(row=4, column=0, columnspan=2, sticky='w')
        label_mid_inform_3 = ttk.Label(textvariable=controller.lenlist2, font=INFOFONT)
        label_mid_inform_3.grid(row=5, column=0, columnspan=2, sticky='w')
        label_mid_inform_4 = ttk.Label(textvariable=controller.lenLCS, font=INFOFONT)
        label_mid_inform_4.grid(row=6, column=0, columnspan=2, sticky='w')

        label_textboxname_1 = ttk.Label(text='Отрывок 1:')
        label_textboxname_1.grid(row=7, column=0, columnspan=2, sticky='nsew')
                
        self.text_str1 = CustomTextWidget(wrap='word', height=15)
        self.text_str1.grid(row=8, column=0, columnspan=2)
        self.text_str1.tag_configure("green", background="#00ff00", overstrike=1)

        label_textboxname_2 = ttk.Label(text='Отрывок 2:')
        label_textboxname_2.grid(row=9, column=0, columnspan=2, sticky='nsew')

        self.text_str2 = CustomTextWidget(wrap='word', height=15)
        self.text_str2.grid(row=10, column=0, columnspan=2)
        self.text_str2.tag_configure("yellow", background="yellow")


class CustomTextWidget(tk.Text):

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        '''The following below code was taken from here: http://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget'''

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=True):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

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


'''
string_1 = StringVar()
string_2 = StringVar()
lists_similarity = StringVar()
string_1_p = StringVar()
string_2_p = StringVar()
lenlist1 = StringVar()
lenlist2 = StringVar()
lenLCS = StringVar()
'''

'''
string_1 = tk.StringVar()
string_2 = tk.StringVar()
lists_similarity = tk.StringVar()
string_1_p = tk.StringVar()
string_2_p = tk.StringVar()
lenlist1 = tk.StringVar()
lenlist2 = tk.StringVar()
lenLCS = tk.StringVar()


def LCS_Length(X, Y):
    m = len(X)
    n = len(Y)
    c = [[None for nn in range(n+1)] for mm in range(m+1)]
    b = [[None for nn in range(n+1)] for mm in range(m+1)]
    for i in range(1, m+1):
        c[i][0] = 0
        for j in range(n+1):
            c[0][j] = 0
            for i in range(1, m+1):
                for j in range(1, n+1):
                    if X[i-1] == Y[j-1]:
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


def Print_LCS_num(b, X, i, j, s1, s2):
    if i == 0 or j == 0:
        return None
    if b[i][j] == 'DIOG':
        Print_LCS_num(b,X, i-1, j-1, s1, s2)
        s1.append(i-1)
        s2.append(j-1)
    elif b[i][j] == 'UP':
        Print_LCS_num(b, X, i-1, j, s1, s2)
    else:
            Print_LCS_num(b, X, i, j-1, s1, s2)


def LCS_main():
    lists_similarity.set('')
    string_1_p.set('')
    string_2_p.set('')
    lenlist1.set('')
    lenlist2.set('')
    lenLCS.set('')
    
    string1 = string_1.get()
    list1 = re.sub("[^\w]", " ", string1).lower().split()
    string2 = string_2.get()
    list2 = re.sub("[^\w]", " ", string2).lower().split()
    lenLCS, b_tab = LCS_Length(list1, list2)
    num_box_list1 = []
    num_box_list2 = []

    Print_LCS_num(b_tab, list1, len(list1), len(list2), num_box_list1, num_box_list2)

    if len(list1) == len(list2) == lenLCS :
        lists_similarity.set('Фрагменты не содержат различий')
    else:
        resultlist1 = list1[:]
        for i in range(len(resultlist1)):
            if i not in num_box_list1:
                resultlist1[i] = '*'+resultlist1[i].upper()+'*'
        resultlist2 = list2[:]
        for i in range(len(resultlist2)):
            if i not in num_box_list2:
                resultlist2[i] = '*'+resultlist2[i].upper()+'*'
        string_1_p.set(' '.join(resultlist1))
        string_2_p.set(' '.join(resultlist2))
        lenlist1.set('The length of the 1 list is: %d' % len(resultlist1))
        lenlist2.set('The length of the 2 list is: %d' % len(resultlist2))
        lenLCS.set('The length of LCS is: %d' % lenLCS)


def clean():
    string_1.set('')
    string_2.set('')
    lists_similarity.set('')
    string_1_p.set('')
    string_2_p.set('')
    lenlist1.set('')
    lenlist2.set('')
    lenLCS.set('')
'''


app = GUIContainer()
app.mainloop()
