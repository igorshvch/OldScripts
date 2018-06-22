from tkguilib import *
import Side_window as sw
import shelve

class Main(tk.Tk, GUI_Manager):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Acts parsing DB client')
        self.db_connection = False
        self.acts_counter = 0
        self.show_acts_count = tk.StringVar()
        self.show_acts_count.set(self.acts_counter)
        self.path = tk.StringVar()
        self.path.set('Undefined')
        self.tree_view = False

        self.side_window = None
        
        self.texts = {}
        
        self.frames_names = ['buffer',
                             'left_bar', 'left_bar_tree',
                             'left_bar_tree_buttons',
                             'center',
                             'right_bar', 'right_bar_label',
                             'right_bar_holder', 'right_bar_buttons',
                             'center_connect_label_holder',
                             'center_inf_label_holder',
                             'center_main_holder',
                             'center_actname_holder', 'center_actname_label',
                             'center_actname_txt',
                             'center_dem_holder', 'center_dem_label',
                             'center_dem_txt',
                             'center_priv_res_holder', 'center_priv_res_label',
                             'center_priv_res_txt',
                             'center_reason1_holder', 'center_reason1_label',
                             'center_reason1_txt',
                             'center_reason2_holder', 'center_reason2_label',
                             'center_reason2_txt',
                             'center_result1_holder', 'center_result1_label',
                             'center_result1_txt',
                             'center_result2_holder', 'center_result2_label',
                             'center_result2_txt']
        
        self.frames = {}
        self.frames['buffer'] = {'f_object':tk.Frame(master=self),
                                 'f_relief':'sunken', 'f_bd':1}
        self.frames['left_bar'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                   'f_side':'left', 'f_expand':'no', 'f_fill':'y',
                                   'f_relief':'sunken', 'f_bd':1}
        self.frames['left_bar_tree'] = {'f_object':tk.Frame(master=self.frames['left_bar']['f_object']),
                                        'f_side':'top', 'f_expand':'no', 'f_fill':'y',
                                        'f_relief':'sunken', 'f_bd':1}
        self.frames['left_bar_tree_buttons'] = {'f_object':tk.Frame(master=self.frames['left_bar']['f_object']),
                                                'f_side':'top', 'f_expand':'no', 'f_fill':'x',
                                                'f_relief':'sunken', 'f_bd':1}
        self.frames['center'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                 'f_side':'left', 'f_relief':'sunken', 'f_bd':1}
        self.frames['right_bar'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                    'f_side':'left', 'f_expand':'no', 'f_fill':'y',
                                    'f_relief':'sunken', 'f_bd':1}
        self.frames['right_bar_holder'] = {'f_object':tk.Frame(master=self.frames['right_bar']['f_object']),
                                           'f_expand':'yes', 'f_fill':'y'}
        self.frames['right_bar_buttons'] = {'f_object':tk.Frame(master=self.frames['right_bar_holder']['f_object'])}
        self.frames['right_bar_label'] = {'f_object':tk.Frame(master=self.frames['right_bar_holder']['f_object']),
                                          'f_expand':'no', 'f_side':'bottom'}
        self.frames['center_connect_label_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object']),
                                                      'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['center_inf_label_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object']),
                                                  'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['center_main_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object']),
                                             'f_fill':'both'}
        self.frames['center_actname_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_actname_label'] = {'f_object':tk.Frame(master=self.frames['center_actname_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_actname_txt'] = {'f_object':tk.Frame(master=self.frames['center_actname_holder']['f_object'])}
        self.frames['center_dem_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_dem_label'] = {'f_object':tk.Frame(master=self.frames['center_dem_holder']['f_object']),
                                           'f_expand':'no', 'f_fill':'x'}
        self.frames['center_dem_txt'] = {'f_object':tk.Frame(master=self.frames['center_dem_holder']['f_object'])}
        self.frames['center_priv_res_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_priv_res_label'] = {'f_object':tk.Frame(master=self.frames['center_priv_res_holder']['f_object']),
                                                'f_expand':'no', 'f_fill':'x'}
        self.frames['center_priv_res_txt'] = {'f_object':tk.Frame(master=self.frames['center_priv_res_holder']['f_object'])}
        self.frames['center_reason1_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_reason1_label'] = {'f_object':tk.Frame(master=self.frames['center_reason1_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_reason1_txt'] = {'f_object':tk.Frame(master=self.frames['center_reason1_holder']['f_object'])}
        self.frames['center_reason2_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_reason2_label'] = {'f_object':tk.Frame(master=self.frames['center_reason2_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_reason2_txt'] = {'f_object':tk.Frame(master=self.frames['center_reason2_holder']['f_object'])}
        self.frames['center_result1_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_result1_label'] = {'f_object':tk.Frame(master=self.frames['center_result1_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_result1_txt'] = {'f_object':tk.Frame(master=self.frames['center_result1_holder']['f_object'])}
        self.frames['center_result2_holder'] = {'f_object':tk.Frame(master=self.frames['center_main_holder']['f_object'])}
        self.frames['center_result2_label'] = {'f_object':tk.Frame(master=self.frames['center_result2_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_result2_txt'] = {'f_object':tk.Frame(master=self.frames['center_result2_holder']['f_object'])}
        
        self.c_txt_n = ['center_actname_txt',
                        'center_dem_txt',
                        'center_priv_res_txt',
                        'center_reason1_txt',
                        'center_reason2_txt',
                        'center_result1_txt',
                        'center_result2_txt']
        self.labels = ['center_actname_label',
                       'center_dem_label',
                       'center_priv_res_label',
                       'center_reason1_label',
                       'center_reason2_label',
                       'center_result1_label',
                       'center_result2_label']
        self.buttons_left = [['Clean', self.remove_all],
                             ['Path', self.path_find],
                             ['Reload', self.reload],
                             ['Save', self.save_data]]
        self.buttons_txt = {}

        self.option_add('*tearOff', 'false')

        menu_dict = {'01File':[['Comand1', lambda:print('cmd1')],
                               ['Comand2', lambda:print('cmd2')],
                               ['Comand3', lambda:print('cmd3')],
                               ['Comand4', lambda:print('cmd4')],
                               ['Quit', self.destroy]],
                     '02Edit':[['Comand1', lambda:print('cmd1')],
                               ['Comand2', lambda:print('cmd2')],
                               ['Comand3', lambda:print('cmd3')],
                               ['Comand4', lambda:print('cmd4')],
                               ['Comand5', lambda:print('cmd5')]],
                     '03Options':[['Comand2', lambda:print('cmd1')],
                                  ['Comand2', lambda:print('cmd2')],
                                  ['Comand3', lambda:print('cmd3')],
                                  ['Comand4', lambda:print('cmd4')],
                                  ['Comand5', lambda:print('cmd5')]],
                     '04Windows':[['Show text widget', self.side_window_open],
                                  ['Comand2', lambda:print('cmd2')],
                                  ['Comand3', lambda:print('cmd3')],
                                  ['Comand4', lambda:print('cmd4')],
                                  ['Comand5', lambda:print('cmd5')]],
                     '05About':[['Comand1', lambda:print('cmd1')],
                                ['Comand2', lambda:print('cmd2')],
                                ['Comand3', lambda:print('cmd3')],
                                ['Comand4', lambda:print('cmd4')],
                                ['Comand5', lambda:print('cmd5')]]}
        top_menu = TopMenu(self, menu_dict)
        
        for i in self.frames:
                self.frames[i]['f_padx'] = 1
                self.frames[i]['f_pady'] = 1
        self.make_all_widgets()

    def make_all_widgets(self):
        #Frames       
        self.make_frames(self.frames, self.frames_names)
        ###
        #Center text containers
        for labl,ttn in zip(self.labels, self.c_txt_n):
            self.make_lb_text(frames_dict=self.frames, parent_lb_name=labl,
                              parent_txt_name=ttn, border1=7, border2=-6,
                              buttons_holder=self.buttons_txt)
            self.texts[ttn].bind('<Control-igrave>',
                                  lambda event, ttn=ttn:self.special_insert_db(ttn,
                                                                               self.texts[ttn]))
        ###
        #Buttons
        self.buttons = self.make_buttons(parent=self.frames['right_bar_buttons']['f_object'],
                                         buttons_list=self.buttons_left,
                                         width=5)
        self.buttons['Renew'] = tk.Button(master=self.frames['left_bar_tree_buttons']['f_object'],
                                          text='Renew',
                                          command=lambda:self.tree_renew(self.tree),
                                          width=5)
        self.buttons['Renew'].pack(side='right', expand='no', fill='none', anchor='w')
        if not self.db_connection:
            for key in ['Reload', 'Save', 'Renew']:
                self.buttons[key]['state']='disabled'
        ###
        #Center information labels
        tk.Label(master=self.frames['center_connect_label_holder']['f_object'],
                 text='Connection:', relief='flat', bg='pink', bd=1,
                 width=10).pack(side='left', expand='no',fill='none')
        self.DB_C = tk.Label(master=self.frames['center_connect_label_holder']['f_object'],
                             text='DB is not connected', relief='raised', bd=1)
        self.DB_C.pack(side='right', expand='yes', fill='x', padx=1)
        
        tk.Label(master=self.frames['center_inf_label_holder']['f_object'],
                 text='Path:', relief='flat', bg='pink', bd=1,
                 width=10).pack(side='left', expand='no', fill='none')
        self.inf = tk.Label(master=self.frames['center_inf_label_holder']['f_object'],
                            textvar=self.path, relief='raised', bd=1)
        self.inf.pack(side='right', expand='yes', fill='x', padx=1)
        ###
        #Right-bottom information labels
        self.act_count = tk.Label(master=self.frames['right_bar_label']['f_object'],
                                  textvar=self.show_acts_count, relief='raised', bd=1)
        self.act_count.pack(side='bottom', fill='x', padx=1)
        
        tk.Label(master=self.frames['right_bar_label']['f_object'],
                 text='acts\nin DB:', relief='raised',
                 bd=1).pack(side='bottom', fill='x', padx=1)
        ###
        #Left bar
        self.tree = self.making_tree(parent=self.frames['left_bar_tree']['f_object'])
        print('this is self.tree:  '+str(self.tree))
        ###

    def making_tree(self, parent, columns=['Value'], scrolls='both'):
        tree = self.make_tree(parent, columns=columns, scrolls=scrolls)
        tree.column('#0', width=100)
        tree.heading('#0', text='Key')
        return tree

    def side_window_open(self):
        side_window = sw.SideWindow(master=self)
        side_window.title('Side window for text processing')

    def tree_renew(self, tree_var):
        print('this is tree_var:  '+str(tree_var))
        counter = 1
        db = shelve.open(self.path.get(), flag='w')
        if self.tree_view:
            for i in db.keys():
                try: tree_var.delete(i)
                except: pass
        print('Open!')
        tree_var.insert('', 'end', 'total_acts_num', text='total_acts_num')
        tree_var.set('total_acts_num', 'Value', db['total_acts_num'])
        tree_var.insert('', 'end', 'total_all_acts', text='total_all_acts')
        tree_var.set('total_all_acts', 'Value', (str(db['total_all_acts'])[:30]+'...'))
        for act in sorted(db.keys())[:-2]:
            tree_var.insert('', 'end', act, text=act)
            for val in sorted(db[act].keys()):
                key = self.key_gen(string=val, counter=counter)
                tree_var.insert(act, 'end', key, text=val, tag=key)
                tree_var.set(key, 'Value', (db[act][val][:30]+'...'))
                tree_var.tag_bind(key, '<1>',
                                  lambda event: print('this is it! ',
                                                      tree_var.selection()[0],
                                                      tree_var.parent(tree_var.selection()[0])))
                tree_var.tag_bind(key, '<Double-1>',
                                  lambda event: self.value_edit(tree_var.parent(tree_var.selection()[0]),
                                                                tree_var.selection()[0]))
                counter+=1
        db.close()
        self.tree_view = True

    def path_find(self):
        def allocate(text, widget_var):
            path = text.get(index1='1.0', index2='end-1c')+'\ActsProcess'
            self.path.set(path)
            self.db_connection = True
            self.DB_C['text']='Connection is established'
            try:
                db = shelve.open(path, flag='w')
                db.close()
            except:
                with shelve.open(path, flag='c') as db:
                    db['total_all_acts']=set()
                    db['total_acts_num'] = self.acts_counter
            for key in ['Reload', 'Save', 'Renew']:
                self.buttons[key]['state']='normal'
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

    def reload(self):
        with shelve.open(self.path.get()) as db:
            self.acts_counter = db['total_acts_num']
            self.show_acts_count.set(str(self.acts_counter))
        

    def save_data(self):
        store = {}
        acts_name_holder = None
        for i in self.c_txt_n:
                self.texts[i].config(state='normal', bg='white')
                store[i[7:-4]] = self.texts[i].get(index1='1.0', index2='end-1c').rstrip()
        db = shelve.open(self.path.get(), flag='w')
        print(store['actname'])
        if store['actname'] in db['total_all_acts']:
            print('--\nAct\'s name\n{}\nis already in acts\' index\n--'.format(store['actname']))
        elif store['actname']=='':
            print('--\nAct\'s name is not set\n--')
        else:
            db['total_acts_num']+=1
            self.acts_counter +=1
            key = self.key_gen(string='act_', counter=self.acts_counter)
            db[key]=store
            acts_name_holder = db['total_all_acts']
            acts_name_holder.add(store['actname'])
            db['total_all_acts'] = acts_name_holder
        db.close()
        for key in self.buttons_txt.keys():
            for button in ['Confirm', 'Del']:
                self.buttons_txt[key][button]['state']='normal'
        for key in self.texts.keys():
            self.texts[key].config(state='normal', bg='white')
        self.remove_all()
        self.show_acts_count.set(str(self.acts_counter))
        self.tree_renew(self.tree)

    def value_edit(self, key_act, key_part):
        print(key_act, key_part)
        key_part=key_part[:-6]
        def save_edited(widget_var, text_var, key_act, key_part):
            print('\n--\nenter editing!')
            new_val = text_var.get(index1='1.0', index2='end-1c')
            print('new val =   ' + new_val)
            with shelve.open(self.path.get(), flag='w') as db:
                holder = db[key_act]
                holder[key_part]=new_val
                db[key_act]=holder
                print('Value Saved')
                print (db[key_act][key_part])
            self.tree_renew(self.tree)
            self.tree.see(key_act)
            self.tree.item(key_act, open='true')
            widget_var.destroy()
        name_string = ' {0} :: {1}'.format(key_act, key_part)
        new_window = self.new_win(title=('Editing '+name_string))
        frame1 = tk.Frame(new_window, relief='sunken', bd=1)
        frame2 = tk.Frame(new_window)
        frame3 = tk.Frame(new_window, relief='sunken', bd=1)
        frame1.pack(side='top', expand='no', fill='x', padx=1, pady=1)
        frame2.pack(side='top', expand='yes', fill='both', padx=1, pady=1)
        frame3.pack(side='top', expand='no', fill='x', padx=1, pady=1)
        text = self.make_lb_text(parent_lb_name=frame1, parent_txt_name=frame2,
                                 store=False, wdg_label=name_string,
                                 border1=7, border2=-6, widget_width=80)
        text.bind('<Control-igrave>', lambda event:self.special_insert_db(text))
        with shelve.open(self.path.get(), flag='w') as db:
            text.insert(index='1.0', chars=db[key_act][key_part])
        tk.Button(master=frame3,
                  text='Save',
                  command=lambda:save_edited(new_window, text, key_act, key_part)).pack(side='left', fill='x')
        tk.Button(master=frame3,
                  text='Quit',
                  command=new_window.destroy).pack(side='right', fill='x')
    
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

############################################################
Main().mainloop()
