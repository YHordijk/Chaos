import mypackage.rule as rule
import mypackage.drawer as draw
import random
from datetime import datetime
import math
import numpy as np

rangex = (-16, 16)
rangey = (-9, 9)
screen = draw.Screen((1280, 720), rangex, rangey, draw_opacity_steps=15)
rule = rule.ChaosGame(screen=screen, plot_on_screen=True)
rule.rule_variant = 1
rule.generate_vertices(5, 8)
rule.set_rule()
rule.iterate((0,0), 1000000)

rule.draw_vertices()
screen.show()
