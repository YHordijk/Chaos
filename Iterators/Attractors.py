import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os
import numpy as np

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


screen, attractor, path = BHsnapshots(3)
screen.draw_opacity_steps = 7

poss = attractor.iterate(1000000, iter_skip=1000)
screen.draw_pixels(poss, auto_size=True)

screen.save(path)
screen.show()
