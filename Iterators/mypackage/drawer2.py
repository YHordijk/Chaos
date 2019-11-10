import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import numpy as np
from math import cos, sin, pi
import colour as clr

class Screen:
    def __init__(self, resolution, rangex=None, rangey=None, bkgr_colour=(0,0,0), draw_colour=(255,255,255), draw_opacity_steps=1):
        self.disp = pg.surface.Surface(resolution)
        self.disp.fill(bkgr_colour)
        # self.disp = pg.display.set_mode(size)
        self.resolution = resolution
        self.rangex = rangex
        self.rangey = rangey
        self._bkgr_colour = bkgr_colour
        self._draw_colour = draw_colour
        self._draw_opacity_steps = draw_opacity_steps
        self.set_draw_colour_grad()

    @property
    def draw_opacity_steps(self):
        return self._draw_opacity_steps

    @draw_opacity_steps.setter
    def draw_opacity_steps(self, val):
        self._draw_opacity_steps = val
        self.set_draw_colour_grad()
        return self._draw_opacity_steps
    

    def set_draw_colour_grad(self):
        if self._draw_opacity_steps > 1:
            c1 = clr.Color(rgb=list(np.asarray(self._bkgr_colour)/255))
            c2 = clr.Color(rgb=list(np.asarray(self._draw_colour)/255))

            range = list(c1.range_to(c2, self._draw_opacity_steps))

            self.draw_colour_grad = [tuple((np.asarray(c.rgb)*255).astype(int)) for c in range]
            self.draw_colour_grad[0] = self.bkgr_colour
            a = len(self.draw_colour_grad)
            self.draw_colour_grad = list(sorted(set(self.draw_colour_grad), key=self.draw_colour_grad.index))
            b = len(self.draw_colour_grad)
            if not a == b:
                print(f'Could only generate colour gradient of length {b}, instead of required {a}.')
        else:
            self.draw_colour_grad = [self._bkgr_colour, self._draw_colour]


    def clear(self):
        self.disp.fill(self.bkgr_colour)

    @property 
    def bkgr_colour(self):
        return self._bkgr_colour

    @property
    def draw_colour(self):
        return self._draw_colour

    @bkgr_colour.setter
    def bkgr_colour(self, val):
        self.disp.fill(val)
        self._bkgr_colour = val
        self.set_draw_colour_grad()
        return self._bkgr_colour

    @draw_colour.setter
    def draw_colour(self, val):
        self._draw_colour = val
        self.set_draw_colour_grad()
        return self._draw_colour

    def draw_pixel(self, pos, rot=None, mandelbrot=False):
        if not mandelbrot:
            try:
                x, y = self.transform_to_disp(pos)
                if rot is not None:
                    x, y = self.rotate(x, y, rot, size)

                colour = self.disp.get_at((x,y))
                index = min(self.draw_colour_grad.index(colour) + 1, self.draw_opacity_steps)
                colour = self.draw_colour_grad[index]

                self.disp.set_at((x,y), colour)
            except:
                pass
        else:
            try:
                x, y, k = pos
                round(k * len(self.draw_colour_grad))
                colour = self.draw_colour_grad[int(round(k * len(self.draw_colour_grad)))]

                self.disp.set_at((x,y), colour)
            except:
                pass

    def draw_pixels(self, poss, rot=None, auto_size=False):
        if auto_size:
            x = [i[0] for i in poss]
            self.rangex = min(x), max(x)
            y = [i[1] for i in poss]
            self.rangey = min(y), max(y)

        for pos in poss:
            self.draw_pixel(pos, rot)

    def transform_to_range(self, pos):
        x, y = pos[0], pos[1]
        x = x*(self.rangex[1]-self.rangex[0]) / self.resolution[0] + self.rangex[0]
        y = y*(self.rangey[1]-self.rangey[0]) / self.resolution[1] + self.rangey[0]
        return x, y

    def transform_to_disp(self, pos):
        #takes position in rangex, rangey and outputs position on size
        x, y = pos[0], pos[1]
        x = round((x - self.rangex[0])*self.resolution[0]/(self.rangex[1]-self.rangex[0]))
        y = round((y - self.rangey[0])*self.resolution[1]/(self.rangey[1]-self.rangey[0]))
        return int(x), int(y)

    def rotate(self, x, y, rot):
        x -= self.resolution[0]/2
        y -= self.resolution[1]/2
        
        newx = x * cos(rot) - y * sin(rot)
        newy = x * sin(rot) + y * cos(rot)
        
        newx += self.resolution[0]/2
        newy += self.resolution[1]/2
        return int(newx), int(newy)

    def show(self):
        dest = pg.display.set_mode(self.resolution)
        dest.blit(self.disp, (0,0))
        pg.display.flip()
        keepon = True
        while keepon:
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                keepon = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                      keepon = False

    def save(self, path):
        pg.image.save(self.disp, path)

    def draw_line(self, points, colour):
        p1 = self.transform_to_disp(points[0])
        p2 = self.transform_to_disp(points[1])
        pg.draw.line(self.disp, colour, p1, p2)



def draw_line(disp, oldx, oldy, x, y, color, rangex, rangey, size, aa=False, rot=None):
    oldx, oldy = transform_to_disp(oldx, oldy, rangex, rangey, size)
    x, y = transform_to_disp(x, y, rangex, rangey, size)
    if rot is not None:
        x, y = rotate(x, y, rot)
    if aa:
        draw.aaline(disp, color, (oldx, oldy), (x, y), True)
    else:
        draw.line(disp, color, (oldx, oldy), (x, y))
