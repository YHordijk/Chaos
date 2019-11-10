import math
import numpy as np
import re
import random
import multiprocessing as mp


class Rule3:
	def __init__(self, screen=None, **kwargs):
		self.screen = screen
		self.vector_equations = None
		self.parse_list = [['math.cos', 'np.cos'],
						   ['math.sin', 'np.sin'],
						   ['pow', 'np.power']]
		self.set_rule()
		# self.vectorize_equations()

		for key, value in kwargs.items():
			setattr(self, key, value)

	def vectorize_equations(self):
		if self.vector_equations == None:
			self.vector_equations = []
			for eq in self.equations:
				for p in self.parse_list:
					eq = eq.replace(p[0], p[1])
				self.vector_equations.append(eq)

	def generate(self, iterations=None, start_pos=None, iter_skip=0, processes=1, plot_on_screen=True, screen=None):
		if iterations is None: iterations = self.iterations
		if start_pos is None: start_pos = self.start_pos
		self.screen = screen

		if type(start_pos) is list:
			pool = mp.Pool(processes)
			pos = pool.map(self.iterate, start_pos)
		else:
			pos = self.iterate(start_pos)
		if plot_on_screen:
			if self.screen is not None:
				self.screen.draw_pixels(pos[iter_skip:], auto_size=True)
			else:
				print('Error: please supply drawer.screen object.')
		return pos

	def iterate_vector(self, start_pos_list, iterations, plot_on_screen=True, screen=None):
		self.x, self.y = np.array_split(start_pos_list, 2, axis=1)

		pos = np.array([[],])
		for i in range(iterations):
			for eq in self.vector_equations:
				exec(eq)
			np.append(pos, np.array([[self.x, self.y]]), axis=0)
		return pos

	def check_screen(self):
		if self.plot_on_screen:
			if self.screen is None:
				print('Error: to plot on screen, please supply drawer.screen object.')
				return

	def load_snapshot(self, index=0):
		snapshot = self.snapshots[index]
		for val, var in zip(snapshot, self.vars):
			setattr(self, var, val)

	def iterate(self, start_pos):
		poss = []
		x, y = start_pos
		for _ in range(self.iterations):
			poss.append((x, y))
			x, y = self.step((x, y))
		return poss




class JR1Attractor(Rule3):
	def set_rule(self):
		self.vars = ['iterations', 'init_x', 'init_y', 'a', 'b', 'c', 'd']
		self.snapshots = [[1000000, 0.1, 0.1, -2.7918, 2.1196, 1.0284, 0.1384],
						  [1000000, 0.1, 0.1, 2.6, -2.5995, -2.9007, 0.3565],
						  [1000000, 0.1, 0.1, 1.8285, -1.8539, 0.3816, 1.9765],
						  [1000000, 0.1, 0.1, 2.5425, 2.8358, -0.8721, 2.7044],
						  [1000000, 0.1, 0.1, -1.8669, 1.2768, -2.9296, -0.4121]]
		self.explanation = 'Rampe1 Attractor.'
		self.name = 'Rampe1 Attractor'

		self.load_snapshot(0)
		self.start_pos = self.init_x, self.init_y

	def step(self, p):
		x = math.cos(p[1]*self.b) + self.c*math.sin(p[0]*self.b) 
		y = math.cos(p[0]*self.a) + self.d*math.sin(p[1]*self.a)

		return x, y


class GMAttractor(Rule3):
	def set_rule(self):
		self.vars = ['iterations', 'init_x', 'init_y', 'a', 'b']
		self.explanation = 'Gumowski-Mira Attractor.'
		self.name = 'Gumowski-Mira Attractor'
		self.snapshots = [[1000000, 0, 0.5, -0.31, 1],
						  [1000000, -0.61, 0.1, -0.012, 0.9186],
						  [1000000, 0.1, 0.1, -0.77, 0.95],
						  [1000000, 0.78662442881614, 0.919355855789036, 0.900278024375439, 0.661233567167073],
						  [1000000, 0, 0.5, 0.008, -0.7],
						  [1000000, -0.325819793157279, 0.48573582014069, 0.062683217227459, -0.436713613104075],
						  [1000000, -0.723135391715914, -0.327585775405169, 0.79253300698474, 0.345703079365194]]
		self.load_snapshot(0)
		self.start_pos = self.init_x, self.init_y
		self.w = 0

	def step(self, p):
		x = self.b * p[1] + self.w
		self.w = self.a*x + (1-self.a)*2*x**2/(1+x**2)
		y = self.w - p[0]

		return x, y

