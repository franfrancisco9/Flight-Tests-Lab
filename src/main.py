import numpy as np
from a import A
from b import B
from tabulate import *
import matplotlib.pyplot as plt

def exercise_a():
    '''
    function that generates all the necessary results to answer exercise A
    '''
    accelerations = {'a1':A(1), 'a2':A(2), 'a3':A(3), 'a4':A(4)} 

    # acceleration 1 results:
    accelerations['a1'].graph()
    accelerations['a1'].single_sided_magnitude_spectrum()
    a1peaksf, a1peaksm = accelerations['a1'].get_results_peaks()

    # acceleration 2 results:
    accelerations['a2'].graph()
    accelerations['a2'].single_sided_magnitude_spectrum()
    a2peaksf, a2peaksm = accelerations['a2'].get_results_peaks()

    # acceleration 3 results:
    accelerations['a3'].graph()
    accelerations['a3'].single_sided_magnitude_spectrum()
    a3peaksf, a3peaksm = accelerations['a3'].get_results_peaks()

    # acceleration 4 results:
    accelerations['a4'].graph()
    accelerations['a4'].single_sided_magnitude_spectrum()
    a4peaksf, a4peaksm = accelerations['a4'].get_results_peaks()

    for i in range(4):
        with open("../results/A10/peaks_results_a"+str(i)+".tex", 'w') as f:
            rows = []
            row_header = ["Picos de a"+str(i+1)] 
            row_f = ["Frequência [Hz]"]
            row_m = ["Magnitude"]
            for j in range(len(accelerations['a'+str(i+1)].get_results_peaks()[0])):
                row_header.append("Pico " + str(j))
                row_f.append(accelerations['a'+str(i+1)].get_results_peaks()[0][j])
                row_m.append(accelerations['a'+str(i+1)].get_results_peaks()[1][j])
                
            rows = [row_header, row_f, row_m]
            table = tabulate(rows, headers='firstrow', tablefmt='latex')
            f.write(table)

def exercise_b():
    '''
    function that generates all the necessary results to answer exercise b
    '''           
    
    hpe = B('Error H')
    error_hpe = hpe.error
    hpe.graph(error_hpe, "HPE", '[m]')

    vpe = B('Error V')
    error_vpe = vpe.error
    vpe.graph(error_vpe, "VPE", '[m]')

def main():
    '''
    main function
    '''
    exercise_a()
    exercise_b()
    plt.show()
    print("Ended Results")

if __name__ == '__main__':
    main()