import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin, asin, sqrt
from vincenty import vincenty

class B:
    '''
    Class to read data from EV_2022.B10 file
    Format: RX_TOM;RX_WEEK;NSV_LOCK;NSV_USED;NS_LAT;NS_LON;NS_ALT;NS_VE;NS_VN;NS_VU;NS_HPL;NS_VPL;REF_LAT;REF_LON;REF_ALT
    '''
    def __init__(self, v):
        '''
        n is the number of the acceleration to study
        eg: a3, n = 3
        '''
        self.list = {'RX_TOM':[0,'s'], 'RX_WEEK':[1,'nº semana gps'], 'NSV_LOCK':[2,'nº satélites'], 'NSV_USED':[3,'nº satélites'],
         'NS_LAT':[4,'°'],'NS_LON':[5,'°'], 'NS_ALT':[6,'m'], 'NS_VE':[7,'ms^-1'], 'NS_VN':[8,'ms^-1'], 'NS_VU':[9,'ms^-1'], 
         'NS_HPL':[10,'m'], 'NS_VPL':[11,'m'], 'REF_LAT':[12,'°'], 'REF_LON':[13,'°'], 'REF_ALT':[14,'m']}
        self.path = "../data/EV_2022.B10"        # path to file
        self.t = self.collect_data('RX_TOM')     # collect time
        self.v = v                               # variable to read, e.g:'RX_TOM'
        if 'Error' in self.v:
            self.error_type =self.v.split()[1]
            self.error = self.error_calculation()
        else:
            self.variable = self.collect_data(v)
        
    

    def collect_data(self, v):
        '''
        Collect the data from EV_2022.B10 file where
        n is the number of the acceleration. 
        eg: RX_TOM, v = 'RX_TOM'
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
        if variable == '':
            plt.ylabel(variable + ' [' + self.list[self.v][1] + ']') 
        else:
             plt.ylabel(variable + ' ' + units) 
        plt.autoscale() 
        plt.savefig("../results/B10/"+variable+".png")

    def error_calculation(self):
        error = []
        if self.error_type == "H":
            ns_lat = self.collect_data('NS_LAT')
            ns_lon = self.collect_data('NS_LON')
            ref_lat = self.collect_data('REF_LAT')
            ref_lon = self.collect_data('REF_LON')
            for i in range(len(ns_lat)):
                error.append(
                    vincenty(
                    (ns_lat[i],ns_lon[i]),
                    (ref_lat[i],ref_lon[i])
                    )*1000  #convert to meters
                )
        else:
            ns_alt = self.collect_data('NS_ALT')
            ref_alt = self.collect_data('REF_ALT')
            for i in range(len(ns_alt)):
                error.append(sqrt((ns_alt[i]-ref_alt[i])**2))

        return error