class BHAttractor(Rule3):
	def set_rule(self):
		self.vars = ['iterations', 'init_x', 'init_y', 'a', 'b']
		self.explanation = 'Bedhead Attractor.'
		self.name = 'Bedhead Attractor'
		self.snapshots = [[1000000, 1., 1., 0.65343, 0.7345345],
						  [1000000, 1., 1., -0.81, -0.92],
						  [1000000, 1., 1., 0.06, 0.98],
						  [1000000, 1., 1., -0.64, 0.76],
						  [1000000, 1., 1., -0.67, 0.83]]

		self.load_snapshot(0)
		self.start_pos = self.init_x, self.init_y

	def step(self, p):
		x = math.sin(p[0]*p[1]/self.b)*p[1] + math.cos(self.a*p[0]-p[1])
		y = p[0] + math.sin(p[1])/self.b

		return x, y


class HLAttractor(Rule3):
	def set_rule(self):
		self.vars = ['iterations', 'init_x', 'init_y', 'a', 'b', 'c']
		self.equations = ['self.nx = self.y - 1 - math.sqrt(abs(self.b*self.x-1-self.c))*math.copysign(1, self.x-1)',
						  'self.y = self.a - self.x - 1',
						  'self.x = self.nx']

		self.vector_equations = []
		self.suggested_space = []
		self.explanation = 'Hopalong Attractor.'
		self.name = 'Hopalong Attractor'

		self.snapshots = [[1000000, 0., 0., random.random()*10, random.random()*10, random.random()*10]]

		self.load_snapshot(0)
		self.start_pos = self.init_x, self.init_y
		# self.a, self.b = 2*random.rand()-1, 2*random.rand()-1

	def step(self, p):
		x = p[1] - 1 - math.sqrt(abs(self.b*p[0]-1-self.c))*math.copysign(1, p[0]-1)
		y = self.a - p[0] - 1

		return x, y


class Mandelbrot(Rule3):
	def __init__(self, rule_variant=0, **kwargs):
		self.rule_variant = rule_variant
		super().__init__(**kwargs)

	def step(self):
		for i in range(self.screen.size[0]):
			print(f'Generating Mandelbrot plot. Current progress: {round(100 * i / self.screen.size[0])}%', end='\r')
			for j in range(self.screen.size[1]):
				self.z = complex(0,0)
				self.c = complex(*self.screen.transform_to_range((i,j)))
				k = 0
				delta = 2 * self.epsilon
				keep_going = True
				while delta > self.epsilon and k < self.max_iters and keep_going:
					k += 1
					try:
						# new_z = (abs(self.z.real) + abs(self.z.imag))**2 + self.c
						new_z = self.calc_next_z()
						delta = abs(self.z - new_z)
						self.z = new_z
					except OverflowError:
						keep_going = False
				

				if k < self.max_iters and keep_going:
					self.screen.draw_pixel((i, j, k/self.max_iters), mandelbrot=True)
					# self.screen.draw_pixel(self.screen.transform_to_range((i,j)))

	def calc_next_z(self):
		if self.rule_variant == 0:
			return self.z**2 + self.c
		if self.rule_variant == 1:
			return complex(abs(self.z.real), abs(self.z.imag))**2 + self.c

	def set_rule(self):
		self.vars = ['epsilon', 'max_iters']
		self.equations = []
		self.name = 'Mandelbrot Set'

		self.epsilon = 10**-7
		self.max_iters = 400
		# self.rule_variant = rule_variant



