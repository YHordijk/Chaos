from mypackage.rule import *
from mypackage.drawer import *
import pygame
from random import randrange


#setup
SIZE = WIDTH, HEIGHT = 1080, 1080
disp = pygame.display.set_mode(SIZE)


rangey = (0,1)
rangex = (0,1)

color = (255,255,255,255)

#number of starting points
P = WIDTH
iters = 300
u= 0.995

rule = Rule2(4)
##for k in range(990, 1150):
##    print(k)
##    u = k/1000
disp.fill((0,0,0))
for i in range(0,P):
    print(i)
    #generate starting pos from range
    x = randrange(rangex[0]*100,rangex[1]*100)/100
    y = randrange(rangey[0]*100,rangey[1]*100)/100
    
    for j in range(0,iters):
        oldx, oldy = x, y
        x,y = rule.iterate(x=x, y=y, u=u, a=6.2, k=.5)
        draw_pixel(disp, x, y, color, rangex, rangey, SIZE)

pygame.display.flip()
##    pygame.image.save(disp, "C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\ikeda frames\\hires2-{}.png".format(k))


keepon = True
while keepon:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              keepon = False
