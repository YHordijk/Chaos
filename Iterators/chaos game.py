from mypackage.rule import *
from mypackage.drawer import *
import pygame

SIZE = WIDTH, HEIGHT = 800, 800
disp = pygame.display.set_mode(SIZE)
disp.fill((255,255,255))

rangex = (-240, 240)
rangey = (-180, 180)

verteces = [(0, 150), (150, 0), (0, -150), (-150, 0)]
rule = ChaosGameRule(rule=1, verteces=verteces)
iters = 50000
color = (255,255,255,20)

x, y = 0, 0

for i in range(0, iters):
	x,y = rule.iterate(x=x, y=y, A=0.5, B=0.5)
	draw_pixel(disp, x, y, color, rangex, rangey, SIZE)

pygame.display.flip()

keepon = True
while keepon:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              keepon = False