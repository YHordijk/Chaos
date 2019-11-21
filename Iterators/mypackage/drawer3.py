import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import numpy as np
from math import cos, sin, pi
import mypackage.colour as cmap

class Screen:
	def __init__(self, resolution, rangex=None, rangey=None, cmap=cmap.CoolWarm):
		self.disp = pg.surface.Surface(resolution)
		self.disp.fill(bkgr_colour)
		self.bkgr_colour = bkgr_colour
		self.resolution = resolution
		self.rangex = rangex
		self.rangey = rangey
		self.cmap = cmap
		self.pixel_array = np.zeros(resolution)


	def clear(self):
		self.disp.fill(self.bkgr_colour)

	def draw_pixel(self, pos, colour, rot=None):
		try:
			x, y = self.transform_to_disp(pos)
			if rot is not None:
				x, y = self.rotate(x, y, rot, size)

			self.disp.set_at((x,y), colour)
		except:
			pass

	def draw_pixels(self, poss, rot=None, auto_size=False):
		if auto_size:
			x = [i[0] for i in poss]
			self.rangex = min(x), max(x)
			y = [i[1] for i in poss]
			self.rangey = min(y), max(y)

		for pos in poss:
			self.draw_pixel(pos, rot)

	def transform_to_range(self, pos):
		x, y = pos[0], pos[1]
		x = x*(self.rangex[1]-self.rangex[0]) / self.resolution[0] + self.rangex[0]
		y = y*(self.rangey[1]-self.rangey[0]) / self.resolution[1] + self.rangey[0]
		return x, y

	def transform_to_disp(self, pos):
		#takes position in rangex, rangey and outputs position on size
		x, y = pos[0], pos[1]
		x = round((x - self.rangex[0])*self.resolution[0]/(self.rangex[1]-self.rangex[0]))
		y = round((y - self.rangey[0])*self.resolution[1]/(self.rangey[1]-self.rangey[0]))
		return int(x), int(y)

	def rotate(self, x, y, rot):
		x -= self.resolution[0]/2
		y -= self.resolution[1]/2
		
		newx = x * cos(rot) - y * sin(rot)
		newy = x * sin(rot) + y * cos(rot)
		
		newx += self.resolution[0]/2
		newy += self.resolution[1]/2
		return int(newx), int(newy)

	def show(self):
		dest = pg.display.set_mode(self.resolution)
		dest.blit(self.disp, (0,0))
		pg.display.flip()
		keepon = True
		while keepon:
			if pg.key.get_pressed()[pg.K_ESCAPE]:
				keepon = False
			for event in pg.event.get():
				if event.type == pg.QUIT:
					  keepon = False

	def save(self, path):
		pg.image.save(self.disp, path)

	def draw_line(self, points, colour):
		print(points)
		p1 = self.transform_to_disp(points[0])
		p2 = self.transform_to_disp(points[1])
		pg.draw.line(self.disp, colour, p1, p2)



def draw_line(disp, oldx, oldy, x, y, color, rangex, rangey, size, aa=False, rot=None):
	oldx, oldy = transform_to_disp(oldx, oldy, rangex, rangey, size)
	x, y = transform_to_disp(x, y, rangex, rangey, size)
	if rot is not None:
		x, y = rotate(x, y, rot)
	if aa:
		draw.aaline(disp, color, (oldx, oldy), (x, y), True)
	else:
		draw.line(disp, color, (oldx, oldy), (x, y))
