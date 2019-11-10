import mypackage.rule2 as rule
import mypackage.drawer as draw
import random
import math
import os
import time



r = rule.JR1Attractor()
r.load_snapshot(2)
s = draw.Screen(resolution=(700,500), draw_opacity_steps=4)
r.generate(screen=s, iter_skip=10)
s.show()