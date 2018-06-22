from datetime import datetime as dt
import tlboxes as tlb
import tkinter as tk
from tkinter import ttk
import random as rd
import shelve as shl
from sys import version_info
import time
import act_sep as acts

PyVer = version_info[1]

coding_chars = ['A', 'B', 'C',
                'D', 'E', 'F',
                'G', 'H', 'I',
                'J', 'K', 'L',
                'M', 'N', 'O',
                'P', 'Q', 'R',
                'S', 'T', 'U',
                'V', 'W', 'X',
                'Y', 'Z', '0',
                '1', '2', '3',
                '4', '5', '6',
                '7', '8', '9',
                'a', 'b', 'c',
                'd', 'e', 'f',
                'g', 'h', 'i',
                'j', 'k', 'l',
                'm', 'n', 'o',
                'p', 'q', 'r',
                's', 't', 'u',
                'v', 'w', 'x',
                'y', 'z']

class Connection():
    def __init__(self, file_name=None, path=None):
        self.db_exists = False
        if not file_name:
            file_name='SimpleBase'
        if not path:
            try:
                open('C:\\Python3{}\\test.txt'.format(PyVer))
                self.path = 'C:\\Python3{}\\AP'.format(PyVer) + '\\' + file_name
            except:
                self.path = 'AP\\' + file_name
        else:
            self.path= (path + '\\' + file_name)
        try:
            db = shl.open(self.path, flag='w')         
        except:
            db = shl.open(self.path, flag='c')
        db.close()
        self.db_exists = True
        self.store_acts()

    def store_acts(self):
        '''Start-up function. Check if there is already a db file. If not
        create a new db template.
        Internal function
        '''
        with shl.open(self.path, flag='w') as db:
            if 'all_acts' in db.keys():
                print('Acts are already stored')
            else:
                buffer = acts.ActSep(my_path=('C:\Python3{}\AP'.format(PyVer)
                                              + '\АС МО 1023 '
                                              + '2017-2303-0106.txt'))
                divided_acts = buffer.store
                db['tags'] = {}
                db['all_acts'] = divided_acts
                db['acts_keys'] = []
                db['opened_acts'] = []
                db['marked_acts'] = {}
                print('Acts are stored')

    def extract_all_acts(self):
        with shl.open(self.path, flag='w') as db:
            all_acts = db['all_acts']
        return all_acts

    def extract_marked_acts(self):
        with shl.open(self.path, flag='w') as db:
            marked_acts = db['marked_acts']
        return marked_acts

    def db_info(self):
        '''Print into the console all info about first-level db keys
        including their values.
        External function
        ================================================
        INTERFACE: run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db:
            acts_left = len(db['all_acts'])
            acts_opened = len(db['opened_acts'])
            acts_marked = len(db['marked_acts'])
        print('Acts in total: {}\n'.format(acts_marked+acts_left)
              +'Opened acts: {}\n'.format(acts_opened)
              +'Marked acts: {}\n'.format(acts_marked)
              +'Acts left: {}'.format(acts_left))

    def make_id(self):
        '''Create uniq act key and store it into the list in the db.
        External-Internal subfunction.
        =======================================================
        INTERFACE: can be run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db: 
            sample = rd.sample(coding_chars, 5)
            code = ''.join(sample)
            now = str(dt.now())[:-4].replace(' ', '_')
            key = now + '_doc::' + code
            lst = db['acts_keys']
            lst.append(key)
            db['acts_keys'] = lst
        print(key)
        return key

    def extract_keys(self):
        '''Collect all first-level db keys into the sorted list
        External function
        ================================================
        INTERFACE: run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db:
            keys = sorted(db.keys())
        return keys
        
    def save_all(self, all_acts, marked_acts, opened_acts):
        '''Save all information after processing to the db file.
        External function
        ================================================
        INTERFACE: run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db:
            db['all_acts'] = all_acts
            marked = db['marked_acts']
            opened = db['opened_acts']
            marked.update(marked_acts)
            opened.extend(opened_acts)
            db['marked_acts'] = marked
            db['opened_acts'] = opened
        print('База данных обновлена!')

    def tags_extraction(self):
        '''Extract all tags and tag information from the db to dictionary object
        and return the object to be procecced.
        External function
        ================================================
        INTERFACE: run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db:
            tags = db['tags']
        if not tags:
            print ('There are no tags!')
        return tags

    def tags_changer(self, tags_dict):
        '''Take updated tag information from the GUI and stor it to the db.
        Extarnal-Internal function.
        ================================================
        INTERFACE: run through the button press from GUI
        '''
        with shl.open(self.path, flag='w') as db:
            db['tags'] = tags_dict

class TopMenu():
    def __init__(self, tkparent=None, names_commands_dict=None):
        self.nc_dict = names_commands_dict
        self.tkparent = tkparent
        self.menu = tk.Menu(master=self.tkparent, tearoff=False)
        self.tkparent['menu']=self.menu
        self.topline = self.make_menu_topline()
        self.cascades = self.make_menu_cascade()

    def make_menu_topline(self):
        store = {}
        for name in sorted(self.nc_dict.keys()):
            store[name] = tk.Menu(master=self.menu)
            self.menu.add_cascade(menu=store[name], label=name[2:])
        return store

    def make_menu_cascade(self):
        for i in sorted(self.nc_dict.keys()):
            for j in range(len(self.nc_dict[i])):
                self.topline[i].add_command(label=self.nc_dict[i][j][0],
                                            command=self.nc_dict[i][j][1])

class CustomTextWidget(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, wrap='word', **kwargs)
        #self.tag_configure('center', justify='left')
        #self.tag_add('center', 1.0, 'end')

        #The following below code was taken from:
        #http://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget

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

class GUI():
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.con = Connection()
        self.tags_dict = self.con.tags_extraction()
        '''==========================================='''
        '''INTERFACE: see Connection.tags_extraction()'''
        self.tags = sorted(self.tags_dict.keys())
        print('all tags: ', self.tags)
        print('all keys: ', self.con.extract_keys())
        '''========================================'''
        '''INTERFACE: see Connection.extract_keys()'''
        self.all_acts = self.con.extract_all_acts()
        '''============================================'''
        '''INTERFACE: see Connection.extract_all_acts()'''
        self.marked_acts = self.con.extract_marked_acts()
        '''==============================================='''
        '''INTERFACE: see Connection.extract_marked_acts()'''
        self.opened_acts = [] #Opened acts holder
        self.current_tag = None #selected tag holder
        self.act_key = None #key holder
        self.info_var = tk.StringVar()
        self.info_var.set('Информация: '
                           +'действия не производились')
        self.tlb = None #Listboxes holder
        self.txthg_val = 12 #Text high value holder
        self.menu = TopMenu(tkparent=self.root,
                            names_commands_dict={
                                '01Главная':[['Выйти', self.all_quit]],
                                '02Опции':[['Показать теги', self.show_tags]]})
        self.make_widgets(self.root)

    def make_widgets(self, main_parent):
        buttons_list = [['Красная строка', self.red_row],
                        ['Удалить текст', self.del_all_text],
                        ['Текущий тег', self.show_cur_tag],
                        ['Заливка разметки', self.light_text],
                        ['Сохранить изменения', self.save_one],
                        ['Сохранить все в БД', self.save_all],
                        ['Напечатать ключи', self.print_keys],
                        ['Следующий акт',
                         lambda: self.open_act(None, mode='b')],
                        ['Информация о БД', self.show_db_info]]
        _, right_bar = self.stand_alone_buttons(main_parent,
                                                buttons_list,
                                                container_pack_options={
                                                    'side':'right',
                                                    'expand':'no',
                                                    'fill':'y'})
        self.ent = self.wdgt_label_bt(main_parent,
                                      tk.Entry,
                                      ('Введите: ИМЯ_ТЕГА'
                                       +' - описание тега'),
                                      wdgt_options={'width':50},
                                      container_pack_options={'side':'top',
                                                              'expand':'no',
                                                              'anchor':'w'})
        self.ent.bind('<Return>', self.append_tag)
        self.text, container = self.scrolled_text(main_parent,
                                                  custome_text_wdgt_flag=True)
        #self.text.bind('<Control-igrave>', lambda event: \
        #               self.text.insert\
        #               ('1.0', chars=self.root.selection_get\
        #               (selection = "CLIPBOARD")))
        for pair in [['red', 'ff0000'], ['yellow', 'ff8700'],
                     ['green', '5a8700'], ['brown', '5a1d00'],
                     ['purple', '7b2dfb'], ['blue', '5adeeb'],
                     ['pink', 'aabceb'], ['blue2', '94aceb'],
                     ['green2', '04f226'], ['red2', 'ee3e26'],
                     ['grey', 'bb5f7b'], ['gold', '93a310'],
                     ['orange', 'f7a310'], ['purple2', 'b1a3cf'],
                     ['grey2', 'c1c3d4'], ['purple3', '8e44e6'],
                     ['blue3', '8ef1e6'], ['green3', '00ff00']]:
            name, color = pair
            color = '#'+color
            self.text.tag_configure(name, background=color)
        self.text.tag_configure('bigfont', font=('Times New Roman',
                                                 self.txthg_val,
                                                 'bold'))
        self.text.tag_add('bigfont', '1.0', 'end')
        #self.text.tag_configure("green", background="#00ff00")
        self.wdgt_label_bt(main_parent, container,
                           'Главное окно',
                           scrolled_text_flag=True,
                           container_pack_options={'side':'top',
                                                   'expand':'no',
                                                   'anchor':'w'})
        self.txthg = self.wdgt_label_bt(main_parent, ttk.Combobox,
                                        'Выберите размер шрифта',
                                        container_pack_options={'side':'top',
                                                                'expand':'no',
                                                                'anchor':'e'})
        self.txthg.bind('<<ComboboxSelected>>', self.txthg_selection)
        self.txthg['values'] = list(range(8, 33, 2))
        self.combo = self.wdgt_label_bt(main_parent, ttk.Combobox,
                                        'Выберите наименование тега',
                                        container_pack_options={'side':'top',
                                                                'expand':'no',
                                                                'anchor':'w'})
        self.combo.bind('<<ComboboxSelected>>', self.combo_selection)
        self.combo['values'] = self.tags
        sub_menu = tk.Frame(main_parent, pady=1)
        sub_menu.pack(side='top', anchor='w')
        tk.Button(sub_menu,
                  text='Подробно',
                  command=self.full_info).pack(side='left',
                                               anchor='w')
        tk.Button(sub_menu,
                  text='Удалить тег',
                  command=self.del_tag).pack(side='left',
                                             anchor='w')
        tk.Button(sub_menu,
                  text='Добавить горячую клавишу',
                  command=self.append_hotkey).pack(side='left',
                                             anchor='w')        
        tk.Label(main_parent,
                 textvar=self.info_var,
                 relief='sunken',
                 bd=1,
                 bg='pink').pack(side='top',
                                 anchor='w',
                                 pady=1)
        self.tlb = tlb.TwoListBoxes(parent=right_bar,
                                    widgets_orient='ver',
                                    data1 = ['act '+str(i) for i
                                             in range(len(self.all_acts))],
                                    data2 = sorted(self.marked_acts.keys()))
        self.tlb.lb1.bind('<Double-1>', lambda event: \
                          self.open_act(event, mode='c'))
        self.tlb.lb2.bind('<Double-1>', self.extract_marked_act)
        self.binding()
        
    def wdgt_label_bt(self,
                      main_parent,
                      tk_obj,
                      label_name,
                      buttons_list=None,
                      container_pack_options=None,
                      holder_wdgt_pack_options=None,
                      wdgt_options=None,
                      wdgt_pack_options=None,
                      scrolled_text_flag=False):
        #Container:
        container = tk.Frame(main_parent)
        if not container_pack_options:
            container.pack(side='top', expand='yes', fill='both')
        else:
            container.pack(**container_pack_options)
        #Holder_label_buttons:
        holder_label_buttons = tk.Frame(container)
        holder_label_buttons.pack(side='top', expand='no', fill='x')
        #Holder_wdgt_1:
        if not scrolled_text_flag:
            holder_wdgt = tk.Frame(container)
            if not holder_wdgt_pack_options:
                holder_wdgt.pack(side='top', expand='yes', fill='both')
            else:
                holder_wdgt.pack(**holder_wdgt_pack_options)
            #Wdgt
            wdgt = tk_obj(holder_wdgt)
            if wdgt_options:
                wdgt.config(**wdgt_options)
            if not wdgt_pack_options:
                wdgt.pack(side='left')
            else:
                wdgt.pack(**wdgt_pack_options)
        #Holder_wdgt_2:
        else:
            holder_wdgt = tk_obj #tk.Frame container
            if not holder_wdgt_pack_options:
                holder_wdgt.pack(side='top', expand='yes', fill='both')
            else:
                holder_wdgt.pack(**holder_wdgt_pack_options)
        #Label:
        label = tk.Label(holder_label_buttons, text=label_name)
        label.pack(side='left', expand='no', fill='x')
        #Buttons:
        if buttons_list:
            buttons_dictionary = {}
            for name, command in buttons_list:
                buttons_dictionary[name] = tk.Button(holder_label_buttons,
                                                    text=name,
                                                    command=command)
                buttons_dictionary[name].pack(side='right')
        #Ending:
        if not scrolled_text_flag:
            if buttons_list:
                return wdgt, buttons_dictionary
            else:
                return wdgt
        else:
            if buttons_list:
                return buttons_dictionary
            else:
                return 0
        

    def scrolled_text(self,
                      main_parent,
                      custome_text_wdgt_flag=False):
        container = tk.Frame(main_parent)
        scroll_bar = tk.Scrollbar(container)
        if not custome_text_wdgt_flag:
            tk_obj = tk.Text(container, wrap='word')
        else:
            tk_obj = CustomTextWidget(container)
        scroll_bar.config(command=tk_obj.yview)
        tk_obj.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side='right', fill='y')
        tk_obj.pack(side='left', expand='yes', fill='both')
        return tk_obj, container

    def stand_alone_buttons(self,
                            main_parent,
                            buttons_list,
                            button_height=1,
                            button_width=25,
                            container_pack_options=None):
        container = tk.Frame(main_parent)
        if not container_pack_options:
            container.pack(side='right', expand='yes', fill='both')
        else:
            container.pack(**container_pack_options)
        buttons_dictionary = {}
        for name, command in buttons_list:
            buttons_dictionary[name] = tk.Button(container,
                                                 text=name,
                                                 command=command,
                                                 height=button_height,
                                                 width=button_width)
            buttons_dictionary[name].pack(side='top',
                                          expand='no',
                                          fill='x',
                                          anchor='w')
        return buttons_dictionary, container

#########
#########
    
    def all_quit(self):
        '''Exit from program, destroy all widgets.
        Top menu command.
        '''
        self.root.destroy()

    def append_hotkey(self):
        '''Bind ciryllian key with selected tag. Use ALT+hotkey combination
        to insert tag.
        Bottom bar's button command.                
        '''
        new_win = self.new_win(self.root,'Ввод значения горячей клаивиши')
        tk.Label(new_win,
                 text='Нажмите клавишу в русской раскладке',
                 width=40,
                 height=10,
                 bg='pink').pack(expand='yes', fill='both')
        new_win.bind('<KeyPress>', self.write_to_var)
        #new_win.destroy()

    def append_tag(self, event):
        '''Collect tag name and description from Entry widget
        from the top bar entry row. Alter self.current_tag var value.
        Change tags in db file
        Internal binded function.
        ========================================
        INTERFACE: see Connection.tags_changer()
        '''
        new_tag = self.ent.get().split(' - ')
        if len(new_tag) != 2:
            self.info_changer('не соблюден формат ввода тега!')
        else:
            if new_tag[0] not in self.tags_dict.keys():
                self.tags_dict[new_tag[0]] = [new_tag[1]]
                self.con.tags_changer(self.tags_dict)
                self.tags = sorted(self.tags_dict.keys())
                self.combo['values'] = self.tags
                self.combo.set(new_tag[0])
                self.ent.delete('0', 'end')
                self.info_changer('добавлен новый тег: '
                                  +'{} - {}'.format(*new_tag))
            else:
                self.ent.delete('0', 'end')
                self.combo.set(new_tag[0])
                self.info_changer('установлен тег: '
                                  +'{} - {}'.format(*new_tag))
            self.current_tag = new_tag[0]

    def binding(self):
        '''Starts at the begining of program execution.
        Binds tags from uploaded dictionary with associated hotkeys.
        Internal function. Uses self.custom_insert(...) as subfunction.
        '''
        if self.tags_dict:
            for key in self.tags_dict.keys():
                try:
                    print(self.tags_dict[key][1])
                    self.text.bind('<Alt-{}>'.format(self.tags_dict[key][1]),
                                   lambda event, \
                                   key=key: self.custome_insert(event, key))
                except:
                    pass
        else:
            print('No hotkeys for binding!')

    def combo_selection(self, event):
        '''Watch for ComboBox widget alteration to upload currently selected tag
        to programm reserved variable. Alter self.current_tag var value.
        Internal binded function.
        '''
        tag = self.combo.get()
        self.info_changer("выбран тег '{}'".format(tag))
        print ('selected: ' , tag)
        self.current_tag = tag

    def custome_insert(self, event, tag):
        '''Subfunction used for binding existing hotkeys with tags.
        Runs when the programm starts.
        Intrnal binded function.
        '''
        self.text.insert(index='sel.first', chars='<{} '.format(tag))
        self.text.insert(index='sel.last', chars=' /{}>'.format(tag))

    def del_all_text(self):
        '''Dels all text from the text window.
        Right bar's button command.
        '''
        text = self.text.get(index1='1.0', index2='end')
        if text and text != '\n':
            self.text.delete(index1='1.0', index2='end')
            self.info_changer('текст удален')
        else:
            self.info_changer('отсутствует текст для удаления')

    def del_tag(self):
        '''Dels tag selected by the ComboBox widget. Alter self.current_tag
        var value.
        Bottom bar's button command.
        ========================================
        INTERFACE: see Connection.tags_changer()
        '''
        tag = self.combo.get()
        if tag:
            description = self.tags_dict[tag][0]
            self.info_changer("тег '{} - ".format(tag)
                              +"{}' удален".format(description))
            self.tags_dict.pop(tag)
            self.con.tags_changer(self.tags_dict)
            self.tags = sorted(self.tags_dict.keys())
            self.combo['values'] = self.tags
            self.combo.set('')
            self.current_tag = ''
        else:
            self.info_changer('тег не выбран!')

    def extract_marked_act(self, event):
        selection = self.tlb.lb2.curselection()
        if selection:
            key = self.tlb.lb2.get(selection)
            self.act_key = key
            act = self.marked_acts[key]
            self.del_all_text()
            time.sleep(0.2)
            self.text.insert('1.0', act, ('bigfont',))
            self.info_changer('акт {} извлечен!'.format(key))
        else:
            pass

    def full_info(self):
        '''Print all information abbout the tag selected by the ComboBox widget
        in the iformation line at the bottom of the main frame.
        Bottom bar's button command.
        '''
        tag = self.combo.get()
        if tag:
            if len(self.tags_dict[tag]) < 2:
                self.info_changer("описание тега '{}': ".format(tag)
                                  +'{}; '.format(self.tags_dict[tag][0])
                                  +'горячая клавиша: отсутствует')
            elif len(self.tags_dict[tag]) == 3:
                self.info_changer("описание тега '{}': ".format(tag)
                                  +'{}; '.format(self.tags_dict[tag][0])
                                  +'горячая клавиша: '
                                  +'{}'.format(self.tags_dict[tag][2]))
            else:
                self.info_changer('ошибка определения горячей клавиши: '
                                  +'превышена длина списка для ключа '
                                  +'"tag" ({})'.format(tag))
        else:
            self.info_changer('тег не выбран!')

    def info_changer(self, string):
        '''Show current state information in the information line
        at the bottom of the main frame.
        Internal subfunction. It is used as subfunction by many functions.
        '''
        self.info_var.set('Информация: {}'.format(string))

    def light_text(self):
        '''Highlight the pattern in the text at the main text widget.
        Right bar's button command.
        '''
        #self.text.highlight_pattern('\<.+?\n*.*\n*.*\n*.*?\>', 'green3')
        for item in [['red', '01_NAME'], ['yellow', '02_DEM'],
                     ['green', '03_FIRST_COURT'], ['brown', '04_APPEAL'],
                     ['pink', '05_CAS_DEM'], ['blue', '06_DESCRP_END'],
                     ['purple', '07_REASON'], ['blue2', '08_REASON_END'],
                     ['green2', '09_RESULT'], ['red2', 'FIRST'],
                     ['gold', 'MAJOR'], ['grey', 'MINOR'],
                     ['orange', 'PRECISION'], ['purple2', 'REASON_MATERIAL'],
                     ['blue3', 'REASON_PROCEDURAL'], ['grey2', 'REPROCESS'],
                     ['purple3', 'REV_DEM'], ['green3', 'SPECIAL']]:
            color, tag = item
            self.text.highlight_pattern('\<{}.+?\n*.*\n*.*\n*.*?\>'.format(tag),
                                        color)
        self.info_changer('размеченный текст подсвечен')

    def new_win(self, main_parent, title):
        '''Create new window.
        Internal subfunction.
        '''
        new_window = tk.Toplevel(main_parent)
        new_window.title(title)
        return new_window

    def open_act(self, event, mode):
        '''Show next document stored in the db.
        Right bar's button command. LB1 list.
        =======================================
        INTERFACE: see Connection.make_id()
        '''
        if mode == 'b': #On button press
            self.del_all_text()
            time.sleep(0.2)
            act = self.all_acts.pop(0)
            key = self.con.make_id()
            self.text.insert('1.0', act, ('bigfont',))
            self.tlb.lb1.delete(0)
            self.tlb.lb2.insert('end', key)
            self.marked_acts[key] = act
            self.opened_acts.append(act)
            self.act_key = key
            self.info_changer('отображен новый акт!')
        elif mode == 'c': #On click
            self.del_all_text()
            time.sleep(0.2)
            selection = self.tlb.lb1.curselection()
            if selection: 
                print(selection)
                self.tlb.lb1.delete(selection)
                act = self.all_acts.pop(selection[0])
                key = self.con.make_id()
                self.text.insert('1.0', act, ('bigfont',))
                self.tlb.lb2.insert('end', key)
                self.marked_acts[key] = act
                self.opened_acts.append(act)
                self.act_key = key
                self.info_changer('отображен новый акт!')
            else:
                pass

    def print_keys(self):
        '''Print all db 1-level keys in the main text widget.
        Right bar's button command
        ========================================
        INTERFACE: see Connection.extract_keys()
        '''
        string = 'all keys:\n'
        counter = 0
        for key in self.con.extract_keys():
            string+=(key+'\n')
            counter+=1
        self.del_all_text()
        time.sleep(1)
        self.text.insert(index='1.0', chars=string)
        self.info_changer('напечатаны ключи; всего '
                          +'"{}" единиц(-ы)'.format(counter))

    def red_row(self):
        '''Create a 'rad row' indents in the text at the main text
        widget.
        Right bar's button command.
        '''
        text = self.text.get(index1='1.0', index2='end-1c')
        if text and text != '\n':
            string = ''
            counter = 0
            self.text.delete(index1='1.0', index2='end')
            splitted = text.split('\n')
            for i in range(len(splitted)):
                if splitted[i]:
                    string +=  (str(counter)
                                +(' '*(6-len(str(counter))))
                                +splitted[i]
                                +'\n')
                    counter += 1
                else:
                    string += str(counter) + '\n'
                    counter += 1
            self.text.insert('1.0', string, ('bigfont',))
            self.info_changer('добавлены красные строки и нумерация абзацев')
        else:
            self.info_changer('отсутствует текст для добавления красных строк')

    def save_all(self):
        '''Save information in self.marked_acts, self.opened_acts
        and self.all_acts variables to the db.
        =======================================
        INTERFACE: see Connection.save_all()
        '''
        self.con.save_all(self.all_acts, self.marked_acts, self.opened_acts)
        self.opened_acts = []
        self.info_changer('ВНИМАНИЕ! Изменения сохранены в файле Базы данных!')

    def save_one(self):
        text = self.text.get(index1='1.0', index2='end-1c')
        self.del_all_text()
        if self.act_key:
            self.marked_acts[self.act_key] = text
            self.info_changer('сохранение изменений прошло успешно!')
        else:
            self.info_changer(('ВНИМАНИЕ! Ошибка при сохранении изменений!'+
                               'Ключ текущего документа не устанолвен!'))

    def show_cur_tag(self):
        '''Show self.current_tag var value in the info line at the bottom of the
        main frame.
        Right bar's button command.
        '''
        if self.current_tag:
            self.info_changer('текущий тег: {}'.format(self.current_tag))
        else:
            self.info_changer('тег не выбран!')

    def show_db_info(self):
        '''Print db info into the console window.
        Right bar's button command.
        ===================================
        INTERFACE: see Connection.db_info()
        '''
        self.con.db_info()
        self.info_changer('информация о базе данных отображена в консоль!')

    def show_tags(self):
        '''Show all current tags with thier description
        and additional (hotkeys) information.
        Top menu command.
        '''
        new_win = self.new_win(main_parent=self.root, title='Список тегов')
        text = tk.Text(new_win)
        string = ''
        for key in sorted(self.tags_dict.keys()):
            string += key + str(self.tags_dict[key]) + '\n'
        text.insert(index='1.0', chars=string)
        text.pack()

    def txthg_selection(self, event):
        '''Watch for ComboBox widget alteration to upload currently selected
        text high value to programm reserved variable. Alter self.txthg_val
        var value.
        Internal binded function.
        '''
        high = self.txthg.get()
        self.info_changer("размер шрифта изменен"
                          +" с {} на {}".format(self.txthg_val, high))
        print ('text high: ' , high)
        self.txthg_val = high
        self.text.tag_configure('bigfont', font=('Times New Roman',
                                                 self.txthg_val,
                                                 'bold'))

    def write_to_var(self, passed_event):
        '''Interface function that trancends the binded tag hotkey value to the
        db functions for writing to the db file.
        Internal subfunction. It is used by self.append_hotkey(...).
        ========================================
        INTERFACE: see Connection.tags_changer()
        '''
        RU_key_holder = passed_event.keysym
        current_tag = self.combo.get()
        if len(self.tags_dict[current_tag]) < 2:
            self.tags_dict[current_tag].extend([RU_key_holder,
                                                passed_event.char])
            self.info_changer("для тега '{}' ".format(current_tag)
                              +"назначена новая"
                              +" горячая клавиша: "
                              +"{}".format(passed_event.char))
            self.con.tags_changer(self.tags_dict)
            self.text.bind('<Alt-{}>'.format(RU_key_holder),
                           lambda event: \
                           self.custome_insert(event, current_tag))
        elif len(self.tags_dict[current_tag]) == 3:
            self.text.bind('<Alt-{}>'.format(self.tags_dict[current_tag][1]),
                           lambda event: None)
            self.info_changer("для тега '{}' ".format(current_tag)
                              +" горячая клавиша изменена: "
                              +"с {} ".format(self.tags_dict[current_tag][1])
                              +"на {}".format(passed_event.char))
            self.tags_dict[current_tag][1:] = RU_key_holder, passed_event.char
            self.con.tags_changer(self.tags_dict)
            self.text.bind('<Alt-{}>'.format(RU_key_holder),
                           lambda event: \
                           self.custome_insert(event, current_tag))
        else:
            self.info_changer('ошибка определения горячей клавиши: '
                              +'превышена длина списка для ключа '
                                  +'"current_tag" ({})'.format(current_tag))
        print(RU_key_holder, passed_event.char)

        
GUI('Клиент для разметки текста').root.mainloop()
