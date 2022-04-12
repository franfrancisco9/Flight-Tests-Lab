import matplotlib.pyplot as plt

class A:
    '''
    Class to read data from EV_2022.A10 file
    '''
    def __init__(self, n, style = "" ):
        '''
        n is the number of the acceleration to study
        eg: a3, n = 3
        '''
        self.path = "../data/EV_2022.A10" # path to file
        self.t = self.collect_data(0) # collect time
        self.n = n
        self.a = self.collect_data(n) # collect acceleration values
        self.style = style            # style for the plots if none given reverts to classic
        

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
                    i = i[n].split('\n')[0]
                try:
                    i = float(i[n])
                    a.append(i)
                except:
                    continue
        return a
    
    def graph(self, t = []):
        '''
        Plot the graph for a given acceleration
        '''
        if t != []:
            a = []
            for i in range(len(t)):
                for j in range(len(self.t)):
                    if t[i] == self.t[j]:
                        a.append(self.a[j])
            self.t = t
            self.a = a

        plt.figure(self.n)
        plt.plot(self.t, self.a, self.style)
        plt.xlabel('t [s]') 
        # naming the y axis 
        plt.ylabel('a'+ str(self.n) +' [m/s^2]') 
        plt.autoscale() 
        plt.show()


if __name__ == '__main__':  
    a1 = A(1)
    a1.collect_data(1)
