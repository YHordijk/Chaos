import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

screen = draw.Screen((200, 200), None, None, draw_opacity_steps=3, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.StrangeAttractor(rule_string='AMTMNQQXUYGA')
rule.find_best_size()