from act_sep import ActSep
import tkinter as tk
from tkinter import ttk
from tkguilib import GUI_Manager, TopMenu
import shelve
from sys import version_info

PyVer = version_info[1]

class SideWindow(GUI_Manager, tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        #GUI_Manager.__init__(self)
        #self.option_add('*tearOff', 'false')
        self.db_connection = '' #Accept 'New' or 'Old' string values
        self.path = tk.StringVar()
        self.path.set('Undefined')
        self.frames_names = ['buffer', 'left_main', 'right_bar',
                             'left_cons_holder', 'left_cons_l_txt', 'left_cons_l_lst',
                             'left_cons_connection_label', 'left_cons_inf_label',
                             'left_cons_label', 'left_cons_txt',
                             'left_lst1_holder', 'left_lst2_holder',
                             'left_lst1_l', 'left_lst1_box', 'left_lst2_l', 'left_lst2_box',
                             'left_text_holder', 'left_text_label',
                             'left_text_txt',
                             'right_buttons_holder','right_buttons_label',
                             'right_buttons_container']
        self.frames={}
        self.frames['buffer'] = {'f_object':tk.Frame(master=self),
                                 'f_relief':'sunken', 'f_bd':1}
        self.frames['left_main'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                    'f_side':'left', 'f_expand':'yes', 'f_fill':'both'}
        self.frames['right_bar'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                    'f_side':'right', 'f_expand':'no', 'f_fill':'y',
                                    'f_relief':'sunken', 'f_bd':1}
        self.frames['left_cons_holder'] = {'f_object':tk.Frame(master=self.frames['left_main']['f_object']),
                                           'f_expand':'no', 'f_fill':'x'}
        self.frames['left_cons_l_txt'] = {'f_object':tk.Frame(master=self.frames['left_cons_holder']['f_object']),
                                          'f_side':'left', 'f_expand':'yes', 'f_fill':'both',
                                          'f_relief':'sunken', 'f_bd':1}
        self.frames['left_cons_l_lst'] = {'f_object':tk.Frame(master=self.frames['left_cons_holder']['f_object']),
                                          'f_side':'right', 'f_expand':'no', 'f_fill':'y',
                                          'f_relief':'sunken', 'f_bd':1}
        self.frames['left_cons_connection_label'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_txt']['f_object']),
                                                     'f_expand':'no', 'f_fill':'x'}
        self.frames['left_cons_inf_label'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_txt']['f_object']),
                                              'f_expand':'no', 'f_fill':'x'}
        self.frames['left_cons_label'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_txt']['f_object']),
                                          'f_expand':'no', 'f_fill':'x'}
        self.frames['left_cons_txt'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_txt']['f_object']),
                                        'f_expand':'yes', 'f_fill':'both'}
        self.frames['left_lst1_holder'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_lst']['f_object']),
                                          'f_side':'left', 'f_expand':'no', 'f_fill':'both'}
        self.frames['left_lst2_holder'] = {'f_object':tk.Frame(master=self.frames['left_cons_l_lst']['f_object']),
                                          'f_side':'right', 'f_expand':'no', 'f_fill':'both'}
        self.frames['left_lst1_l'] = {'f_object':tk.Frame(master=self.frames['left_lst1_holder']['f_object']),
                                      'f_side':'top', 'f_expand':'no', 'f_fill':'x',
                                      'f_relief':'sunken', 'f_bd':1}
        self.frames['left_lst1_box'] = {'f_object':tk.Frame(master=self.frames['left_lst1_holder']['f_object']),
                                        'f_side':'top', 'f_expand':'no', 'f_fill':'y'}
        self.frames['left_lst2_l'] = {'f_object':tk.Frame(master=self.frames['left_lst2_holder']['f_object']),
                                      'f_side':'top', 'f_expand':'no', 'f_fill':'x',
                                      'f_relief':'sunken', 'f_bd':1}
        self.frames['left_lst2_box'] = {'f_object':tk.Frame(master=self.frames['left_lst2_holder']['f_object']),
                                        'f_side':'top', 'f_expand':'no', 'f_fill':'y'}
        self.frames['left_text_holder'] = {'f_object':tk.Frame(master=self.frames['left_main']['f_object']),
                                           'f_expand':'yes', 'f_fill':'both'}
        self.frames['left_text_label'] = {'f_object':tk.Frame(master=self.frames['left_text_holder']['f_object']),
                                          'f_expand':'no', 'f_fill':'x'}
        self.frames['left_text_txt'] = {'f_object':tk.Frame(master=self.frames['left_text_holder']['f_object']),
                                        'f_expand':'yes', 'f_fill':'both'}
        self.frames['right_buttons_holder'] = {'f_object':tk.Frame(master=self.frames['right_bar']['f_object']),
                                               'f_expand':'no', 'f_fill':'y'}
        self.frames['right_buttons_label'] = {'f_object':tk.Frame(master=self.frames['right_buttons_holder']['f_object']),
                                              'f_expand':'no', 'f_fill':'y'}
        self.frames['right_buttons_container'] = {'f_object':tk.Frame(master=self.frames['right_buttons_holder']['f_object']),
                                                  'f_expand':'no', 'f_fill':'y'}
        self.texts={}
        self.buttons_txt={}
        self.buttons_right = [['Clean', self.remove_all],
                              ['Path', self.path_find],
                              ['Reload', lambda:print('SideW-reload')],
                              ['Save', lambda:print('SideW-save')]]
        self.buttons_lstb = [['Prcd', self.lstb_prcd],
                             ['UnPrcd', self.lstb_unprcd]]
        self.acts_prcd_dict = {}
        self.acts_prcd_dict['processed'] = []
        self.acts_prcd_dict['unprocessed'] = []
        self.lstbox = None
        self.labels = ['left_cons_label',
                       'left_text_label']
        self.c_txt_n = ['left_cons_txt',
                        'left_text_txt']
        menu_dict = {'01File':[['Comand1', lambda:print('cmd1')],
                               ['Comand2', lambda:print('cmd2')],
                               ['Comand3', lambda:print('cmd3')],
                               ['Comand4', lambda:print('cmd4')],
                               ['Quit', self.destroy]]}
        top_menu = TopMenu(self, menu_dict)
        #
        for i in self.frames:
                self.frames[i]['f_padx'] = 1
                self.frames[i]['f_pady'] = 1
        self.make_all_widgets()
        
    def make_all_widgets(self):
        #Frames
        self.make_frames(self.frames, self.frames_names)
        ###
        #Text & labels
        for labl,ttn,width in zip(self.labels, self.c_txt_n, [20,40]):
            self.make_lb_text(frames_dict=self.frames, parent_lb_name=labl,
                              parent_txt_name=ttn, border1=5, border2=-6,
                              buttons_holder=self.buttons_txt, widget_width=width)
            self.texts[ttn].bind('<Control-igrave>',
                                  lambda event, ttn=ttn:self.special_insert_db(ttn,
                                                                               self.texts[ttn]))
        ###
        #Cons inf labels left_cons_connection_label left_cons_inf_label
        tk.Label(master=self.frames['left_cons_connection_label']['f_object'],
                 text='Connection:', relief='flat', bg='pink', bd=1,
                 width=10).pack(side='left', expand='no',fill='none')
        self.DB_C = tk.Label(master=self.frames['left_cons_connection_label']['f_object'],
                             text='DB is not connected', relief='raised', bd=1)
        self.DB_C.pack(side='right', expand='yes', fill='x', padx=1)
        
        tk.Label(master=self.frames['left_cons_inf_label']['f_object'],
                 text='Path:', relief='flat', bg='pink', bd=1,
                 width=10).pack(side='left', expand='no', fill='none')
        self.inf = tk.Label(master=self.frames['left_cons_inf_label']['f_object'],
                            textvar=self.path, relief='raised', bd=1)
        self.inf.pack(side='right', expand='yes', fill='x', padx=1)
        
        ###
        #Listboxes
        tk.Label(master=self.frames['left_lst1_l']['f_object'],
                 text='Unprocessed').pack(side='left')
        tk.Button(master=self.frames['left_lst1_l']['f_object'],
                  text=self.buttons_lstb[0][0],
                  command=self.buttons_lstb[0][1]).pack(side='right')
        self.lstbox_unproceed = self.make_listbox(parent=self.frames['left_lst1_box']['f_object'],
                                                  action_argument=None, listbox_width=20)
        tk.Label(master=self.frames['left_lst2_l']['f_object'],
                     text='Processed').pack(side='left')
        tk.Button(master=self.frames['left_lst2_l']['f_object'],
                  text=self.buttons_lstb[1][0],
                  command=self.buttons_lstb[1][1]).pack(side='right')
        self.lstbox_proceed = self.make_listbox(parent=self.frames['left_lst2_box']['f_object'],
                                                action_argument=None, listbox_width=20)
        ###
        #Buttons
        self.buttons_rgbar = self.make_buttons(parent=self.frames['right_buttons_container']['f_object'],
                                         buttons_list=self.buttons_right,
                                         width=5)
        if not self.db_connection:
            for key in ['Reload', 'Save']:
                self.buttons_rgbar[key]['state']='disabled'
        ###

    def path_find(self):
        def allocate(text, widget_var):
            path = text.get(index1='1.0', index2='end-1c')+'\ActsTexts'
            self.path.set(path)
            #self.db_connection = True
            self.DB_C['text']='Connection is established'
            try:
                db = shelve.open(path, flag='w')
                self.db_connection = 'Old'
            except:
                acts = self.sep_acts()
                db = shelve.open(path, flag='c')
                self.db_connection = 'New'
            if self.db_connection == 'Old':
                for i in range(1, len(db.keys())+1, 1):
                    self.lstbox_unproceed.insert('end', self.key_gen('act_', i))
                self.acts_prcd_dict = db['acts_prcd']
                db.close()
            elif self.db_connection == 'New':
                for i in range(1, len(acts)+1, 1):
                    label = self.key_gen('act_', i)
                    db[label] = acts[i-1]
                    self.lstbox_unproceed.insert('end', label)
                    self.acts_prcd_dict['unprocessed'].append(label)
                    print(label, end=', ')
                db['acts_prcd'] = self.acts_prcd_dict
                db.close()
            for key in ['Reload', 'Save']:
                self.buttons_rgbar[key]['state']='normal'
            widget_var.destroy()
        new_window = self.new_win(title='Enter path to database')
        container_text = tk.Frame(new_window)
        container_buttons = tk.Frame(new_window, relief='sunken', bd=1)
        container_text.pack(side='top', padx=1, pady=1)
        container_buttons.pack(side='top', fill='x', padx=1, pady=1)
        text = self.make_text_with_scroll(parent=container_text, widget_height=3, widget_width=80)
        text.bind('<Control-igrave>', lambda event:self.special_insert(text))
        tk.Button(master=container_buttons,
                  text='Allocate',
                  command=lambda:allocate(text, new_window)).pack(side='left', fill='x')
        tk.Button(master=container_buttons,
                  text='Quit',
                  command=new_window.destroy).pack(side='right', fill='x')

    def sep_acts(self):
        separator = ActSep(my_path = r'C:\Python3{0}\AP\АС МО 1023 2017-2303-0106.txt'.format(PyVer))
        return separator.store

    def remove_all(self):
        for i in self.c_txt_n:
            self.texts[i].delete(index1='1.0', index2='end')

    def special_insert_db(self, txt_name, widget):
        self.special_insert(widget)
        self.special_confirm_db(txt_name, widget)

    def special_insert(self, widget):
        widget.insert(index='1.0',
                      chars=self.selection_get(selection = "CLIPBOARD"))

    def special_confirm_db(self, txt_name, widget):
        widget.config(state='disabled', bg='#d4d0c8')
        self.buttons_txt[txt_name]['Confirm']['state']='disabled'
        self.buttons_txt[txt_name]['Del']['state']='disabled'

    def special_edit_db(self, txt_name, widget):
        widget.config(state='normal', bg='white')
        self.buttons_txt[txt_name]['Confirm']['state']='normal'
        self.buttons_txt[txt_name]['Del']['state']='normal'

    def special_del_db(self, txt_name, widget):
        widget.delete(index1='1.0', index2='end')
        self.buttons_txt[txt_name]['Confirm']['state']='normal'

    def key_gen(self, string, counter):
        return (string+('0'*(6-len(str(counter))))+str(counter))

    def lstb_prcd(self):
        position = self.lstbox_unproceed.curselection()
        if position:
            print(type(self.lstbox_unproceed.curselection()))
            label = self.lstbox_unproceed.get('active')
            self.lstbox_unproceed.delete(position)
            processed = self.acts_prcd_dict['processed']
            if processed:
                if label > processed[-1]:
                    processed.append(label)
                    self.acts_prcd_dict['processed'] = processed
                    self.lstbox_proceed.insert('end', label)
                elif label < processed[-1]:
                    processed.append(label)
                    processed = sorted(processed)
                    self.acts_prcd_dict['processed'] = processed
                    self.lstbox_proceed.delete('0', 'end')
                    for i in processed:
                        self.lstbox_proceed.insert('end', i)
                else:
                    print('Label storing error!')
            else:
                processed.append(label)
                self.lstbox_proceed.insert('end', label)
        else:
            print('Nothing is selected')
            
    def lstb_unprcd(self):
        position = self.lstbox_proceed.curselection()
        if position:
            print(type(self.lstbox_unproceed.curselection()))
            label = self.lstbox_proceed.get('active')
            self.lstbox_proceed.delete(position)
            unprocessed = self.acts_prcd_dict['unprocessed']
            if unprocessed:
                if label > unprocessed[-1]:
                    unprocessed.append(label)
                    self.acts_prcd_dict['unprocessed'] = unprocessed
                    self.lstbox_unproceed.insert('end', label)
                elif label < unprocessed[-1]:
                    unprocessed.append(label)
                    unprocessed = sorted(unprocessed)
                    self.acts_prcd_dict['unprocessed'] = unprocessed
                    self.lstbox_unproceed.delete('0', 'end')
                    for i in unprocessed:
                        self.lstbox_unproceed.insert('end', i)
                else:
                    print('Label storing error!')
            else:
                unprocessed.append(label)
                self.lstbox_unproceed.insert('end', label)
        else:
            print('Nothing is selected')
