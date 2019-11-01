import tkinter as tk 
from tkinter import ttk
import os
import mypackage.rule as rule
import mypackage.drawer as drawer
import time



class MainWindow(tk.Frame):
	def __init__(self):
		#define some variables to ease selection of chaotic type and set objects for later
		self._chaotic_types = ['Chaos Game', 'Ikeda Map', 'Mandelbrot Set', 'Bedhead Attractor', 'Hopalong Attractor', 'Rampe1 Attractor', 'Gumowski-Mira Attractor']
		self._chaotic_types_classes = [rule.ChaosGame(), rule.Ikeda(), rule.Mandelbrot(), rule.BHAttractor(), rule.HLAttractor(), rule.JR1Attractor(), rule.GMAttractor()]
		self._chaotic_types_settings = [None for i in range(len(self._chaotic_types))]
		self._generate_standard_settings()
		self.rule = self._chaotic_types_classes[0]

		self._root = tk.Tk()
		self._root.title('Chaos Drawer')

		self.padx, self.pady = 5, 3
		self._create_widgets()
		tk.Frame.__init__(self, self._root)
		self._snapshot = tk.IntVar(); self._snapshot.set(0)


	def _generate_standard_settings(self):
		for i, obj in enumerate(self._chaotic_types_classes):
			setting = []
			for var in obj.vars:
				exec(f'setting.append(obj.{var})')
			self._chaotic_types_settings[i] = setting


	def _set_parameter_widgets(self):
		
		#make new window
		self.p = p = tk.Toplevel()
		px, py = self.padx, self.pady

		curr_row = 0
		tk.Label(p, text=f'Settings: {self._chaotic_type.get()}').grid(row=0, padx=px, pady=py, columnspan=3)

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
		tk.Button(p, text='Save', command=self._save_settings, width=20).grid(row=curr_row, column=0, padx=px, pady=py)
		tk.Button(p, text='Load', command=self._load_settings, width=20).grid(row=curr_row, column=1, padx=px, pady=py)
		tk.Entry(p, textvariable=self._snapshot, width=3).grid(row=curr_row, column=2, padx=px, pady=py, sticky='W')


	def _load_settings(self):
		self.rule.load_snapshot(self._snapshot.get())
		self.p.destroy()
		self._set_parameter_widgets()


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
		o = tk.OptionMenu(frame, self._chaotic_type, *self._chaotic_types, command=self._update_rule)
		o.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		o.config(width=30)
		tk.Button(frame, text='Change Parameters', command=self._set_parameter_widgets).grid(row=curr_row, column=2, sticky="W", padx=px, pady=py)

		# #make iterations setting
		# curr_row += 1
		# self._iterations = tk.IntVar(); self._iterations.set(1000000)
		# tk.Label(r, text='Iterations: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		# tk.Entry(r, textvariable=self._iterations, width=12).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#Resolution setting
		curr_row += 1
		self._resx, self._resy = tk.IntVar(), tk.IntVar(); self._resx.set(4000), self._resy.set(2250)
		tk.Label(r, text='Resolution: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		#make container for resolution
		frame = tk.Frame(r)
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Entry(frame, textvariable=self._resx, width=6).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='x').grid(row=curr_row, column=2, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._resy, width=6).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)

		#Display on completion
		curr_row += 1
		self._show_on_completion = tk.BooleanVar(); self._show_on_completion.set(False)
		tk.Label(r, text='Display generated image: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		tk.Checkbutton(r, variable=self._show_on_completion).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#opacity setting
		curr_row += 1
		self._opacity_steps = tk.IntVar(); self._opacity_steps.set(4)
		tk.Label(r, text='Opacity Steps: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		self.opacity_entry = tk.Entry(r, textvariable=self._opacity_steps, width=3)
		self.opacity_entry.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)

		#draw colour
		curr_row += 1
		self._opacity_steps = tk.IntVar(); self._opacity_steps.set(4)
		tk.Label(r, text='Background Colour: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		frame = tk.Frame(r)
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		self._bkgr_R, self._bkgr_G, self._bkgr_B = tk.IntVar(), tk.IntVar(), tk.IntVar(); self._bkgr_R.set(0), self._bkgr_G.set(0), self._bkgr_B.set(0)
		tk.Label(frame, text='R: ').grid(row=curr_row, column=0, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._bkgr_R, width=3).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='G:').grid(row=curr_row, column=2, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._bkgr_G, width=3).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='B:').grid(row=curr_row, column=4, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._bkgr_B, width=3).grid(row=curr_row, column=5, sticky='W', padx=px, pady=py)

		#draw colour
		curr_row += 1
		self._opacity_steps = tk.IntVar(); self._opacity_steps.set(4)
		tk.Label(r, text='Draw Colour: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		frame = tk.Frame(r)
		frame.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		self._draw_R, self._draw_G, self._draw_B = tk.IntVar(), tk.IntVar(), tk.IntVar(); self._draw_R.set(255), self._draw_G.set(255), self._draw_B.set(255)
		tk.Label(frame, text='R: ').grid(row=curr_row, column=0, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._draw_R, width=3).grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='G:').grid(row=curr_row, column=2, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._draw_G, width=3).grid(row=curr_row, column=3, sticky='W', padx=px, pady=py)
		tk.Label(frame, text='B:').grid(row=curr_row, column=4, sticky='W', pady=py)
		tk.Entry(frame, textvariable=self._draw_B, width=3).grid(row=curr_row, column=5, sticky='W', padx=px, pady=py)

		#Path setting
		curr_row += 1
		self._save_path = tk.StringVar()
		tk.Label(r, text='Image path: ').grid(row=curr_row, column=0, sticky='W', padx=px, pady=py)
		self.path_entry = tk.Entry(r, textvariable=self._save_path, width=45)
		self.path_entry.grid(row=curr_row, column=1, sticky='W', padx=px, pady=py)
		self._update_path()

		#Start button
		curr_row += 1
		tk.Button(r, text='Start', command=self._start, width=20).grid(row=curr_row, columnspan=2, padx=px, pady=py)

		#make progress bar
		curr_row += 1
		self.progressbar = ttk.Progressbar(r, orient='horizontal', length=500, mode='determinate')
		self.progressbar.grid(row=curr_row, columnspan=2, padx=px, pady=py)


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
		prog = tk.IntVar(); prog.set(0)
		max = 50
		self.progressbar['maximum'] = max
		self.progressbar['variable'] = prog

		batches = [self.rule.iterations//max for i in range(max-1)]
		batches.append(self.rule.iterations - sum(batches))

		poss = []
		for i, b in enumerate(batches):
			if i == 0:
				poss += self.rule.iterate(b)	
			else:
				poss += self.rule.iterate(b, poss[-1])		
			prog.set(i+1)
			self._root.update()

		resolution = self._resx.get(), self._resy.get()
		draw_colour = self._draw_R.get(), self._draw_G.get(), self._draw_B.get()
		bkgr_colour = self._bkgr_R.get(), self._bkgr_G.get(), self._bkgr_B.get()
		self.screen = drawer.Screen(resolution, draw_colour=draw_colour, bkgr_colour=bkgr_colour)
		self.screen.draw_opacity_steps = int(self.opacity_entry.get())

		self.screen.draw_pixels(poss, auto_size=True)
		self.screen.save(self._save_path.get())
		if self._show_on_completion.get():
			self.screen.show()
		self._update_path()

main = MainWindow()
main.mainloop()
