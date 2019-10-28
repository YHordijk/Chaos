import mypackage.rule as rule
import mypackage.drawer as draw
import random
import math
import os

#good values for julia sets using burning ship function:
#(-0.8727956777951056-0.28632560361827397j)

rangex = (-2, 2)
rangey = (-2, 2)

# rangex = (-0.2375, -0.125)
# rangey = (0.644, 0.715)
screen = draw.Screen((3000, 3000), rangex, rangey, draw_opacity_steps=50, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
# screen = draw.Screen((640, 640), rangex, rangey, draw_opacity_steps=50, bkgr_colour=(255,255,255), draw_colour=(0,0,0))
rule = rule.Mandelbrot(screen=screen, plot_on_screen=True, rule_variant=1)
# rule = rule.Julia(screen=screen, plot_on_screen=True, c=complex(-0.7269, 0.1889), rule_variant=0)
# rule = rule.Julia(screen=screen, plot_on_screen=True, c=complex(3*random.random()-2, 2*random.random()-1), rule_variant=0)
# print(rule.c)

# print(screen.transform_to_range((2350, 1918)))

rule.start()
path = os.getcwd() + f'\\mandelbrot_frames\\julia_{rule.rule_variant}_{rule.c}.bmp'
# screen.show()
screen.save(path)
