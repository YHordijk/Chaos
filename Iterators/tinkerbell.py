from mypackage.rule import *
from mypackage.drawer import *
import pygame
from random import randrange
from math import pi

pygame.init()

#setup
SIZE = WIDTH, HEIGHT = 400, 400
disp = pygame.display.set_mode(SIZE)
disp.fill((0,0,0))

rangey = (0.6, -1.6)
rangex = (-1.5, 0.5)



iters = 2000

x = -0.72
y = -0.64

rule = Rule2(6)
rule.set_standard()

color = (255,255,255)

draw_pixel(disp, 0, 0, color, rangex, rangey, SIZE)
pygame.display.flip()

for i in range(0,iters):
	x, y = rule.iterate(x=x, y=y)
	draw_pixel(disp, x, y, color, rangex, rangey, SIZE)
pygame.display.flip()

keepon = True
while keepon:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			  keepon = False
