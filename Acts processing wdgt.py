from tkguilib import *
import shelve

class Main(GUI_Manager):
    def __init__(self, *args, **kwargs):
        GUI_Manager.__init__(self, *args, **kwargs)
        self.title('Acts parsing DB client')
        self.db_connection = False
        self.acts_counter = 0
        self.show_acts_count = tk.StringVar()
        self.show_acts_count.set(self.acts_counter)
        self.path = tk.StringVar()
        self.path.set('Undefined')
        self.tree_view = False
        
        self.texts = {}
        
        self.frames_names = ['buffer', 'left_bar', 'left_bar_tree', 'left_bar_tree_buttons',
                             'center', 'right_bar', 'right_bar_label',
                             'right_bar_holder', 'right_bar_buttons',
                             'center_connect_label_holder',
                             'center_inf_label_holder',
                             'center_actname_holder', 'center_actname_label',
                             'center_actname_txt', 'center_dem_holder',
                             'center_dem_label', 'center_dem_txt',
                             'center_reason1_holder', 'center_reason1_label',
                             'center_reason1_txt', 'center_reason2_holder',
                             'center_reason2_label', 'center_reason2_txt',
                             'center_result1_holder', 'center_result1_label',
                             'center_result1_txt', 'center_result2_holder',
                             'center_result2_label', 'center_result2_txt']
        
        self.frames = {}
        self.frames['buffer'] = {'f_object':tk.Frame(master=self)}
        self.frames['left_bar'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                   'f_side':'left', 'f_expand':'no', 'f_fill':'y'}
        self.frames['left_bar_tree'] = {'f_object':tk.Frame(master=self.frames['left_bar']['f_object']),
                                        'f_side':'top', 'f_expand':'no', 'f_fill':'y'}
        self.frames['left_bar_tree_buttons'] = {'f_object':tk.Frame(master=self.frames['left_bar']['f_object']),
                                                'f_side':'left', 'f_expand':'no', 'f_fill':'y'}
        self.frames['center'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                 'f_side':'left'}
        self.frames['right_bar'] = {'f_object':tk.Frame(master=self.frames['buffer']['f_object']),
                                    'f_side':'left', 'f_expand':'no', 'f_fill':'y', 'f_relief':'sunken', 'f_bd':1}
        self.frames['right_bar_holder'] = {'f_object':tk.Frame(master=self.frames['right_bar']['f_object']),
                                           'f_expand':'yes', 'f_fill':'y'}
        self.frames['right_bar_buttons'] = {'f_object':tk.Frame(master=self.frames['right_bar_holder']['f_object'])}
        self.frames['right_bar_label'] = {'f_object':tk.Frame(master=self.frames['right_bar_holder']['f_object']),
                                          'f_expand':'no', 'f_side':'bottom'}
        self.frames['center_connect_label_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object']),
                                                      'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['center_inf_label_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object']),
                                                  'f_side':'top', 'f_expand':'no', 'f_fill':'x'}
        self.frames['center_actname_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_actname_label'] = {'f_object':tk.Frame(master=self.frames['center_actname_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_actname_txt'] = {'f_object':tk.Frame(master=self.frames['center_actname_holder']['f_object'])}
        self.frames['center_dem_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_dem_label'] = {'f_object':tk.Frame(master=self.frames['center_dem_holder']['f_object']),
                                           'f_expand':'no', 'f_fill':'x'}
        self.frames['center_dem_txt'] = {'f_object':tk.Frame(master=self.frames['center_dem_holder']['f_object'])}
        self.frames['center_reason1_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_reason1_label'] = {'f_object':tk.Frame(master=self.frames['center_reason1_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_reason1_txt'] = {'f_object':tk.Frame(master=self.frames['center_reason1_holder']['f_object'])}
        self.frames['center_reason2_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_reason2_label'] = {'f_object':tk.Frame(master=self.frames['center_reason2_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_reason2_txt'] = {'f_object':tk.Frame(master=self.frames['center_reason2_holder']['f_object'])}
        self.frames['center_result1_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_result1_label'] = {'f_object':tk.Frame(master=self.frames['center_result1_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_result1_txt'] = {'f_object':tk.Frame(master=self.frames['center_result1_holder']['f_object'])}
        self.frames['center_result2_holder'] = {'f_object':tk.Frame(master=self.frames['center']['f_object'])}
        self.frames['center_result2_label'] = {'f_object':tk.Frame(master=self.frames['center_result2_holder']['f_object']),
                                               'f_expand':'no', 'f_fill':'x'}
        self.frames['center_result2_txt'] = {'f_object':tk.Frame(master=self.frames['center_result2_holder']['f_object'])}

        self.txt_n = ['center_actname_txt',
                      'center_dem_txt',
                      'center_reason1_txt',
                      'center_reason2_txt',
                      'center_result1_txt',
                      'center_result2_txt']
        labels = ['center_actname_label',
                  'center_dem_label',
                  'center_reason1_label',
                  'center_reason2_label',
                  'center_result1_label',
                  'center_result2_label']
        buttons_left = [['Clean', self.remove_all],
                        ['Path', self.path_find],
                        ['Reload', self.reload],
                        ['Save', self.save_data]]
        
        for i in self.frames:
                self.frames[i]['f_padx'] = 1
                self.frames[i]['f_pady'] = 1
                
        self.make_frames(self.frames, self.frames_names)
        
        for i in self.txt_n:
            if 'actname' not in i:
                self.texts[i] = self.make_text_with_scroll(parent=self.frames[i]['f_object'],
                                                           widget_height=5)
                self.binding_insert(self.texts[i])
            else:
                self.texts[i] = self.make_text_with_scroll(parent=self.frames[i]['f_object'],
                                                           widget_height=3)
                self.binding_insert(self.texts[i])
        
        for i in labels:
            self.frames[i]['f_object'].config(relief='sunken', bd=1)
        for i in labels:
            tk.Label(master=self.frames[i]['f_object'], text=i[7:-6]).pack(side='left')
            
        for i in zip(labels, self.txt_n):
            label, txt_n = i
            buttons_txt = [['Del', lambda txt_n=txt_n:self.texts[txt_n].delete(index1='1.0', index2='end')],
                           ['Edit', lambda txt_n=txt_n:self.texts[txt_n].config(state='normal', bg='white')],
                           ['Confirm', lambda txt_n=txt_n:self.texts[txt_n].config(state='disabled', bg='#d4d0c8')]]
            self.make_buttons(parent=self.frames[label]['f_object'],
                              buttons_list=buttons_txt,
                              side='right')
        #Buttons
        self.buttons = self.make_buttons(parent=self.frames['right_bar_buttons']['f_object'],
                                         buttons_list=buttons_left,
                                         width=5)
        ###

        #Center information labels
        tk.Label(master=self.frames['center_connect_label_holder']['f_object'],
                 text='Connection:', relief='raised', bd=1, width=10).pack(side='left',
                                                                           expand='no',
                                                                           fill='none')
        self.DB_C = tk.Label(master=self.frames['center_connect_label_holder']['f_object'],
                             text='DB is not connected', relief='raised', bd=1)
        self.DB_C.pack(side='right', expand='yes', fill='x', padx=1)
        
        tk.Label(master=self.frames['center_inf_label_holder']['f_object'],
                 text='Path:', relief='raised', bd=1, width=10).pack(side='left',
                                                                     expand='no',
                                                                     fill='none')
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
        
        self.buttons['Renew'] = tk.Button(master=self.frames['left_bar_tree_buttons']['f_object'],
                                          text='Renew',
                                          command=lambda:self.tree_renew(self.tree),
                                          width=5)
        self.buttons['Renew'].pack(side='top', expand='no', anchor='w')
        ###
        if not self.db_connection:
            for key in ['Reload', 'Save', 'Renew']:
                self.buttons[key]['state']='disabled'

    def making_tree(self, parent, columns=['Value'], scrolls='both'):
        tree = self.make_tree(parent, columns=columns, scrolls=scrolls)
        tree.column('#0', width=100)
        tree.heading('#0', text='Key')
        #try:
            #db = shelve.open(self.path.get(), flag='w')
            #tree.insert('', 'end', 'total_acts_num', text='total_acts_num')
            #tree.set('total_acts_num', 'Value', db['total_acts_num'])
            #tree.insert('', 'end', 'total_all_acts', text='total_all_acts')
            #tree.set('total_all_acts', 'Value', (str(db['total_all_acts'])[:30]+'...'))
            #tree.insert('', 'end', 'total_acts_num', text='total_acts_num')
            #tree.set('total_acts_num', columns[i], db['total_acts_num'])
            #for act in sorted(db.keys())[:-1]:
            #    tree.insert('', 'end', act, text=act)
            #    for key in sorted(db[act].keys()):
            #        tree.insert(act, 'end', key, text=key)
            #        tree.set(key, columns[i], (db[act][key][:30]+'...'))
            #db.close()
            #print('this is left-hand tree:  '+str(tree))
            #return tree
        #except:
        return tree
            

    def tree_renew(self, tree_var):
        print('this is tree_var:  '+str(tree_var))
        counter = 0
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
            for key in sorted(db[act].keys()):
                tree_var.insert(act, 'end', key+str(counter), text=key)
                tree_var.set(key+str(counter), 'Value', (db[act][key][:10]+'...'))
                counter+=1
        db.close()
        self.tree_view = True

    def remove_all(self):
        for i in self.txt_n:
            self.texts[i].delete(index1='1.0', index2='end')

    def path_find(self):
        new_window = self.new_win(title='Enter path to database')
        container_text = tk.Frame(new_window)
        container_buttons = tk.Frame(new_window)
        container_text.pack(side='top')
        container_buttons.pack(side='top', fill='x')
        text = self.make_text_with_scroll(parent=container_text, widget_height=3)
        self.binding_insert(text)
        tk.Button(master=container_buttons,
                  text='Allocate',
                  command=lambda:self.allocate(text, new_window)).pack(side='left', fill='x')
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
        for i in self.txt_n:
                self.texts[i].config(state='normal', bg='white')
                store[i[7:-4]] = self.texts[i].get(index1='1.0', index2='end-1c').rstrip()
        #try:
        db = shelve.open(self.path.get(), flag='w')
        #    db_exist = True
        #except:
        #   db = shelve.open(self.path.get(), flag='c')
        #    db_exist = False
        #if db_exist:
        print(store['actname'])
        if store['actname'] in db['total_all_acts']:
            print('Act name\n{}\nis already in acts\' index'.format(store['actname']))
        else:
            db['total_acts_num']+=1
            self.acts_counter +=1
            db[('act_'
                +('0'*(6-len(str((self.acts_counter)))))
                +str(self.acts_counter))]=store
            acts_name_holder = db['total_all_acts']
            acts_name_holder.add(store['actname'])
            db['total_all_acts'] = acts_name_holder
        #else:
        #    print(store['actname'])
        #    db = shelve.open(self.path.get(), flag='c')
        #    db['total_all_acts']=set()
        #    db['total_acts_num'] = self.acts_counter
        #    db['total_acts_num']+=1
        #    self.acts_counter +=1
        #    db[('act_'
        #        +('0'*(6-len(str((self.acts_counter)))))
        #        +str(self.acts_counter))]=store
        #    db['total_all_acts'].add(store['actname'])
        db.close()
        self.show_acts_count.set(str(self.acts_counter))
        self.tree_renew(self.tree)

    def allocate(self, text, widget_var):
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

############################################################
Main().mainloop()
