import pygame as pg
import numpy as np
from math import cos, sin, pi
import colour as clr

class Screen:
    def __init__(self, size, rangex, rangey, bkgr_colour=(0,0,0), draw_colour=(255,255,255), draw_opacity_steps=10):
        self.disp = pg.surface.Surface(size)
        self.disp.fill(bkgr_colour)
        # self.disp = pg.display.set_mode(size)
        self.size = size
        self.rangex = rangex
        self.rangey = rangey
        self._bkgr_colour = bkgr_colour
        self._draw_colour = draw_colour
        self.draw_opacity_steps = min(255, draw_opacity_steps)
        self.set_draw_colour_grad()

    def set_draw_colour_grad(self):
        c1 = clr.Color(rgb=list(np.asarray(self._bkgr_colour)/255))
        c2 = clr.Color(rgb=list(np.asarray(self._draw_colour)/255))

        range = list(c1.range_to(c2, self.draw_opacity_steps))

        self.draw_colour_grad = [tuple((np.asarray(c.rgb)*255).astype(int)) for c in range]
        self.draw_colour_grad[0] = self.bkgr_colour

    @property 
    def bkgr_colour(self):
        return self._bkgr_colour

    @property
    def draw_colour(self):
        return self._draw_colour

    @bkgr_colour.setter
    def bkgr_colour(self, val):
        self._bkgr_colour = val
        self.set_draw_colour_grad()
        return self._bkgr_colour

    @draw_colour.setter
    def draw_colour(self, val):
        self._draw_colour = val
        self.set_draw_colour_grad()
        return self._draw_colour

    def draw_pixel(self, pos, rot=None):
        try:
            x, y = self.transform_range(pos)
            if rot is not None:
                x, y = self.rotate(x, y, rot, size)

            colour = self.disp.get_at((x,y))
            index = min(self.draw_colour_grad.index(colour) + 1, self.draw_opacity_steps - 1)
            colour = self.draw_colour_grad[index]

            self.disp.set_at((x,y), colour)
        except:
            pass

    def draw_pixels(self, poss, rot=None):
        for pos in poss:
            self.draw_pixel(pos, rot)


    def transform_range(self, pos):
        #takes position in rangex, rangey and outputs position on size
        x, y = pos[0], pos[1]
        x = round((x - self.rangex[0])*self.size[0]/(self.rangex[1]-self.rangex[0]))
        y = round((y - self.rangey[0])*self.size[1]/(self.rangey[1]-self.rangey[0]))
        return int(x), int(y)

    def rotate(self, x, y, rot):
        x -= self.size[0]/2
        y -= self.size[1]/2
        
        newx = x * cos(rot) - y * sin(rot)
        newy = x * sin(rot) + y * cos(rot)
        
        newx += self.size[0]/2
        newy += self.size[1]/2
        return int(newx), int(newy)

    def show(self):
        dest = pg.display.set_mode(self.size)
        dest.blit(self.disp, (0,0))
        pg.display.flip()
        keepon = True
        while keepon:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                      keepon = False

    def save(self, path):
        pg.image.save(self.disp, "C:\\Users\\Yuman\\Desktop\\Programmeren\\Python\\PyGame\\Chaos\\ikeda frames\\hires2-{}.png".format(k))

# def draw_pixel(disp, x, y, colour, rangex, rangey, size, rot=None):
#     x, y = transform_range(x, y, rangex, rangey, size)
#     if rot is not None:
#         x, y = rotate(x, y, rot, size)
#     if len(coloru) == 4:

#         a = colour[3]
#         try:
#             colour = disp.get_at((x,y))
#             c1 = max(colour[0]-a, 0)
#             c2 = max(colour[1]-a, 0)
#             c3 = max(colour[2]-a, 0)

#             colour = (c1, c2, c3)
#         except:
#             pass
        
    
#     disp.set_at((x,y), colour)
#     return x, y

def draw_line(disp, oldx, oldy, x, y, color, rangex, rangey, size, aa=False, rot=None):
    oldx, oldy = transform_range(oldx, oldy, rangex, rangey, size)
    x, y = transform_range(x, y, rangex, rangey, size)
    if rot is not None:
        x, y = rotate(x, y, rot)
    if aa:
        draw.aaline(disp, color, (oldx, oldy), (x, y), True)
    else:
        draw.line(disp, color, (oldx, oldy), (x, y))