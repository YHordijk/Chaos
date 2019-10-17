from mypackage.rule import *
from mypackage.drawer import *
import pygame
from random import randrange
from math import pi

pygame.init()

#setup
SIZE = WIDTH, HEIGHT = 1600, 900
disp = pygame.display.set_mode(SIZE)
disp.fill((255,255,255))

rangex = (-1, 1)
rangey = (-0.5, 1.5)

steps = WIDTH
iterperstep = 2000
convergepercent = 0.5
starty = randrange(1,99)/100

color = (255,255,255, 10)

rule = Rule2(3)

dx = rangex[1]-rangex[0]
dy = rangey[1]-rangey[0]

rot = 0/(2*pi)

#main loop
for i in range(0,steps):
	y = starty
	x = rangex[0]+dx/steps*i
	for j in range(0,iterperstep):
		x,y = rule.iterate(x=x, y=y, a=6.2)
		if j>iterperstep*convergepercent:
			draw_pixel(disp, x, y, color, rangex, rangey, SIZE, rot=rot)
	# print(i)
pygame.display.flip()

keepon = True
while keepon:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			  keepon = False
