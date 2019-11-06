import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os
import numpy as np
import pygame as pg

#Snapshots
def BHsnapshots(variant=0):
	if variant == 0:
		attractor = rule.BHAttractor(a=0.65343, b=0.7345345)

	if variant == 1:
		attractor = rule.BHAttractor(a=-0.81, b=-0.92)

	if variant == 2:
		attractor = rule.BHAttractor(a=0.06, b=0.98)

	if variant == 3:
		attractor = rule.BHAttractor(a=-0.67, b=0.83)

	path = os.getcwd() + f'\\attractor_frames\\BHAttractor_{attractor.a}_{attractor.b}.bmp'
	screen = draw.Screen((1600, 900))

	return screen, attractor, path

def GMsnapshots(variant=0):
	if variant == 0:
		attractor = rule.GMAttractor(a=-0.31, b=1)
		start_pos = (0,0.5)

	if variant == 1:
		attractor = rule.GMAttractor(a=-0.012, b=0.9186)
		start_pos = (-0.61, 0.1)

	if variant == 2:
		attractor = rule.GMAttractor(a=-0.77, b=0.95)
		start_pos = (0.1, 0.1)

	path = os.getcwd() + f'\\attractor_frames\\GMAttractor_{attractor.a}_{attractor.b}.bmp'
	screen = draw.Screen((1600, 900))

	return screen, attractor, start_pos, path

def JR1snapshots(variant=0):
	if variant == 0:
		attractor = rule.JR1Attractor(a=2.6, b=-2.5995, c=-2.9007, d=0.3565)

	if variant == 1:
		attractor = rule.JR1Attractor(a=-2.7918, b=2.1196, c=1.0284, d=0.1384)

	path = os.getcwd() + f'\\attractor_frames\\JR1Attractor_{attractor.a}_{attractor.b}_{attractor.c}_{attractor.d}.bmp'
	screen = draw.Screen((500, 500))

	return screen, attractor, path


screen, attractor, path = JR1snapshots(1)
screen.draw_opacity_steps = 2
screen.draw_colour = (200, 20, 75)
screen.bkgr_colour = (225, 225, 225)

poss = attractor.iterate(10000, iter_skip=1000)
# screen.draw_pixels(poss, auto_size=True)
disp = screen.disp
arr = pg.surfarray.array2d(screen.disp)
# arr.unmap_rgb(0)

for i in range(500):
	print(arr[i][i])
	arr[i][i] = disp.map_rgb((255,0,0))

screen.disp = pg.surfarray.make_surface(arr)
print(arr)

screen.save(path)
screen.show()