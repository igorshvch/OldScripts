import tkinter as tk
from tkinter import ttk

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


class GUI_Manager():
    #def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs)
        #self.frames_names = ['buffer']
        #self.frames = {}
        #self.frames['buffer'] = {'f_object':tk.Frame(master=self)}
        #self.buttons_list = [['button name', lambda: print('Command')]]

    def new_win(self, title):
        new_window = tk.Toplevel(self)
        new_window.title(title)
        return new_window

    def make_frames(self, frames_dict, frames_names, key_to_frame='f_object'):
        for i in frames_names:
            frames_dict[i][key_to_frame].config(relief=frames_dict[i].get('f_relief', 'flat'),
                                            bd=frames_dict[i].get('f_bd', 0))
            frames_dict[i][key_to_frame].pack(side=frames_dict[i].get('f_side', 'top'),
                                           expand=frames_dict[i].get('f_expand', 'yes'),
                                           fill=frames_dict[i].get('f_fill', 'both'),
                                           padx=frames_dict[i].get('f_padx', 0),
                                           pady=frames_dict[i].get('f_pady', 0))

    def make_notebook(self, parent, pad_names=[]):
            notebook = ttk.Notebook(master=parent)
            pad_store_dict = {i:tk.Frame(master=notebook) for i in pad_names}
            for name in pad_names:
                notebook.add(pad_store_dict[name], text=name)
            notebook.pack(side='top', expand='yes', fill='both')
            return pad_store_dict

    def make_text_with_scroll(self, widget=None,
                              parent=None, widget_height=None,
                              widget_width=None, scroll_='yes'):
        if scroll_ == 'yes':
            scroll_bar = tk.Scrollbar(master=parent)
            if widget:
                tk_object = CustomTextWidget
            else:
                tk_object = tk.Text
            widget_var = tk_object(master=parent)
            if widget_height:
                widget_var['height']=widget_height
            if widget_width:
                widget_var['width']=widget_width        
            scroll_bar.config(command=widget_var.yview)
            widget_var.config(yscrollcommand=scroll_bar.set)
            scroll_bar.pack(side='right', fill='y')
            widget_var.pack(side='left', expand='yes', fill='both')
            return widget_var
        else:
            if widget:
                tk_object = CustomTextWidget
            else:
                tk_object = tk.Text
            widget_var = tk_object(master=parent)
            if widget_height:
                widget_var['height']=widget_height
            if widget_width:
                widget_var['width']=widget_width 
            widget_var.pack(side=widget_side, expand=widget_expand, fill=widget_fill)
            return widget_var

    def make_buttons(self, parent=None, buttons_list=None,
                     height=1, width=None, side='top', anchor='w'):
        store={}
        for i in buttons_list:
            text, command = i
            if width:
                store[text] = tk.Button(master=parent,
                                        text=text,
                                        command=command,
                                        height=height,
                                        width=width)
                store[text].pack(side=side, anchor=anchor)
            else:
                store[text]=tk.Button(master=parent,
                                      text=text,
                                      command=command,
                                      height=height)
                store[text].pack(side=side, expand='no',
                                 fill='x', anchor=anchor)
        return store

    def make_radiobuttons(self, parent=None,
                          values=None,
                          pack_side='top',
                          tk_var=None,
                          wdg_state='normal',
                          pack_option='yes'):
        store_dict = {}
        for i in range(len(values)):
            store_dict[values[i][1]]=tk.Radiobutton(master=parent,
                                                    text=values[i][0],
                                                    variable=tk_var,
                                                    value=values[i][1],
                                                    command=values[i][2],
                                                    state=wdg_state)
            if pack_option=='yes':
                store_dict[values[i][1]].pack(side=pack_side,
                                              anchor='nw')
            else:
                pass
        tk_var.set(values[0][1])
        return store_dict

    def make_listbox(self, parent=None, action_argument=None,
                     binded_function=None, listbox_width=27):
        scroll = tk.Scrollbar(master=parent)
        listbox = tk.Listbox(master=parent, width=listbox_width)
        scroll.config(command=listbox.yview)
        listbox.config(yscrollcommand=scroll.set)
        listbox.bind(action_argument, binded_function)
        scroll.pack(side='right', fill='y')
        listbox.pack(side='left', expand='yes', fill='both')
        return listbox

    def make_tree(self, parent, columns=None, scrolls='both',
                  fill='none', expand='no'):
        if columns:
            tree_var = ttk.Treeview(master=parent, columns=columns)
            tree_var.column('#0', width=100)
            for col in columns:
                tree_var.column(col, width=40)
                tree_var.heading(col, text=col)
        else:
            tree_var = ttk.Treeview(master=parent)
            tree_var.column('#0', width=100)
        if scrolls == 'both':
            scroll_bar_y = tk.Scrollbar(master=parent, orient='vertical')
            scroll_bar_x = tk.Scrollbar(master=parent, orient='horizontal')
            scroll_bar_y.pack(side='right', fill='y')
            scroll_bar_x.pack(side='bottom', fill='x')
            scroll_bar_y.config(command=tree_var.yview)
            scroll_bar_x.config(command=tree_var.xview)
            tree_var.config(yscrollcommand=scroll_bar_y.set)
            tree_var.config(xscrollcommand=scroll_bar_x.set)
        elif scrolls == 'ver':
            scroll_bar_y = tk.Scrollbar(master=parent, orient='vertical')
            scroll_bar_y.pack(side='right', fill='y')
            scroll_bar_y.config(command=tree_var.yview)
            tree_var.config(yscrollcommand=scroll_bar_y.set)
        elif scrolls == 'hor':
            scroll_bar_x = tk.Scrollbar(master=parent, orient='horizontal')
            scroll_bar_x.pack(side='bottom', fill='x')
            scroll_bar_x.config(command=tree_var.xview)
            tree_var.config(xscrollcommand=scroll_bar_x.set)
        tree_var.pack(side='top', fill=fill, expand=expand)
        return tree_var

    def make_progressbar(self, parent, orient='horizontal',
                         length=200, mode='indeterminate',
                         pack_side='top'):
        progress_var = ttk.Progressbar(master=parent, orient=orient,
                    length=length, mode=mode)
        progress_var.pack(side=pack_side)
        return progress_var

    #def custom_insert(self, event, text_widget=None):
    #   text_widget.insert(index='1.0', chars=self.selection_get(selection = "CLIPBOARD"))
    #
    #def custom_copy(self, event, text_widget=None):
    #    text_widget.get(index1='1.0', index2='end-1c')
    #
    #def binding_insert(self, text_widget=None):
    #   text_widget.bind('<Control-igrave>', self.custom_insert)
    #
    #def binding_copy(self, text_widget=None):
    #    text_widget.bind('<Control-ntilde>', self.custom_copy)
    #
    #def destroy_widget(self, widget_var):
    #    widget_var.destroy()

    def make_lb_text(self, parent_lb_name, parent_txt_name,
                     key_to_frame='f_object', border1=0, border2=None,
                     store=True, frames_dict=None, wdg_label=None, widget_width=40,
                     default_buttons=True, buttons_holder=None, buttons_list=None):
        if store:
            frames_dict[parent_lb_name][key_to_frame].config(relief='sunken', bd=1)
            tk.Label(master=frames_dict[parent_lb_name][key_to_frame],
                     text=parent_lb_name[border1:border2]).pack(side='left')
            if default_buttons:
                buttons_list = [['Del', lambda :self.special_del_db(parent_txt_name, self.texts[parent_txt_name])],
                                ['Edit', lambda :self.special_edit_db(parent_txt_name, self.texts[parent_txt_name])],
                                ['Confirm', lambda :self.special_confirm_db(parent_txt_name, self.texts[parent_txt_name])]]
            else:
                buttons_list = buttons_list
            buttons_holder[parent_txt_name]=self.make_buttons(parent=frames_dict[parent_lb_name][key_to_frame],
                                                              buttons_list=buttons_list,
                                                              side='right')
            if 'actname' not in parent_txt_name:
                self.texts[parent_txt_name] = self.make_text_with_scroll(parent=frames_dict[parent_txt_name][key_to_frame],
                                                                    widget_height=5, widget_width=widget_width)
            else:
                self.texts[parent_txt_name] = self.make_text_with_scroll(parent=frames_dict[parent_txt_name][key_to_frame],
                                                                    widget_height=3, widget_width=widget_width)
                return None
        else:
            tk.Label(master=parent_lb_name, text=wdg_label).pack(side='left')
            text = self.make_text_with_scroll(parent=parent_txt_name,
                                              widget_height=5, widget_width=widget_width)
            if default_buttons:
                buttons_list = [['Del', lambda :text.delete(index1='1.0', index2='end')],
                                  ['Edit', lambda :text.config(state='normal', bg='white')],
                                  ['Confirm', lambda :text.config(state='disabled', bg='#d4d0c8')]]
            else:
                buttons_list = buttons_list
            self.make_buttons(parent=parent_lb_name,
                              buttons_list=buttons_list,
                              side='right')
            return text


class TextLabelButtons(GUI_Manager):
    def make_scroll_text_label_widget(self, parent_frame, buttons_list, label_text, text_height, text_width):
        holder = tk.Frame(master=parent.frame)
        holder_label = tk.Frame(master=holder, relief='sunken', bd=1)
        holder_text = tk.Frame(master=holder)
        label = tk.Label(master=holder_label, text=label_text)
        holder.pack(side='top')
        holder_label.pack(side='top', expand='no', fill='x', padx=1, pady=1)
        holder_text.pack(side='top', expand='yes', fill='both', padx=1, pady=1)
        label.pack(side='left', expand='no', fill='none')
        text = self.make_text_with_scroll(parent=holder_text,
                                          widget_height=text_height,
                                          widget_width=text_width)
        buttons = self.make_buttons(parent=holder_label,
                                    buttons_list=buttons_list,
                                    side='right')

        return holder, text, buttons, label
