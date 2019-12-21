# import mypackage.drawer2 as draw
# import mypackage.colour as cmap
# import random
# import math
# import os
import time
import numpy as np

resolution = (720, 720)
rangex = (-2.5,1.5)
rangey = (-2,2)

def mandelbrot(c):
	i = z = 0
	while i < 15 and abs(z) < 2:
		z = z**2 + c
		i += 1
	return i

start = time.perf_counter()
array = np.empty(resolution)
for i, x in enumerate(np.linspace(*rangex, resolution[0])):
	for j, y in enumerate(np.linspace(*rangey, resolution[1])):
		array[i,j] = mandelbrot(complex(x,y))
print(time.perf_counter()-start)


start = time.perf_counter()
array = np.empty(resolution)
for i, x in enumerate(np.linspace(*rangex, resolution[0])):
	for j, y in enumerate(np.linspace(*rangey, resolution[1])):
		counter = z = 0
		c = complex(x,y)
		while counter < 15 and abs(z) < 2:
			z = z**2 + c
			counter += 1
		array[i,j] = counter
print(time.perf_counter()-start)


start = time.perf_counter()
array = np.empty(resolution)
code = compile('z**2 + c', '', 'eval', optimize=2)
print(code)
for i, x in enumerate(np.linspace(*rangex, resolution[0])):
	for j, y in enumerate(np.linspace(*rangey, resolution[1])):
		counter = z = 0
		c = complex(x,y)
		while counter < 15 and abs(z) < 2:
			z = eval(code)
			counter += 1
		array[i,j] = counter
print(time.perf_counter()-start)