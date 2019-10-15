import pygame as pg 
import numpy as np 
import math
import colour as c


class Grid:
	def __init__(self, cell_size=20, size=[[-5, 5],[-5, 5]], number_of_grid_lines=10):
		self.cell_size = cell_size
		#size[0] is size in x-direction, size[1] is size in y-direction. First index is size in negative direction, rel. origin and second positive
		self.size = size
		self.values = np.zeros((self.length_vertical, self.length_horizontal))
		# self.values = np.random.choice(2, (self.length_vertical, self.length_horizontal))
		# self.values = np.random.rand(self.length_vertical, self.length_horizontal)
		self.colours = None
		self.max_value = 0
		self.number_of_grid_lines = number_of_grid_lines

	@property 
	def length_horizontal(self):
		#+1 because we must count (0,0) as well
		return (self.size[0][1] - self.size[0][0]) + 1

	@property 
	def length_vertical(self):
		return (self.size[1][1] - self.size[1][0]) + 1


	def extend_horizontal(self, direction):
		if direction == -1:
			obj = 0
			self.size[0][0] -= 1
			
		elif direction == 1:
			obj = self.length_horizontal
			self.size[0][1] += 1

		self.values = np.insert(self.values, obj, 0, 1)

	def extend_vertical(self, direction):
		if direction == -1:
			obj = 0
			self.size[1][0] -= 1
			
		elif direction == 1:
			obj = self.length_vertical
			self.size[1][1] += 1
			
		self.values = np.insert(self.values, obj, 0, 0)

	def get_value(self, pos):
		x, y = pos[0] - self.size[0][0], pos[1] - self.size[1][0]
		return self.values[y][x]

	def set_value(self, pos, value):
		x, y = pos[0] - self.size[0][0], pos[1] - self.size[1][0]
		self.values[y][x] = value

	def check_size(self, pos):
		if pos[0] > self.size[0][1]:
			self.extend_horizontal(1)
		if pos[0] < self.size[0][0]:
			self.extend_horizontal(-1)
		if pos[1] > self.size[1][1]:
			self.extend_vertical(1)
		if pos[1] < self.size[1][0]:
			self.extend_vertical(-1)

		# print(self.values)

	def get_grid_surface(self, ant_pos):
		size = ((self.length_horizontal)*self.cell_size+1, (self.length_vertical)*self.cell_size+1)
		# print(grid_surface)
		surface = pg.Surface(size)
		surface.fill((255,255,255))

		

		coords = []

		for h in range(self.length_horizontal):
			for v in range(self.length_vertical):
				x = h * self.cell_size
				y = v * self.cell_size

				value = int(self.values[v][h])
				if self.colours == None:
					white = c.Color(rgb=(1,1,1))
					self.colours = list(white.range_to(c.Color(rgb=(0.8,0.2,0)), self.max_value))
				color = 255*np.asarray(self.colours[value].rgb)
				

				rect = pg.Rect(x, y, self.cell_size, self.cell_size)
				pg.draw.rect(surface, color, rect)

		if self.draw_grid:
			y_max = self.length_vertical * self.cell_size
			f = math.floor(self.length_horizontal/self.number_of_grid_lines)
			for h in range(self.length_horizontal):
				if h%f == 0:
					x = h * self.cell_size
					coords.append([(x, 0), (x, y_max)])
					if h == self.length_horizontal - 1:
						x = (h + 1) * self.cell_size
						coords.append([(x, 0), (x, y_max)])

			x_max = self.length_horizontal * self.cell_size
			f = math.floor(self.length_vertical/self.number_of_grid_lines)
			for v in range(self.length_vertical):
				if v%f == 0:
					y = v * self.cell_size
					coords.append([(0, y), (x_max, y)])
					if v == self.length_vertical - 1:
						y = (v + 1) * self.cell_size
						coords.append([(0, y), (x_max, y)])

			for coord in coords:
					pg.draw.line(surface, (150,150,150), coord[0], coord[1], 1)

		x, y = ant_pos[0] - self.size[0][0], ant_pos[1] - self.size[1][0]
		center = (int((x + 0.5) * self.cell_size), int((y + 0.5) * self.cell_size))
		pg.draw.circle(surface, (0,0,0), center, int(self.cell_size/4))

		return surface

class Ant:
	def __init__(self, pos=[0,0], direction=0):
		self.grid = Grid()
		self.pos = pos
		self.direction = direction

	def forward(self):
		#direction 0 is up, 1 is right, 2 is down, 3 is left
		if self.direction == 0:
			self.pos[1] -= 1
		if self.direction == 1:
			self.pos[0] += 1
		if self.direction == 2:
			self.pos[1] += 1
		if self.direction == 3:
			self.pos[0] -= 1

		self.grid.check_size(self.pos)

	def rotate(self, direction):
		# +1 is right rotate, -1 is left rotate
		self.direction += direction
		self.direction = self.direction % 4

	def get_value(self):
		return self.grid.get_value(self.pos)

	def set_value(self, value):
		return self.grid.set_value(self.pos, value)

	def walk(self, iterations=-1, rule='LR', draw=True, resolution=(1280, 720), FPS=5, draw_every_frame=False, draw_grid=True):
		if draw:
			self.display = Display(resolution, FPS)

		self.grid.draw_grid = draw_grid
		self.grid.max_value = len(rule)

		i = 0
		while i != iterations:
			self.display.tick()
			if (i % math.ceil(FPS/5) == 0 or draw_every_frame):
				self.display.surface.fill((255,255,255))
				grid_surface = self.grid.get_grid_surface(self.pos)
				pg.transform.scale(grid_surface, resolution, self.display.surface)
				pg.display.flip()

			if i == 0:
				self.forward()

			self.rule(rule)

			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()
			i += 1

		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()

	def rule(self, rule='LR'):
		directions = []
		for c in rule:
			if c == 'L':
				directions.append(-1)
			if c == 'R':
				directions.append(1)

		curr_val = int(self.get_value())
		self.set_value((curr_val + 1) % len(rule))
		self.rotate(directions[curr_val])
		self.forward()

		# # print(int(self.get_value()) == 1)
		# if int(self.get_value()) == 0:
		# 	self.set_value(1)
		# 	self.rotate(1)

		# elif int(self.get_value()) == 1:
		# 	self.set_value(0)
		# 	self.rotate(-1)
			
		# # print(self.get_value())
		# self.forward()



class Display:
	def __init__(self, resolution, FPS):
		self.resolution = resolution
		self.FPS = FPS
		self.surface = pg.display.set_mode(resolution)
		# print(self.surface)
		self.clock = pg.time.Clock()

	def tick(self):
		self.clock.tick(self.FPS)

