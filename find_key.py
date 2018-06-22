import tkinter as tk

class FindKeySym():
    def run(self):
        root = tk.Frame()
        lablefont = ('courier', 20, 'bold')
        lb = tk.Label(root, text='Press me!', bg = 'pink', font=lablefont, height=5, width=20)
        root.pack(expand='yes', fill='both')
        lb.pack(expand='yes', fill='both')
        lb.bind('<KeyPress>', self.print_ks)
        lb.bind('<Alt-Control-aring>', self.special)
        lb.focus()
        tk.mainloop()

    def special(self, event):
        print('You got me!')

    def print_ks(self, event):
        print('key_sym: ', event.keysym)
