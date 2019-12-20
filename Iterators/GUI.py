import tkinter as tk 
from tkinter import ttk
import os
import mypackage.rule3 as rule
import mypackage.colour_maps as cmap
import mypackage.renderer as rend
import time
import multiprocessing as mp
import numpy as np



class MainWindow(tk.Frame):
	def __init__(self):
		#define some variables to ease selection of chaotic type and set objects for later
		self._chaotic_types = ['Chaos Game', 'Ikeda Map', 'Mandelbrot Set', 'Bedhead Attractor', 'Hopalong Attractor', 'Rampe1 Attractor', 'Gumowski-Mira Attractor']
		self._chaotic_types_classes = [rule.ChaosGame(), rule.Ikeda(), rule.Mandelbrot(), rule.BHAttractor(), rule.HLAttractor(), rule.JR1Attractor(), rule.GMAttractor()]
		self._chaotic_types_settings = [None for i in range(len(self._chaotic_types_classes))]
		self._generate_standard_settings()
		self.rule = self._chaotic_types_classes[0]
		self._chaotic_type_index = 0

		self._cmap_names = cmap.get_cmap_names()
		self._cmap_classes = cmap.get_cmap_classes()
		self._cmap = self._cmap_classes[0]

		self._root = tk.Tk()
		self._root.title('Chaos Drawer')

		self.padx, self.pady = 5, 3
		self._create_widgets()
		tk.Frame.__init__(self, self._root)
		self._snapshot = tk.IntVar(); self._snapshot.set(1)


	def _generate_standard_settings(self):
		self._chaotic_types_settings = [[getattr(obj, var) for var in obj.vars] for obj in self._chaotic_types_classes]

	def _set_parameter_widgets(self):
		#make new window
		self.p = p = tk.Toplevel()
		pf = tk.Frame(p, bg=("light grey"), bd=2, relief='ridge')
		px, py = self.padx, self.pady

		curr_row = 0
		tk.Label(p, text=f'Settings: {self._chaotic_type.get()}').grid(row=0, padx=px, pady=py, columnspan=3)

		curr_row += 1
		pf.grid(row=curr_row, padx=px, pady=py, columnspan=5, sticky='ew')
		tk.Label(pf, bg=("light grey"), text='Parameter').grid(row=curr_row, column=0, padx=px, pady=py)
		tk.Label(pf, bg=("light grey"), text='Value').grid(row=curr_row, column=1, padx=px, pady=py)
		tk.Label(pf, bg=("light grey"), text='Suggested Space').grid(row=curr_row, column=2, padx=px, pady=py)

		curr_row += 1
		ttk.Separator(pf).grid(row=curr_row, columnspan=3)

		settings = []
		for var in self.rule.vars:
			curr_row += 1
			exec(f'''
setting = tk.StringVar()
setting.set(self.rule.{var})
settings.append(setting)
tk.Label(pf, bg=("light grey"), text="{var}").grid(row=curr_row, column=0, padx=px, pady=py)
tk.Entry(pf, textvariable=setting).grid(row=curr_row, column=1, padx=px, pady=py)
				''')
		self._chaotic_types_settings[self._chaotic_type_index] = settings

		curr_row += 1
		tk.Button(p, text='Save', command=self._save_settings, width=20).grid(row=curr_row, column=0, padx=px, pady=py)
		tk.Button(p, text='Load Preset', command=self._load_settings, width=20).grid(row=curr_row, column=1, padx=px, pady=py)
		tk.Entry(p, textvariable=self._snapshot, width=3).grid(row=curr_row, column=2, pady=py, sticky='W')
		tk.Label(p, text=f'/{len(self.rule.snapshots)}').grid(row=curr_row, column=3, pady=py, sticky='W')

	def _load_settings(self):
		self.rule.load_snapshot(self._snapshot.get()-1)
		self.p.destroy()

	def _save_settings(self):
		settings = self._chaotic_types_settings[self._chaotic_type_index]
		#set rule variables according to settings set in self._set_parameter_widgets
		for i, setting in enumerate(settings):
			exec(f'self.rule.{self.rule.vars[i]} = {setting.get()}')
		self.p.destroy()

	def _create_widgets(self):
		r = self._root
		px, py = self.padx, self.pady

		#Top label
		curr_row = 0
		tk.Label(r, text='Settings').grid(row=curr_row, columnspan=2, padx=px, pady=py)

		curr_row += 1
		sf = tk.Frame(r, bg=("light grey"), bd=2, relief='ridge')
		sf.grid(row=curr_row, padx=px, pady=py)

		#Set chaotic type row
		curr_row += 1
		self._chaotic_type = tk.StringVar(); self._chaotic_type.set(self._chaotic_types[0])
		frame = tk.Frame(sf, bg=("light grey"))
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(sf, text='Chaotic generator type: ', anchor="e", bg=("light grey")).grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		o = tk.OptionMenu(frame, self._chaotic_type, *self._chaotic_types, command=self._update_rule)
		o.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		o.config(width=30)
		tk.Button(frame, text='Change Parameters', command=self._set_parameter_widgets).grid(row=curr_row, column=2, sticky="W", padx=px, pady=py)

		# #make iterations setting
		# curr_row += 1
		# self._iterations = tk.IntVar(); self._iterations.set(1000000)
		# tk.Label(sf, text='Iterations: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		# tk.Entry(sf, textvariable=self._iterations, width=12).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#Resolution setting
		curr_row += 1
		self._resx, self._resy = tk.IntVar(), tk.IntVar(); self._resx.set(4000), self._resy.set(2250)
		tk.Label(sf, text='Resolution: ', bg=("light grey")).grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		#make container for resolution
		frame = tk.Frame(sf, bg=("light grey"))
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Entry(frame, textvariable=self._resx, width=6).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='x', bg=("light grey")).grid(row=curr_row, column=2, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._resy, width=6).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)

		#Display on completion
		curr_row += 1
		self._show_on_completion = tk.BooleanVar(); self._show_on_completion.set(False)
		tk.Label(sf, text='Display generated image: ', bg=("light grey")).grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		tk.Checkbutton(sf, variable=self._show_on_completion, bg=("light grey")).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#cmap setting
		curr_row += 1
		self._colour_map = tk.StringVar(); self._colour_map.set(self._cmap_names[0]); self._cmap_cycles = tk.StringVar(); self._cmap_cycles.set(1)
		frame = tk.Frame(sf, bg=("light grey"))
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(sf, text='Colour Map: ', anchor="e", bg=("light grey")).grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		o = tk.OptionMenu(frame, self._colour_map, command=self._update_cmap, *self._cmap_names)
		o.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		o.config(width=12)
		tk.Label(frame, text='Colour Cycles: ', anchor="e", bg=("light grey")).grid(row=curr_row, column=2, sticky='W', padx=px, pady=py)
		tk.Entry(frame, textvariable=self._cmap_cycles, width=3).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)
		tk.Button(frame, text='Show Sample', command=self._show_cmap).grid(row=curr_row, column=4, sticky="W", padx=px, pady=py)

		#Path setting
		curr_row += 1
		self._save_path = tk.StringVar()
		tk.Label(sf, text='Image path: ', bg=("light grey")).grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		self.path_entry = tk.Entry(sf, textvariable=self._save_path, width=45)
		self.path_entry.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		self._update_path()

		#Start button
		curr_row += 1
		tk.Button(r, text='Start', command=self._start, width=20).grid(row=curr_row, columnspan=2, padx=px, pady=py)

		#make progress bar
		curr_row += 1
		self.progressbar = ttk.Progressbar(r, orient='horizontal', length=500, mode='determinate')
		self.progressbar.grid(row=curr_row, columnspan=2, padx=px, pady=py)

	def _update_cmap(self, var=None):
		self._cmap = self._cmap_classes[self._cmap_names.index(self._colour_map.get())]

	def _show_cmap(self):
		rend.draw_cmap_sample(self._cmap(cycles=int(self._cmap_cycles.get())))


	def _update_path(self, var=None):
		path = os.getcwd() + '\\Images\\' + self._chaotic_type.get().replace(' ', '_') + '.bmp'

		i = 0
		while os.path.isfile(path):
			i += 1
			path = os.getcwd() + '\\Images\\' + self._chaotic_type.get().replace(' ', '_') + f'_{i}.bmp'

		self._save_path.set(path)
		self.path_entry.xview_scroll(1000, 'units')

	def _update_rule(self, var=None):
		#set rule according to chosen chaotic system
		self._chaotic_type_index = self._chaotic_types.index(self._chaotic_type.get())
		self.rule = self._chaotic_types_classes[self._chaotic_type_index]
		self._update_path()


	def _start(self):
		#make progressbar
		resolution = self._resx.get(), self._resy.get()
		self.renderer = rend.Renderer(resolution, colour_map=self._cmap(cycles=int(self._cmap_cycles.get())))

		prog = tk.IntVar(); prog.set(0)
		self.progressbar['maximum'] = 3
		self.progressbar['variable'] = prog

		# batches = [self.rule.iterations//max for i in range(max-1)]
		# batches.append(self.rule.iterations - sum(batches))

		self.rule.resolution = resolution
		pixel_array = self.rule.generate()

		prog.set(1); self._root.update()
		# for i, b in enumerate(batches):
		# 	print(b)
		# 	if i == 0:
		# 		poss += self.rule.generate(renderer=self.renderer)	
		# 	else:
		# 		poss += self.rule.generate(b, start_pos=poss[-1], renderer=self.renderer)		
		# 	prog.set(i+1)
		# 	self._root.update()

		self.renderer.input_array(np.sqrt(pixel_array))
		prog.set(2); self._root.update()

		self.renderer.save(self._save_path.get())
		prog.set(3); self._root.update()

		if self._show_on_completion.get():
			self.renderer.show()

		self._update_path()
		prog.set(0); self._root.update()

main = MainWindow()
main.mainloop()
