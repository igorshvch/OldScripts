import tkinter as tk

class TextApp(tk.Frame):
	def __init__(self, *args, **kargs):
		tk.Frame.__init__(self, *args, **kargs)
		self.pack(expand='yes', fill='both')
		tk.Label(self, text='Пример форматирвоания текста виджетом Text').pack(side='top', expand='yes', fill='x')
		self.txt = tk.Text(self)
		self.txt.pack(side='top', expand='yes', fill='both')
		tk.Button(self, text='Read', command=self.reader).pack(side='left', expand='yes', fill='x')
		tk.Button(self, text='Print', command=self.printer).pack(side='left', expand='yes', fill='x')
		tk.Button(self, text='Extract', command=self.extraction).pack(side='left', expand='yes', fill='x')
		tk.Button(self, text='Insert', command=self.insertion).pack(side='left', expand='yes', fill='x')
		tk.Button(self, text='Delete', command=self.deletion).pack(side='left', expand='yes', fill='x')
	def reader(self):
		self.container = self.txt.get('1.0', 'end-1c')
	def printer(self):
		if '\n' in self.container:
			store = self.container.split('\n')
			for i in store:
				print('\t', i)
		else:
			print('\t', self.container)
	def extraction(self):
		print(self.txt.get('1.0', 'end-1c'))
	def insertion(self):
		store = '<INS>\t' + self.container + '\t</INS>'
		if '\n' in store:
			store = store.replace('\n', '\n<INS>\t')
			self.txt.insert(index = '1.0', chars=store)
		else:
			self.txt.insert(index = '1.0', chars=store)
	def deletion(self):
		self.txt.delete(index1='1.0', index2='end')

TextApp().mainloop()
