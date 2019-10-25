import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

rangex = (-2.5, 1)
rangey = (-1, 1)
screen = draw.Screen((1000, 1000), rangex, rangey, draw_opacity_steps=255, bkgr_colour=(0,0,0), draw_colour=(255,255,255))
rule = rule.Mandelbrot(screen=screen, plot_on_screen=True)

rule.start()

screen.show()