class Julia(Mandelbrot):
	def __init__(self, c=complex(1,1), **kwargs):
		self.c = c
		super().__init__(**kwargs)

	def step(self):
		for i in range(self.screen.size[0]):
			print(f'Generating Julia plot. Current progress: {round(100 * i / self.screen.size[0])}%', end='\r')
			for j in range(self.screen.size[1]):
				self.z = complex(*self.screen.transform_to_range((i,j)))
				k = 0
				delta = 2 * self.epsilon
				keep_going = True
				while delta > self.epsilon and k < self.max_iters and keep_going:
					k += 1
					try:
						# new_z = (abs(self.z.real) + abs(self.z.imag))**2 + self.c
						new_z = self.calc_next_z()
						delta = abs(self.z - new_z)
						self.z = new_z
					except OverflowError:
						keep_going = False
				
				if k < self.max_iters and keep_going:
					self.screen.draw_pixel((i, j, k/self.max_iters), mandelbrot=True)
					# self.screen.draw_pixel(self.screen.transform_to_range((i,j)))

	def set_rule(self):
		self.vars = ['c', 'epsilon', 'max_iters']
		self.equations = []
		self.name = 'Julia Set'
		self.snapshots = []

class Ikeda(Rule3):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def set_rule(self):
		self.vars = ['u']
		self.equations = ['self.t = 0.4 - 6 / (1 + pow(self.x,2) + pow(self.y,2))',
						  'self.x = 1 + self.u * (self.x*math.cos(self.t)-self.y*(math.sin(self.t)))',
						  'self.y = self.u*(self.x*math.sin(self.t)+self.y*(math.cos(self.t)))']

		self.vector_equations = ['self.t = 0.4 - 6 / (1 + np.square(self.x) + np.square(self.y))',
								 'self.x = 1 + self.u * (self.x * np.cos(self.t) - self.y * np.sin(self.t))',
								 'self.y = self.u * (self.x * np.sin(self.t) + self.y * np.cos(self.t))']
		self.suggested_space = ['rangex = (-10, 10)',
								'rangey = (-10, 10)']
		self.explanation = 'Ikeda map, variable u. For u > 0.6 it has an attractor. Starting point may be anything.'

		self.u = 0.85
		self.snapshots = []


