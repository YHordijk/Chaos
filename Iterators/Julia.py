import mypackage.rule2 as rule
import mypackage.drawer2 as draw
import random
import math
import os
import numpy as np

screen = draw.Screen((3000, 3000), (-1.5, 1.5), (-1.5, 1.5), draw_opacity_steps=60, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.Julia(screen=screen, plot_on_screen=True, max_iters=120, rule_variant=0)
c = 0 + 2j
rule.c = c
rule.generate(e=2)
# path = os.getcwd() + f'\\mandelbrot_frames\\julia_{rule.rule_variant}_{rule.c}.bmp'
path = os.getcwd() + f'\\mandelbrot_frames\\julia_bs_{c}.bmp'
screen.save(path)
screen.show()

