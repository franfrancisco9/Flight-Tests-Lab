import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from vincenty import vincenty
from tabulate import tabulate

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
         'NS_LAT':[4,'°'],'NS_LON':[5,'°'], 'NS_ALT':[6,'m'], 'NS_VE':[7,'ms^-1'], 'NS_VN':[8,'m*s^-1'], 'NS_VU':[9,'m*s^-1'], 
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
        if variable == self.v:
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

class Performance:
    # modes: name: [[HPE Limit, HPE percentil],[VPE limit, VPE percentil], [HAL limit, HAL percentil], [VAL limit, VAL percentil]]
    def __init__(self, data):
        self.data = data
    
    def limit_percentil(self, data1, data2, mode1, mode2):
        '''
        Returns True if the given the data1 and data2 values repects the percentil below the limit and modes to study
        '''
        results = []
        values = []
        for j in self.data:
            result = []
            value = []
            limit = self.data[j][mode1][0]
            percentil = self.data[j][mode1][1] 
            percentil_value = np.percentile(data1, percentil) 
            if percentil_value <= limit:
                result.append(True)
            else:
                result.append(False)
            value.append(percentil_value)
            
            limit = self.data[j][mode2][0]
            percentil = self.data[j][mode2][1] 
            percentil_value = np.percentile(data2, percentil)  
            if percentil_value <= limit:
                result.append(True)
            else:
                result.append(False)
            value.append(percentil_value)
            values.append(value)

            results.append(result)

        return results , values

    def generate_latex_tables_limit_percentil(self, accuracies, percentil_values,  mode1, mode2, name_table):
         with open("../results/B10/tables/" + name_table + "_table.tex", 'w') as f:
            rows = []
            row_header = ["Modos de Operação"]
            k = 0
            for j in self.data: 
                if k == 0:
                    row_header.append(mode1 + "(" + str(self.data[j][mode1][1]) + "%)")
                    row_header.append('Valor do percentil')
                    row_header.append(mode2 + "(" + str(self.data[j][mode2][1]) + "%)")
                    row_header.append('Valor do percentil')
                    rows.append(row_header)
                row = [j]
                for j in range(2):
                    row.append(accuracies[k][j])
                    row.append(percentil_values[k][j])
                k += 1
                rows.append(row)
            table = tabulate(rows, headers='firstrow', tablefmt='latex')
            f.write(table)

    def integrity_event(self, hpl, hpe, vpl, vpe):
        path = "../data/EV_2022.B10"        # path to file
        f = open(path, 'r').read().split('\n')
        integrity_events = []
        l = 0
        for i in hpl:
            if i < hpe[l]:
                integrity_events.append(f[l] + ';' + str(hpe[l]) + ';HPL<HPE')
            l += 1
        l = 0
        for i in vpl:
            if i < vpe[l]:
                integrity_events.append(f[l] + ';' + str(vpe[l]) + ';VPL<VPE')
            l += 1
        return integrity_events
    
    def generate_latex_tables_integrity_event(self, integrity_events):
         with open("../results/B10/tables/integrity_events_table.tex", 'w') as f:
            rows = []
            row_header = ["Evento de Integridade", 'RX_TOM', 'RX_WEEK', 'NSV_LOCK', 'NSV_USED', 'NS_LAT', 'NS_LON', 'NS_ALT', 'NS_VE', 'NS_VN', 'NS_VU', 'NS_HPL', 'NS_VPL', 'REF_LAT', 'REF_LON', 'REF_ALT', 'Erro', 'Diferença']
            for j in integrity_events: 
                row = ['Dados']
                for k in j.split(';'):
                    try:
                        row.append(round(float(k),2))
                    except:
                        row.append(k)

                rows.append(row)
            table = tabulate(rows, headers=row_header, tablefmt='latex')
            f.write(table)

    def availability(self, data1, data2, mode1, mode2):
        '''
        Returns percentage of availability for each mode
        '''
        availability = []
        assert len(data1) == len(data2)
        lenght = len(data1)
        for j in self.data:
            off = 0
            limit = [self.data[j][mode1][0], self.data[j][mode2][0]]
            for i in range(lenght):
                if data1[i] > limit[0] or data2[i] > limit[1]:
                    off += 1
            availability.append(str((lenght-off)/lenght*100)+'%')

        return availability

    def generate_latex_tables_availability(self, availability):
         with open("../results/B10/tables/availability_table.tex", 'w') as f:
            rows = []
            row_header = ["Disponibilidade (%)", 'Sim', 'Não']
            l = 0
            for j in self.data: 
                row = [j]
                k = availability[l]
                k = round(float(k.split('%')[0]),2)
                if k >= 99:
                    row.append(k)
                    row.append('X')
                    row.append(' ')
                else:
                    row.append(k)
                    row.append(' ')
                    row.append('X')
                l += 1
                rows.append(row)
            table = tabulate(rows, headers=row_header, tablefmt='latex')
            f.write(table)
    
    def generate_latex_tables_continuity(self, continuity):
         with open("../results/B10/tables/continuity_table.tex", 'w') as f:
            rows = []
            row_header = ["Continuidade ([0-1])"]
            l = 0
            for j in self.data: 
                row = [j]
                k = continuity[l]
                k = round(k,3)
                row.append(k)
                l += 1
                rows.append(row)
            table = tabulate(rows, headers=row_header, tablefmt='latex')
            f.write(table)




