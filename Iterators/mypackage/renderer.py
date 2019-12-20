import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import numpy as np
from math import cos, sin, pi, tan
import math, sys
try:
	import mypackage.colour_maps as cmap
except:
	import colour_maps as cmap
import time


class Renderer:
	def __init__(self, resolution=(0,0), rangex=None, rangey=None, colour_map=cmap.CoolWarm()):
		self.disp = pg.surface.Surface(resolution)
		self.resolution = resolution
		self.rangex = rangex
		self.rangey = rangey
		self.colour_map = colour_map
		self.pixel_array = np.zeros(resolution)

	@property
	def resolution(self):
		return self._resolution
	
	@resolution.setter
	def resolution(self, val):
		self._resolution = val
		self.disp = pg.surface.Surface(val)
		

	def clear(self):
		self.pixel_array = np.zeros(resolution)

	def map_rgb_to_surface(self, array):
		print(array)
		return cmap.Ocean[array]

	def blit_array(self, array):
		pg.surfarray.blit_array(self.disp, self.colour_map[self.pixel_array])

	def show(self, clickable=True):
		self.blit_array(self.pixel_array)
		dest = pg.display.set_mode(self.resolution)
		dest.blit(self.disp, (0,0))
		pg.display.flip()
		keepon = True
		prev_press = 0
		while keepon:
			if clickable:
				if pg.mouse.get_pressed()[0] and not prev_press:
					x, y = pg.mouse.get_pos()
					print(x*(self.rangex[1]-self.rangex[0]) / self.resolution[0] + self.rangex[0], y*(self.rangey[1]-self.rangey[0]) / self.resolution[1] + self.rangey[0])

				prev_press = pg.mouse.get_pressed()[0]

			if pg.key.get_pressed()[pg.K_ESCAPE]:
				keepon = False
			for event in pg.event.get():
				if event.type == pg.QUIT:
					  keepon = False
					  pg.quit()

	def save(self, path):
		self.blit_array(self.pixel_array)
		pg.image.save(self.disp, path)

	def input_array(self, array):
		self.pixel_array = array
		self.resolution = array.shape

	def input_pos(self, poss, auto_size=True):
		x, y = np.hsplit(poss, 2)
		if auto_size:
			self.rangex = x.min(), x.max()
			self.rangey = y.min(), x.max()
		x, y = self.transform_to_disp((x,y))

		poss = np.append(x, y)

		pa = self.pixel_array
		for p in poss:
			pa[p[0],p[1]] += 1

		self.pixel_array = pa

		return pa

	def transform_to_disp(self, pos):
		if type(pos) is tuple:
			x, y = pos
		else:
			x, y = np.hsplit(pos,2)[0], np.hsplit(pos,2)[1]

		x = ((x - self.rangex[0])*(self.resolution[0]-1)/(self.rangex[1]-self.rangex[0]))
		y = ((y - self.rangey[0])*(self.resolution[1]-1)/(self.rangey[1]-self.rangey[0]))

		return x.astype(int), y.astype(int)


def draw_cmap_sample(colour_map):
	res = (600,200)
	print(colour_map.cycles)
	array = np.empty(res)
	s = Renderer(res, colour_map=colour_map)
	for y in range(res[1]):
		for x in range(res[0]):
			array[x,y] = x
	s.input_array(array)
	s.show(clickable=False)


# def mandelbrott(x, y, res, rangex, rangey, max=400):
# 	c = complex(x/res[0]*(rangex[1]-rangex[0])+rangex[0], y/res[1]*(rangey[1]-rangey[0])+rangey[0])
# 	i = z = 0
# 	while i < max and abs(z) <= 2:
# 		z = z**2 + c
# 		i += 1

# 	return i



# res = (600,200)

# rangex=(-0.5997039466666666, -0.5992148133333333)
# rangey=(0.663875215, 0.6645834983333333)

# array = np.empty(res)

# s = Renderer(res, rangex=rangex, rangey=rangey, colour_map=cmap.Hot(cycles=1))

# # for y in range(res[0]):
# # 	for x in range(res[1]):
# # 		array[x,y] = mandelbrott(x, y, res, rangex, rangey)


# for y in range(res[1]):
# 	for x in range(res[0]):
# 		array[x,y] = x

# s.input_array(array)
# s.show()