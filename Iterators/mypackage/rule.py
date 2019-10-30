import math
import numpy as np
import re
import random

# class Rule2:
#     def __init__(self, rule):
#         self.rule = rule

#     def set_variables(self, inputvars={}, **kwargs):
#         #concatenate the two lists
#         if kwargs == None:
#             kwargs = {}
#         kwargs.update(inputvars)

#         #set attributes on self
#         for key, value in kwargs.items():
#             setattr(self, key, value)

#     def iterate(self, **kwargs):
#         from math import cos, sin, exp, pi
#         #set vars if not done yet:
#         try:
#             self.set_variables(inputvars=kwargs)
#         except TypeError as e:
#             print(e)
#         #sets self.equations and self.rulevars
#         self.set_rule()
#         #execute equations
#         for eq in self.equations:
#             try:
#                 exec(eq)
#             except AttributeError as e:
#                 print(e)
#         return self.x, self.y
        
#     def set_standard(self):
#         self.set_rule()
#         for s in self.standard_sett:
#             exec(s)
            
#     def set_rule(self):
#         #set the variables to be used by rule

#         if self.rule == 1:
#             self.rulevars = ('x', 'y')
#             self.equations = ('self.x = self.x',
#                              'self.y = self.x*self.y*(1-self.y)')
#             self.standard_sett = ('self.rangex = (2.4, 4)',
#                                   'self.rangey = (0, 1)')
#             self.explanation = 'Standard bifurcation, logistic map.'
            
#         if self.rule == 2:
#             self.rulevars = ('x', 'y', 'u')
#             self.equations = ('self.t = 0.4 - 6/(1+self.x**2+self.y**2)',
#                              'self.x = 1+self.u*(self.x*cos(self.t)-self.y*(sin(self.t)))',
#                              'self.y = self.u*(self.x*sin(self.t)+self.y*(cos(self.t)))')
#             self.standard_sett = ('self.rangex = (-10, 10)',
#                                   'self.rangey = (-10, 10)',
#                                   'self.u = 0.85')
#             self.explanation = 'Ikeda map'
            
#         if self.rule == 3:
#             self.rulevars = ('x', 'y', 'a')
#             self.equations = ('self.x = self.x',
#                               'self.y = exp(-self.a*self.y**2)+self.x')
#             self.standard_sett = ('self.rangex = (-1, 1)',
#                                   'self.rangey = (-1, 1.5)',
#                                   'self.a = 6.2')
            
#         if self.rule == 4:
#             self.rulevars = ('x', 'y', 'k')
#             self.equations = ('self.oldx = self.x',
#                               'self.x = (self.oldx + self.y + self.k/(1)*sin(2*pi*self.x))%(1)',
#                               'self.y = (self.oldx - self.x)%(2*pi)')
#             self.standard_sett = ('self.rangex = (0, 1)',
#                                   'self.rangey = (0, 1)',
#                                   'self.k = 0.6')
            
#         if self.rule == 5:
#             self.rulevars = ('x', 'y', 'k')
#             self.equations = ('self.x = (self.x + self.k*sin(self.y))%(2*pi)',
#                               'self.y = (self.y + self.x)%(2*pi)')
#             self.standard_sett = ('self.rangex = (0, 2*pi)',
#                                   'self.rangey = (0, 2*pi)',
#                                   'self.k = 0.6')

#         if self.rule == 6:
#             self.rulevars = ('x', 'y', 'a', 'b', 'c', 'd')
#             self.equations = ('oldx = self.x',
#                               'self.x = self.x**2 - self.y**2 + self.a*self.x + self.b*self.y',
#                               'self.y = 2*oldx*self.y+self.c*self.x + self.d*self.y')
#             self.standard_sett = ('self.rangex = (-1.5, 0.5)',
#                                   'self.rangey = (-1.6, 0.6)',
#                                   'self.a = 0.9',
#                                   'self.b = -0.6013',
#                                   'self.c = 2.0',
#                                   'self.d = 0.5')
                                
# class ChaosGameRule(Rule2):
#     def __init__(self, verteces=None, **kwargs):
#         super().__init__(**kwargs)
#         self.verteces =  verteces

