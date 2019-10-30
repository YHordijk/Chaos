import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os
import numpy as np

#Snapshots
def snapshots(variant=0):
	if variant == 0:
		rangex = (-80, 80)
		rangey = (-80, 80)
		attractor = rule.GMAttractor(a=-0.31, b=1)
		start_pos = (0,0.5)

	if variant == 1:
		rangex = (-20, 20)
		rangey = (-20, 20)
		attractor = rule.GMAttractor(a=-0.012, b=0.9186)
		start_pos = (-0.61, 0.1)

	if variant == 2:
		rangex = (-15, 20)
		rangey = (-10, 10)
		attractor = rule.GMAttractor(a=-0.77, b=0.95)
		start_pos = (0.1, 0.1)

	screen = draw.Screen((1600, 900), rangex, rangey)
	return screen, attractor, start_pos




# screen, attractor, start_pos = snapshots(0)

# screen.draw_opacity_steps = 7
# screen.clear()
# screen.draw_pixels(attractor.iterate(start_pos, 100000))
# screen.show()

rangex = (-30, 30)
rangey = (-30, 30)
attractor = rule.HLAttractor()
screen = draw.Screen((1200, 720), rangex, rangey)
screen.draw_opacity_steps = 5
poss = attractor.iterate((0,0), 100000)
path = os.getcwd() + f'\\attractor_frames\\HLAttractor_{attractor.a}_{attractor.b}_{attractor.c}.bmp'
screen.draw_pixels(poss)
screen.save(path)
screen.show()