class ChaosGame(Rule3):
	def __init__(self, vertices=None, rule_variant=0, **kwargs):
		self.rule_variant = rule_variant
		self.vertices = vertices
		super().__init__(**kwargs)

	@property
	def rule_variant(self):
		return self._rule_variant

	@rule_variant.setter
	def rule_variant(self, val):
		self._rule_variant = val
		self.set_rule()
	
	def generate_vertices(self, nmbr_vertices, radius, rotation=None):
		if rotation == None:
			rotation = 0.5 * 360/nmbr_vertices
		vertices = []
		for i in range(nmbr_vertices):
			rotation += 360/(nmbr_vertices)
			vertices.append((math.cos(math.radians(rotation)) * radius, math.sin(math.radians(rotation)) * radius))

		self.vertices = vertices
		self.vert_history = [0,1,2,3,4]
		vertex_probs = np.random.rand(len(self.vertices))
		vertex_probs = vertex_probs / np.sum(vertex_probs)
		self.vertex_probs = vertex_probs.tolist()

		self.p1vert = self.vertices[0]
		self.p2vert = self.vertices[1]
		return vertices

	def draw_vertices(self, colour=(255,255,255)):
		colour = self.screen._draw_colour
		self.check_screen()
		for i in range(len(self.vertices)):
			self.screen.draw_line((self.vertices[i], self.vertices[(i+1)%len(self.vertices)]), colour)

	def choose_vertex(self):
		return random.choice(self.vertices)

	def add_vert_to_history(self):
		self.vert_history.append(self.nextvert)
		if len(self.vert_history) > 5:
			del(self.vert_history[0])

	def set_rule(self):
		self.snapshots = []
		if self.rule_variant == 0:
			self.vars = ['A', 'B']
			self.equations = ('self.nextvert = random.choice(self.vertices)',
							  'self.x = (self.nextvert[0] + self.x)*self.A',
							  'self.y = (self.nextvert[1] + self.y)*self.B')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where any vertex may be chosen. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 1:
			self.vars = ['A', 'B']
			self.nextvert = self.choose_vertex()
			self.equations = (
'''
nextnextvert = self.choose_vertex()
while self.nextvert == nextnextvert:
	nextnextvert = self.choose_vertex()
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where vertices may not be chosen two times in the row. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 2:
			self.vars = ['A', 'B']
			# self.vert_history.append(random.choice(self.vertices))
			self.nextvert = self.choose_vertex()
			self.equations = (
'''
a = self.vertices.index(self.nextvert)
nextnextvert = self.choose_vertex()
b = self.vertices.index(nextnextvert)
while (b - a)%(len(self.vertices)) == 2 or (a - b)%(len(self.vertices)) == 2:
	nextnextvert = self.choose_vertex()
	b = self.vertices.index(nextnextvert)
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where next vertex may not be two spaces away from last vertex. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 3:
			self.vars = ['A', 'B']
			# self.vert_history.append(random.choice(self.vertices))
			self.nextvert = self.choose_vertex()
			self.equations = (
'''
a = self.vertices.index(self.nextvert)
nextnextvert = self.choose_vertex()
b = self.vertices.index(nextnextvert)
while (a - b)%(len(self.vertices)) == 1:
	nextnextvert = self.choose_vertex()
	b = self.vertices.index(nextnextvert)
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where next vertex may not be one space away (counter-clockwise) from last vertex. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 4:
			self.vars = ['A', 'B']
			self.equations = (
'''
self.nextvert = self.choose_vertex()
a = self.vertices.index(self.nextvert)
b = self.vertices.index(self.p1vert)
if self.p2vert == self.p1vert:
	while (b - a)%(len(self.vertices)) == 1 or (a - b)%(len(self.vertices)) == 1:
		self.nextvert = self.choose_vertex()
		a = self.vertices.index(self.nextvert)
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B

# print(self.vertices.index(self.nextvert), self.vertices.index(self.p1vert), self.vertices.index(self.p2vert))

self.p2vert = self.p1vert
self.p1vert = self.nextvert

''')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where next vertex may not be one space away from last vertex if last two chosen vertices are the same. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 5:
			self.vars = ['A', 'B']
			self.nextvert = self.choose_vertex()
			self.equations = ('j = random.choices(list(range(len(self.vertices))), weights=self.vertex_probs)[0]',
							  'self.nextvert = self.vertices[j]',
							  'self.x = (self.nextvert[0] + self.x)*self.A',
							  'self.y = (self.nextvert[1] + self.y)*self.B')
			self.add_vert_to_history()
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where the choice of the next vertex is weighted via self.vertex_probs. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5

		if self.rule_variant == 6:
			self.vars = ['A', 'B']
			self.nextvert = self.choose_vertex()
			self.equations = (
'''
self.nextvert = self.choose_vertex()
a = self.vertices.index(self.nextvert)
b = self.vertices.index(self.p1vert)
if self.p2vert == self.p1vert:
	while (b - a)%(len(self.vertices)) != 1 or (a - b)%(len(self.vertices)) != 1:
		self.nextvert = self.choose_vertex()
		a = self.vertices.index(self.nextvert)
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B

# print(self.vertices.index(self.nextvert), self.vertices.index(self.p1vert), self.vertices.index(self.p2vert))

self.p2vert = self.p1vert
self.p1vert = self.nextvert

''')
			self.vector_equations = None
			self.suggested_space = None
			self.explanation = 'Rule variant on chaos game where next vertex may only be one space away from last vertex if last two chosen vertices are the same. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
			self.A = 0.5
			self.B = 0.5



