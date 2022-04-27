import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from tabulate import tabulate
from scipy.signal import argrelextrema

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
    
    def graph(self, values = [], variable = '', units = '', time = []):
        '''
        Plot the graph for a given acceleration
        '''
        if values == []:
            values = self.variable
        if variable == '':
            variable = self.v

        plt.figure(variable)
        if time != []:
            plt.scatter(self.t, values, s = 5)
        else:
            plt.plot(self.t, values)
        plt.title("Variação temporal da variável " + variable)
        plt.xlabel('t [s]') 
        if variable == self.v:
            plt.ylabel(variable + ' [' + self.list[self.v][1] + ']') 
        else:
            if time != []:
                plt.ylabel(units)
            else:
                plt.ylabel(variable + ' ' + units) 
        plt.autoscale() 
        plt.savefig("../results/C10/"+variable+".png")

    def acceleration_converter(self):
        g0 = 9.80665 # m*s^-2
        acceleration = self.collect_data('a_z')
        for i in range(len(acceleration)):
            acceleration[i] = round(acceleration[i]/g0, 3)

        return acceleration

    def local_extremes(self, acceleration):
        '''
        Write in a file only local max and min for a_z measured in g's, format: t, a_z(g)\n
        '''
        acceleration = np.array(acceleration)
        with open("../results/C10/local_extreme.txt", 'w') as f:
            indicex_max = argrelextrema(acceleration, np.greater)
            indices_min = argrelextrema(acceleration, np.less)
            indices = np.sort(np.append(indices_min[0],indicex_max[0]))
            self.t =  np.array(self.t)
            self.t = self.t[indices]
            acceleration = acceleration[indices]
            if acceleration[1] > acceleration[0]:
                tipo = ['vale', 'pico']
            else:
                tipo = ['pico', 'vale']
            self.graph(acceleration, 'Extremos locais aceleração (picos e vales)', 'a_z [g]', ['change'])
            j = 1
            for i in range(len(acceleration)):
                #line = str(self.t[i]) + ';' + str(acceleration[i])  + ';' + str(tipo[i % 2]) + '\t\t' + '| '
                #if j % 4 == 0: # used to generate file for latex 
                line = str(self.t[i]) + ';' + str(acceleration[i])  + ';' + str(tipo[i % 2]) + '\n' 
                f.write(line)
                j += 1

    def occurence_counter(self, n1, n2, file = []):
        '''
        Counter the number of occurences of the given n values
        '''
        if file == []:
            acceleration = self.acceleration_converter()
        else:
            acceleration = file
        occurrences = 0
        flag = 0
        #print("PAIR:",n1,'---',n2)
        if n1 > 1:
            for i in range(len(acceleration)):
                if acceleration[i] > n1 and flag == 0:
                    flag = 1
                    #print(acceleration[i], '>', n1)
                elif acceleration[i] < n2 and flag == 1:
                    occurrences += 1
                    flag = 0
                    #print(acceleration[i], '<', n2)
        elif n1 < 1:
            for i in range(len(acceleration)):
                if acceleration[i] < n1 and flag == 0:
                    flag = 1
                    #print(acceleration[i], '<', n1)
                elif acceleration[i] > n2 and flag == 1:
                    occurrences += 1
                    flag = 0
                    #print(acceleration[i], '>', n2)
        
        return occurrences

    def occurence_counter_file(self, n1, n2):
        '''
        return the occurence counter of a file 
        '''
        with open("../results/C10/local_extreme.txt", 'r') as f:
            accelerations = []
            for line in f:
                accelerations.append(float(line.split(';')[1]))
        occurrences = self.occurence_counter(n1, n2, accelerations)
        return occurrences
    

    def save_occurence(self, occurrences, name, pairs):
        '''
        save the data of occurence_counter into a file 
        '''
        with open("../results/C10/" + name + ".txt", 'w') as f:
            for i in range(len(occurrences)):
                f.write('N_1 = ' + str(pairs[i][0]) + ' g e N_2 = ' + str(pairs[i][1]) + ' g ---> ' + str(occurrences[i]) + ' ocorrências' + '\n')
