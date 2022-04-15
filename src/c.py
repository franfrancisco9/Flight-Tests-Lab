import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from vincenty import vincenty
from tabulate import tabulate

class C:
    '''
    Class to read data from EV_2022.C10 file
    Format: t;EAS;QNE;a_z;N2_rh;FF_rh;EGT_rh;N2_lt;FF_lt;EGT_lt
    '''
    def __init__(self, v):
        '''
        n is the number of the acceleration to study
        eg: a3, n = 3
        '''
        self.list = {'t':[0,'s'], 'EAS':[1,'kn'], 'QNE':[2,'ft'], 'a_z':[3,'m*s^-2'],
                     'N2_rh':[4,'% nominal'], 'FF_rh':[5,'lb*hora^-1'], 'EGT_rh':[6,'K'], 
                     'N2_lt':[7,'% nominal'], 'FF_lt':[8,'lb*hora^-1'], 'EGT_lt':[9,'K']
                    }
        self.path = "../data/EV_2022.C10"        # path to file
        self.t = self.collect_data('t')          # collect time
        self.v = v                               # variable to read, e.g:'t'
        self.variable = self.collect_data(v)
        
    

    def collect_data(self, v):
        '''
        Collect the data from EV_2022.C10 file where
        n is the number of the acceleration. 
        eg: t, v = 't'
        '''
        variable = []
        n = self.list[v][0]
        with open(self.path, 'r') as f:  
            for i in f:
                i = i.split(';')             # split the values by ';'
                if '\n' in i[n]:
                    i[n] = i[n].split('\n')[0]
                try:
                    i = float(i[n])
                    variable.append(i)
                except:
                    continue                                 
        return variable
    
    def graph(self, values = [], variable = '', units = ''):
        '''
        Plot the graph for a given acceleration
        '''
        if values == []:
            values = self.variable
        if variable == '':
            variable = self.v

        plt.figure(variable)
        plt.plot(self.t, values)
        plt.title("Variação temporal da variável " + variable)
        plt.xlabel('t [s]') 
        if variable == self.v:
            plt.ylabel(variable + ' [' + self.list[self.v][1] + ']') 
        else:
             plt.ylabel(variable + ' ' + units) 
        plt.autoscale() 
        plt.savefig("../results/C10/"+variable+".png")