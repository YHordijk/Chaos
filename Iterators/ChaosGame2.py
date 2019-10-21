import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

rangex = (-1, 1)
rangey = (-1, 1)
screen = draw.Screen((300, 300), rangex, rangey, draw_opacity_steps=1, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.ChaosGame(screen=screen, plot_on_screen=True)
rule.generate_vertices(6, 1)
rule.rule_variant = 5

iters = 5000
rule.iterate((0,0), iters, iter_skip=10)

rule.draw_vertices()

path = os.getcwd() + f'\\chaos_game_frames\\{rule.rule_variant}_{iters}.bmp'
print(path)
screen.save(path)
