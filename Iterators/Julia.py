import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

screen = draw.Screen((200, 200), None, None, draw_opacity_steps=3, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.Julia(screen=screen, plot_on_screen=True, c=complex(-0.7269, 0.1889))

rule.start(set_standard_size=True, rule_variant=3)
path = os.getcwd() + f'\\mandelbrot_frames\\julia_{rule.rule_variant}_{rule.c}.bmp'
screen.save(path)
screen.show()