#     def set_rule(self):
#         from random import randrange
#         self.nextvert = self.verteces[randrange(0, len(self.verteces))]
#         self.rulevars = ('x', 'y', 'A', 'B')
#         self.equations = ('self.x = (self.nextvert[0] + self.x)/self.A',
#                           'self.y = (self.nextvert[1] + self.y)/self.B')
#         self.standard_sett = ('self.A = 0.5',
#                               'self.B = 0.5',)


class Rule3:
    def __init__(self, plot_on_screen=False, screen=None, **kwargs):
        self.plot_on_screen = plot_on_screen
        self.screen = screen
        self.vector_equations = None
        self.parse_list = [['math.cos', 'np.cos'],
                           ['math.sin', 'np.sin'],
                           ['pow', 'np.power']]
        self.set_rule()
        self.vectorize_equations()

        for key, value in kwargs.items():
            setattr(self, key, value)

        

    def vectorize_equations(self):
        if self.vector_equations == None:
            self.vector_equations = []
            for eq in self.equations:
                for p in self.parse_list:
                    eq = eq.replace(p[0], p[1])
                self.vector_equations.append(eq)

    def iterate(self, start_pos, iterations, iter_skip=0):
        self.x, self.y = start_pos
        
        pos = []
        for i in range(iterations):
            if type(self.equations) is str:
                exec(self.equations)
            else:
                for eq in self.equations:
                    exec(eq)
                
            if i > iter_skip:
                pos.append((self.x, self.y))

        if self.plot_on_screen:
            if self.screen is not None:
                for p in pos:
                    self.screen.draw_pixel(p)
            else:
                print('Error: please supply drawer.screen object.')
                return pos
        else:
            return pos

    def iterate_vector(self, start_pos_list, iterations, plot_on_screen=True, screen=None):
        self.x, self.y = np.array_split(start_pos_list, 2, axis=1)

        pos = np.array([[],])
        for i in range(iterations):
            for eq in self.vector_equations:
                exec(eq)
            np.append(pos, np.array([[self.x, self.y]]), axis=0)
        return pos

    def check_screen(self):
        if self.plot_on_screen:
            if self.screen is None:
                print('Error: to plot on screen, please supply drawer.screen object.')
                return


class GMAttractor(Rule3):
    def set_rule(self):
        self.vars = ['x', 'y', 'a', 'b']
        self.equations = ['self.t = self.x',
                          'self.x = self.b * self.y + self.w',
                          'self.w = self.a*self.x + (1-self.a)*2*self.x**2/(1+self.x**2)',
                          'self.y = self.w - self.t']

        self.vector_equations = []
        self.suggested_space = []
        self.explanation = 'Gumowski-Mira Attractor.'

        self.w = 0
        self.a, self.b = 2*random.rand()-1, 2*random.rand()-1


class HLAttractor(Rule3):
    def set_rule(self):
        self.vars = ['x', 'y', 'a', 'b', 'c']
        self.equations = ['self.nx = self.y - 1 - math.sqrt(abs(self.b*self.x-1-self.c))*math.copysign(1, self.x-1)',
                          'self.y = self.a - self.x - 1',
                          'self.x = self.nx']

        self.vector_equations = []
        self.suggested_space = []
        self.explanation = 'Hopalong Attractor.'

        self.a, self.b, self.c = random.random()*10, random.random()*10, random.random()*10
        self.w = 0
        # self.a, self.b = 2*random.rand()-1, 2*random.rand()-1


class Mandelbrot(Rule3):
    def __init__(self, rule_variant=0, **kwargs):
        self.epsilon = 10**-7
        self.max_iters = 400
        self.rule_variant = rule_variant
        super().__init__(**kwargs)

    def start(self):
        for i in range(self.screen.size[0]):
            print(f'Generating Mandelbrot plot. Current progress: {round(100 * i / self.screen.size[0])}%', end='\r')
            for j in range(self.screen.size[1]):
                self.z = complex(0,0)
                self.c = complex(*self.screen.transform_to_range((i,j)))
                k = 0
                delta = 2 * self.epsilon
                keep_going = True
                while delta > self.epsilon and k < self.max_iters and keep_going:
                    k += 1
                    try:
                        # new_z = (abs(self.z.real) + abs(self.z.imag))**2 + self.c
                        new_z = self.calc_next_z()
                        delta = abs(self.z - new_z)
                        self.z = new_z
                    except OverflowError:
                        keep_going = False
                

                if k < self.max_iters and keep_going:
                    self.screen.draw_pixel((i, j, k/self.max_iters), mandelbrot=True)
                    # self.screen.draw_pixel(self.screen.transform_to_range((i,j)))

    def calc_next_z(self):
        if self.rule_variant == 0:
            return self.z**2 + self.c
        if self.rule_variant == 1:
            return complex(abs(self.z.real), abs(self.z.imag))**2 + self.c

    def set_rule(self):
        self.vars = ['x', 'y', 'c', 'd']
        self.equations = []


