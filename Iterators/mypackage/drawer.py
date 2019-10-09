from pygame import surface
from pygame import display
from pygame import draw
import numpy as np
from math import cos, sin, pi

def transform_range(x, y, rangex, rangey, SIZE):
    #takes position in rangex, rangey and outputs position on SIZE
    x = round((x - rangex[0])*SIZE[0]/(rangex[1]-rangex[0]))
    y = round((y - rangey[0])*SIZE[1]/(rangey[1]-rangey[0]))
    return int(round(x)), int(round(y))

def rotate(x, y, rot, SIZE):
    x -= SIZE[0]/2
    y -= SIZE[1]/2
    
    newx = x * cos(rot) - y * sin(rot)
    newy = x * sin(rot) + y * cos(rot)
    
    newx += SIZE[0]/2
    newy += SIZE[1]/2
    return int(round(newx)), int(round(newy))

def draw_pixel(disp, x, y, color, rangex, rangey, SIZE, rot=None):
    x, y = transform_range(x, y, rangex, rangey, SIZE)
    if rot is not None:
        x, y = rotate(x, y, rot, SIZE)
    if len(color) == 4:

        a = color[3]
        try:
            color = disp.get_at((x,y))
            c1 = max(color[0]-a, 0)
            c2 = max(color[1]-a, 0)
            c3 = max(color[2]-a, 0)

            color = (c1, c2, c3)
        except:
            pass
        
    
    disp.set_at((x,y), color)
    return x, y

def draw_line(disp, oldx, oldy, x, y, color, rangex, rangey, SIZE, aa=False, rot=None):
    oldx, oldy = transform_range(oldx, oldy, rangex, rangey, SIZE)
    x, y = transform_range(x, y, rangex, rangey, SIZE)
    if rot is not None:
        x, y = rotate(x, y, rot)
    if aa:
        draw.aaline(disp, color, (oldx, oldy), (x, y), True)
    else:
        draw.line(disp, color, (oldx, oldy), (x, y))

