import math
import numpy as np
import re

class Rule2:
    def __init__(self, rule):
        self.rule = rule

    def set_variables(self, inputvars={}, **kwargs):
        #concatenate the two lists
        if kwargs == None:
            kwargs = {}
        kwargs.update(inputvars)

        #set attributes on self
        for key, value in kwargs.items():
            setattr(self, key, value)

    def iterate(self, **kwargs):
        from math import cos, sin, exp, pi
        #set vars if not done yet:
        try:
            self.set_variables(inputvars=kwargs)
        except TypeError as e:
            print(e)
        #sets self.equations and self.rulevars
        self.set_rule()
        #execute equations
        for eq in self.equations:
            try:
                exec(eq)
            except AttributeError as e:
                print(e)
        return self.x, self.y
        
    def set_standard(self):
        self.set_rule()
        for s in self.standard_sett:
            exec(s)
            
    def set_rule(self):
        #set the variables to be used by rule

        if self.rule == 1:
            self.rulevars = ('x', 'y')
            self.equations = ('self.x = self.x',
                             'self.y = self.x*self.y*(1-self.y)')
            self.standard_sett = ('self.rangex = (2.4, 4)',
                                  'self.rangey = (0, 1)')
            self.explanation = 'Standard bifurcation, logistic map.'
            
        if self.rule == 2:
            self.rulevars = ('x', 'y', 'u')
            self.equations = ('self.t = 0.4 - 6/(1+self.x**2+self.y**2)',
                             'self.x = 1+self.u*(self.x*cos(self.t)-self.y*(sin(self.t)))',
                             'self.y = self.u*(self.x*sin(self.t)+self.y*(cos(self.t)))')
            self.standard_sett = ('self.rangex = (-10, 10)',
                                  'self.rangey = (-10, 10)',
                                  'self.u = 0.85')
            self.explanation = 'Ikeda map'
            
        if self.rule == 3:
            self.rulevars = ('x', 'y', 'a')
            self.equations = ('self.x = self.x',
                              'self.y = exp(-self.a*self.y**2)+self.x')
            self.standard_sett = ('self.rangex = (-1, 1)',
                                  'self.rangey = (-1, 1.5)',
                                  'self.a = 6.2')
            
        if self.rule == 4:
            self.rulevars = ('x', 'y', 'k')
            self.equations = ('self.oldx = self.x',
                              'self.x = (self.oldx + self.y + self.k/(1)*sin(2*pi*self.x))%(1)',
                              'self.y = (self.oldx - self.x)%(2*pi)')
            self.standard_sett = ('self.rangex = (0, 1)',
                                  'self.rangey = (0, 1)',
                                  'self.k = 0.6')
            
        if self.rule == 5:
            self.rulevars = ('x', 'y', 'k')
            self.equations = ('self.x = (self.x + self.k*sin(self.y))%(2*pi)',
                              'self.y = (self.y + self.x)%(2*pi)')
            self.standard_sett = ('self.rangex = (0, 2*pi)',
                                  'self.rangey = (0, 2*pi)',
                                  'self.k = 0.6')

        if self.rule == 6:
            self.rulevars = ('x', 'y', 'a', 'b', 'c', 'd')
            self.equations = ('oldx = self.x',
                              'self.x = self.x**2 - self.y**2 + self.a*self.x + self.b*self.y',
                              'self.y = 2*oldx*self.y+self.c*self.x + self.d*self.y')
            self.standard_sett = ('self.rangex = (-1.5, 0.5)',
                                  'self.rangey = (-1.6, 0.6)',
                                  'self.a = 0.9',
                                  'self.b = -0.6013',
                                  'self.c = 2.0',
                                  'self.d = 0.5')
                                
class ChaosGameRule(Rule2):
    def __init__(self, verteces=None, **kwargs):
        super().__init__(**kwargs)
        self.verteces =  verteces

    def set_rule(self):
        from random import randrange
        self.nextvert = self.verteces[randrange(0, len(self.verteces))]
        self.rulevars = ('x', 'y', 'A', 'B')
        self.equations = ('self.x = (self.nextvert[0] + self.x)/self.A',
                          'self.y = (self.nextvert[1] + self.y)/self.B')
        self.standard_sett = ('self.A = 0.5',
                              'self.B = 0.5',)


class Rule3:
    def __init__(self, **kwargs):
        self.vector_equations = None
        self.set_rule()
        self.vectorize_equations()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.parse_list = [['math.cos', 'np.cos'],
                           ['math.sin', 'np.sin'],
                           ['pow', 'np.power']]

    def vectorize_equations(self):
        if self.vector_equations == None:
            self.vector_equations = []
            for eq in self.equations:
                for p in self.parse_list:
                    eq = eq.replace(p[0], p[1])
                self.vector_equations.append(eq)

    def iterate(self, start_pos, iterations):
        self.x, self.y = start_pos
        
        pos = []
        for i in range(iterations):
            for eq in self.equations:
                exec(eq)
            pos.append((self.x, self.y))
        return pos

    def iterate_vector(self, start_pos_list, iterations):
        self.x, self.y = np.array_split(start_pos_list, 2, axis=1)

        pos = np.array([[],])
        for i in range(iterations):
            for eq in self.vector_equations:
                exec(eq)
            np.append(pos, np.array([[self.x, self.y]]), axis=0)
        return pos



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