class Julia(Mandelbrot):
    def __init__(self, c=complex(1,1), **kwargs):
        self.c = c
        super().__init__(**kwargs)

    def start(self):
        for i in range(self.screen.size[0]):
            print(f'Generating Julia plot. Current progress: {round(100 * i / self.screen.size[0])}%', end='\r')
            for j in range(self.screen.size[1]):
                self.z = complex(*self.screen.transform_to_range((i,j)))
                k = 0
                delta = 2 * self.epsilon
                keep_going = True
                while delta > self.epsilon and k < self.max_iters and keep_going:
                    k += 1
                    try:
                        # new_z = (abs(self.z.real) + abs(self.z.imag))**2 + self.c
                        new_z = self.calc_next_z()
                        delta = abs(self.z - new_z)
                        self.z = new_z
                    except OverflowError:
                        keep_going = False
                
                if k < self.max_iters and keep_going:
                    self.screen.draw_pixel((i, j, k/self.max_iters), mandelbrot=True)
                    # self.screen.draw_pixel(self.screen.transform_to_range((i,j)))


class Ikeda(Rule3):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_rule(self):
        self.vars = ['x', 'y', 'u']
        self.equations = ['self.t = 0.4 - 6 / (1 + pow(self.x,2) + pow(self.y,2))',
                          'self.x = 1 + self.u * (self.x*math.cos(self.t)-self.y*(math.sin(self.t)))',
                          'self.y = self.u*(self.x*math.sin(self.t)+self.y*(math.cos(self.t)))']

        self.vector_equations = ['self.t = 0.4 - 6 / (1 + np.square(self.x) + np.square(self.y))',
                                 'self.x = 1 + self.u * (self.x * np.cos(self.t) - self.y * np.sin(self.t))',
                                 'self.y = self.u * (self.x * np.sin(self.t) + self.y * np.cos(self.t))']
        self.suggested_space = ['rangex = (-10, 10)',
                                'rangey = (-10, 10)']
        self.explanation = 'Ikeda map, variable u. For u > 0.6 it has an attractor. Starting point may be anything.'

        self.u = 0.85


