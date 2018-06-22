import tkinter as tk
from tkinter import ttk

class GUIContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()

        self.frames = {}
        frame = MainPage(container, self)
        self.frames['MainPage'] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('MainPage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Just Example.\nJust do it!")
        label.pack()


app = GUIContainer()
app.mainloop()


        
