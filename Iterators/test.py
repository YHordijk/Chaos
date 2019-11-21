import mypackage.drawer2 as draw
import mypackage.colour as cmap
import random
import math
import os
import time

l = 600

s = draw.Screen((l,300), rangex=(-1,1), rangey=(-1,1))
c = cmap.Hot()


for x in range(l):
	s.draw_line(((2*x/l-1,-1),(2*x/l-1,1)), c[x/l])

s.show()