class ChaosGame(Rule3):
    def __init__(self, vertices=None, rule_variant=0, **kwargs):
        self.rule_variant = rule_variant
        self.vertices = vertices
        super().__init__(**kwargs)

    @property
    def rule_variant(self):
        return self._rule_variant

    @rule_variant.setter
    def rule_variant(self, val):
        self._rule_variant = val
        self.set_rule()
    
    def generate_vertices(self, nmbr_vertices, radius, rotation=None):
        if rotation == None:
            rotation = 0.5 * 360/nmbr_vertices
        vertices = []
        for i in range(nmbr_vertices):
            rotation += 360/(nmbr_vertices)
            vertices.append((math.cos(math.radians(rotation)) * radius, math.sin(math.radians(rotation)) * radius))

        self.vertices = vertices
        self.vert_history = [0,1,2,3,4]
        vertex_probs = np.random.rand(len(self.vertices))
        vertex_probs = vertex_probs / np.sum(vertex_probs)
        self.vertex_probs = vertex_probs.tolist()

        self.p1vert = self.vertices[0]
        self.p2vert = self.vertices[1]
        return vertices

    def draw_vertices(self, colour=(255,255,255)):
        colour = self.screen._draw_colour
        self.check_screen()
        for i in range(len(self.vertices)):
            self.screen.draw_line((self.vertices[i], self.vertices[(i+1)%len(self.vertices)]), colour)

    def choose_vertex(self):
        return random.choice(self.vertices)

    def add_vert_to_history(self):
        self.vert_history.append(self.nextvert)
        if len(self.vert_history) > 5:
            del(self.vert_history[0])

    def set_rule(self):
        if self.rule_variant == 0:
            self.vars = ['x', 'y', 'A', 'B']
            self.equations = ('self.nextvert = random.choice(self.vertices)',
                              'self.x = (self.nextvert[0] + self.x)*self.A',
                              'self.y = (self.nextvert[1] + self.y)*self.B')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where any vertex may be chosen. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 1:
            self.vars = ['x', 'y', 'A', 'B']
            self.nextvert = self.choose_vertex()
            self.equations = (
'''
nextnextvert = self.choose_vertex()
while self.nextvert == nextnextvert:
    nextnextvert = self.choose_vertex()
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where vertices may not be chosen two times in the row. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 2:
            self.vars = ['x', 'y', 'A', 'B']
            # self.vert_history.append(random.choice(self.vertices))
            self.nextvert = self.choose_vertex()
            self.equations = (
'''
a = self.vertices.index(self.nextvert)
nextnextvert = self.choose_vertex()
b = self.vertices.index(nextnextvert)
while (b - a)%(len(self.vertices)) == 2 or (a - b)%(len(self.vertices)) == 2:
    nextnextvert = self.choose_vertex()
    b = self.vertices.index(nextnextvert)
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where next vertex may not be two spaces away from last vertex. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 3:
            self.vars = ['x', 'y', 'A', 'B']
            # self.vert_history.append(random.choice(self.vertices))
            self.nextvert = self.choose_vertex()
            self.equations = (
'''
a = self.vertices.index(self.nextvert)
nextnextvert = self.choose_vertex()
b = self.vertices.index(nextnextvert)
while (a - b)%(len(self.vertices)) == 1:
    nextnextvert = self.choose_vertex()
    b = self.vertices.index(nextnextvert)
self.nextvert = nextnextvert
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B
''')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where next vertex may not be one space away (counter-clockwise) from last vertex. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 4:
            self.vars = ['x', 'y', 'A', 'B']
            self.equations = (
'''
self.nextvert = self.choose_vertex()
a = self.vertices.index(self.nextvert)
b = self.vertices.index(self.p1vert)
if self.p2vert == self.p1vert:
    while (b - a)%(len(self.vertices)) == 1 or (a - b)%(len(self.vertices)) == 1:
        self.nextvert = self.choose_vertex()
        a = self.vertices.index(self.nextvert)
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B

# print(self.vertices.index(self.nextvert), self.vertices.index(self.p1vert), self.vertices.index(self.p2vert))

self.p2vert = self.p1vert
self.p1vert = self.nextvert

''')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where next vertex may not be one space away from last vertex if last two chosen vertices are the same. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 5:
            self.vars = ['x', 'y', 'A', 'B']
            self.nextvert = self.choose_vertex()
            self.equations = ('j = random.choices(list(range(len(self.vertices))), weights=self.vertex_probs)[0]',
                              'self.nextvert = self.vertices[j]',
                              'self.x = (self.nextvert[0] + self.x)*self.A',
                              'self.y = (self.nextvert[1] + self.y)*self.B')
            self.add_vert_to_history()
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where the choice of the next vertex is weighted via self.vertex_probs. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5

        if self.rule_variant == 6:
            self.vars = ['x', 'y', 'A', 'B']
            self.nextvert = self.choose_vertex()
            self.equations = (
'''
self.nextvert = self.choose_vertex()
a = self.vertices.index(self.nextvert)
b = self.vertices.index(self.p1vert)
if self.p2vert == self.p1vert:
    while (b - a)%(len(self.vertices)) != 1 or (a - b)%(len(self.vertices)) != 1:
        self.nextvert = self.choose_vertex()
        a = self.vertices.index(self.nextvert)
self.x = (self.nextvert[0] + self.x)*self.A
self.y = (self.nextvert[1] + self.y)*self.B

# print(self.vertices.index(self.nextvert), self.vertices.index(self.p1vert), self.vertices.index(self.p2vert))

self.p2vert = self.p1vert
self.p1vert = self.nextvert

''')
            self.vector_equations = None
            self.suggested_space = None
            self.explanation = 'Rule variant on chaos game where next vertex may only be one space away from last vertex if last two chosen vertices are the same. Change position based on distance between current position and chosen vertex multiplied by factors A and B in x and y directions respectively.'
            self.A = 0.5
            self.B = 0.5



