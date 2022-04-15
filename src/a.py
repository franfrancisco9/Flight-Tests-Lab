import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks as fp
from tabulate import tabulate

class A:
    '''
    Class to read data from EV_2022.A10 file
    Format: t;a1;a2;a3;a4
    '''
    def __init__(self, n):
        '''
        n is the number of the acceleration to study
        eg: a3, n = 3
        '''
        self.path = "../data/EV_2022.A10" # path to file
        self.t = self.collect_data(0) # collect time
        self.n = n
        self.a = self.collect_data(n) # collect acceleration values
        self.magn = 0
        self.feq = 0
        self.peaksf = np.array([])
        self.peaksm = np.array([])

    def collect_data(self, n):
        '''
        Collect the data from EV_2022.A10 file where
        n is the number of the acceleration. 
        eg: a3, n = 3
        '''
        a = []
        with open(self.path, 'r') as f:  
            for i in f:
                i = i.split(';')             # split the values by ';'
                if '\n' in i[n]:
                    i[n] = i[n].split('\n')[0]
                try:
                    i = float(i[n])
                    a.append(i)
                except:
                    continue
        return a
    
    def graph(self):
        '''
        Plot the graph for a given acceleration
        '''
        plt.figure("a"+str(self.n))
        plt.plot(self.t, self.a)
        plt.title("Variação temporal da aceleração " + str(self.n))
        plt.xlabel('t [s]') 
        plt.ylabel('a'+ str(self.n) +' [m*s^-2]') 
        plt.autoscale() 
        plt.savefig("../results/A10/a"+str(self.n)+".png")

    def single_sided_magnitude_spectrum(self):
        '''
        Plot the single-sided magnitude  spectrum for a given acceleration
        '''
        plt.figure("Espetro a"+str(self.n))
        out = plt.magnitude_spectrum(self.a)
        self.magn, self.freq = out[0], out[1]
        peaks, _ = fp(self.magn,height = 0.25)
        max_index = np.where(self.magn == np.amax(self.magn))
        if max_index not in peaks:
            peaks = np.append(max_index, peaks)
        self.peaksf, self.peaksm = self.freq[peaks], self.magn[peaks]

        plt.plot(self.freq, self.magn)
        plt.plot( self.peaksf, self.peaksm, "x")
        plt.title("Espetro unilateral de amplitude da aceleração " + str(self.n))
        plt.xlabel('Frequency [Hz]') 
        plt.ylabel('|a'+ str(self.n) +'(t)|') 
        plt.autoscale() 
        plt.savefig("../results/A10/espetro_a"+str(self.n)+".png")

    def get_results_peaks(self):
        return self.peaksf, self.peaksm

    def generate_latex_tables_peaks(self, accelerations, i):
         with open("../results/A10/tables/peaks_results_a"+str(i)+".tex", 'w') as f:
            rows = []
            row_header = ["Picos de a"+str(i)] 
            row_f = ["Frequência [Hz]"]
            row_m = ["Magnitude"]
            for j in range(len(accelerations['a'+str(i)].get_results_peaks()[0])):
                row_header.append("Pico " + str(j+1))
                row_f.append(accelerations['a'+str(i)].get_results_peaks()[0][j])
                row_m.append(accelerations['a'+str(i)].get_results_peaks()[1][j])
                
            rows = [row_header, row_f, row_m]
            table = tabulate(rows, headers='firstrow', tablefmt='latex')
            f.write(table)