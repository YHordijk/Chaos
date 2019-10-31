import tkinter as tk 
import os
import mypackage.rule as rule


class MainWindow(tk.Frame):
	def __init__(self, title=''):
		#define some variables to ease selection of chaotic type and set objects for later
		self._chaotic_types = ['Chaos Game', 'Ikeda Map', 'Mandelbrot Set']
		self._chaotic_types_classes = [rule.ChaosGame(), rule.Ikeda(), rule.Mandelbrot()]
		self._chaotic_types_settings = [None for i in range(len(self._chaotic_types))]

		self._root = tk.Tk()
		self._root.title(title)

		self.padx, self.pady = 5, 3
		self._create_widgets()
		tk.Frame.__init__(self, self._root)


	def _set_parameter_widgets(self):
		#set rule according to chosen chaotic system
		self._chaotic_type_index = self._chaotic_types.index(self._chaotic_type.get())
		self.rule = self._chaotic_types_classes[self._chaotic_type_index]
		#make new window
		p = tk.Toplevel()
		px, py = self.padx, self.pady

		curr_row = 0
		tk.Label(p, text=f'Settings: {self._chaotic_type.get()}').grid(row=0, padx=px, pady=py, columnspan=3)

		# curr_row += 1
		# tk.Label(p, text='').grid(row=curr_row, padx=px, pady=py)

		curr_row += 1
		tk.Label(p, text='Parameter').grid(row=curr_row, column=0, padx=px, pady=py)
		tk.Label(p, text='Value').grid(row=curr_row, column=1, padx=px, pady=py)
		tk.Label(p, text='Suggested Space').grid(row=curr_row, column=2, padx=px, pady=py)

		settings = []
		for var in self.rule.vars:
			curr_row += 1
			exec(f'''
setting = tk.StringVar()
setting.set(self.rule.{var})
settings.append(setting)
tk.Label(p, text="{var}").grid(row=curr_row, column=0, padx=px, pady=py)
tk.Entry(p, textvariable=setting).grid(row=curr_row, column=1, padx=px, pady=py)
				''')
		self._chaotic_types_settings[self._chaotic_type_index] = settings

		curr_row += 1
		tk.Button(p, text='Save', command=self._save_settings, width=20).grid(row=curr_row, columnspan=3, padx=px, pady=py)


	def _save_settings(self):
		settings = self._chaotic_types_settings[self._chaotic_type_index]
		#set rule variables according to settings set in self._set_parameter_widgets
		for i, setting in enumerate(settings):
			exec(f'self.rule.{self.rule.vars[i]} = {setting.get()}')


	def _create_widgets(self):
		r = self._root
		px, py = self.padx, self.pady

		#Top label
		curr_row = 0
		tk.Label(r, text='Settings').grid(row=curr_row, columnspan=2, padx=px, pady=py)

		#Set chaotic type row
		curr_row += 1
		self._chaotic_type = tk.StringVar(); self._chaotic_type.set(self._chaotic_types[0])
		frame = tk.Frame(r)
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(r, text='Chaotic generator type: ', anchor="e").grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		o = tk.OptionMenu(frame, self._chaotic_type, *self._chaotic_types, command=self._update_path)
		o.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		o.config(width=30)
		tk.Button(frame, text='Change Parameters', command=self._set_parameter_widgets).grid(row=curr_row, column=2, sticky="W", padx=px, pady=py)

		#Resolution setting
		curr_row += 1
		self._resx, self._resy = tk.IntVar(), tk.IntVar(); self._resx.set(1600), self._resy.set(900)
		tk.Label(r, text='Resolution: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		#make container for resolution
		frame = tk.Frame(r)
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Entry(frame, textvariable=self._resx, width=6).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='x').grid(row=curr_row, column=2, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._resy, width=6).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)

		#Display on completion
		curr_row += 1
		self._show_on_completion = tk.BooleanVar(); self._show_on_completion.set(True)
		tk.Label(r, text='Display generated image: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		tk.Checkbutton(r, variable=self._show_on_completion).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#Path setting
		curr_row += 1
		self._save_path = tk.StringVar()
		tk.Label(r, text='Image path: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		self.path_entry = tk.Entry(r, textvariable=self._save_path, width=50)
		self.path_entry.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		self._update_path()

		#Start button
		curr_row += 1
		tk.Button(r, text='Start', command=self._start, width=20).grid(row=curr_row, columnspan=2, padx=px, pady=py)


	def _update_path(self, var=None):
		self._save_path.set(os.getcwd() + '\\Images\\' + self._chaotic_type.get().replace(' ', '_'))
		self.path_entry.xview_scroll(1000, 'units')
		

	def _start(self):
		print(self._show_on_completion.get())
		print(self._chaotic_type.get())
		print(self._save_path.get())
	

main = MainWindow(title='Chaos drawer')
main.mainloop()
