import tkinter as tk

default_bl_1 = [['One', lambda:print('"One" was pressed!')],
                ['Two', lambda:print('"Two" was pressed!')]]

default_bl_2 = [['Three', lambda:print('"Three" was pressed!')],
                ['Four', lambda:print('"Four" was pressed!')]]

test_list = ['item {}'.format(i) for i in range(20)]

class TwoListBoxes(tk.Frame):
    def __init__(self, parent=None,
                 sl_side='top',
                 widgets_orient='horizontal',
                 bl1=default_bl_1,
                 bl2=default_bl_2,
                 lb_txt1='Default',
                 lb_txt2='Default',
                 data1 = test_list,
                 data2 = None,
                 inner_binding=None):
        tk.Frame.__init__(self, parent)
        self.bl1 = bl1
        self.bl2 = bl2
        self.data1 = data1
        self.data2 = data2
        self.lb_txt1 = lb_txt1
        self.lb_txt2 = lb_txt2
        self.b_dict = {} #buttons dictionary
        self.wo = widgets_orient
        self.lb1 = None #Listbox holder
        self.lb2 = None #Listbox holder
        self.inner_binding = inner_binding
        self.pack(side=sl_side, expand='yes', fill='both')
        self.make_widgets()
        self.fill_data()

    def make_buttons(self, parent, buttons_list):
        for name, func in buttons_list:
            self.b_dict[name] = tk.Button(parent,
                                          text=name,
                                          command=func)
            self.b_dict[name].pack(side='left',
                                   expand='no',
                                   fill='x')

    def make_lstb(self,
                  buttons_list,
                  lb_text='Default'
                  ):
        container = tk.Frame(self)
        label = tk.Label(container,
                         text=lb_text)
        lstb_scr_container = tk.Frame(container)
        sbar = tk.Scrollbar(lstb_scr_container)
        lst_b = tk.Listbox(lstb_scr_container, relief='sunken', height=8)
        sbar.config(command=lst_b.yview)
        lst_b.config(yscrollcommand=sbar.set)
        buttons_container = tk.Frame(container)
        container.pack(side=('left' if self.wo == 'horizontal' else 'top'),
                       expand='yes',
                       fill='both')
        label.pack(side='top', expand='no', fill='both')
        lstb_scr_container.pack(side='top', expand='yes', fill='both')
        sbar.pack(side='right', fill='y')
        lst_b.pack(side='left', expand='yes', fill='both')
        buttons_container.pack(side='top', expand='no', fill='x')
        self.make_buttons(buttons_container, buttons_list)
        return lst_b

    def make_widgets(self):
        self.lb1 = self.make_lstb(self.bl1, lb_text=self.lb_txt1)
        self.lb2 = self.make_lstb(self.bl2, lb_text=self.lb_txt2)
        if self.inner_binding:
            self.lb1.bind('<Double-1>', lambda event: \
                          self.extract_from_lb(event, self.lb1, self.lb2))
            self.lb2.bind('<Double-1>', lambda event: \
                          self.extract_from_lb(event, self.lb2, self.lb1))
                      

    def fill_data(self):
        if not self.data2:
            for i in self.data1:
                self.lb1.insert('end', i)
        else:
            for i in self.data1:
                self.lb1.insert('end', i)
            for i in self.data2:
                self.lb2.insert('end', i)

    def extract_from_lb(self, event, obj1, obj2):
        selection = obj1.curselection()
        if selection:
            label = obj1.get(selection)
            obj1.delete(selection)
            obj2.insert('0', label)
            self.port4040 = selection
        else:
            pass
            

#TwoListBoxes(widgets_orient='horizontal').mainloop()
        
        
