import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

# rangex = (-2, 1)
# rangey = (-1, 1)

rangex = (-0.2375, -0.125)
rangey = (0.644, 0.715)
screen = draw.Screen((4000, 2250), rangex, rangey, draw_opacity_steps=50, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
# screen = draw.Screen((500, 500), rangex, rangey, draw_opacity_steps=50, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.Mandelbrot(screen=screen, plot_on_screen=True)

# print(screen.transform_to_range((2350, 1918)))

rule.start()
path = os.getcwd() + f'\\mandelbrot_frames\\mandelbrot3.bmp'
# screen.show
screen.save(path)


