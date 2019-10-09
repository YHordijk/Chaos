from mypackage.rule import *
from mypackage.drawer import *
import pygame
from random import randrange
import numpy as np

SIZE = WIDTH, HEIGHT = 800, 800
disp = pygame.display.set_mode(SIZE)
disp.fill((0,0,0))

color = (255,255,255)

rangey = (-20, 20)
rangex = (-20, 20)

points = np.array([[0,0],[0,0]])
points = np.array([[0,0], [3,0],[0,3],[0,-4],[-4,0],[0,8]])

clock = pygame.time.Clock()

FPS = 120
rungame = True

accel = 1

updt = 0
while rungame:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        points -= np.array([accel, 0])
    if keys[pygame.K_RIGHT]:
        points += np.array([accel, 0])
    if keys[pygame.K_UP]:
        points -= np.array([0, accel])
    if keys[pygame.K_DOWN]:
        points += np.array([0, accel])
            
    
    disp.fill((0,0,0))
    clock.tick_busy_loop(FPS)/1000
    updt += 1
    rot = 0.2*updt/(2*pi)
    for point in points:
        draw_pixel(disp, point[0], point[1], color, rangex, rangey, SIZE, rot=rot)



    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              rungame = False
