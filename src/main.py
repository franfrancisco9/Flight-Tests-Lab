import numpy as np
from a import A
from b import B
import matplotlib.pyplot as plt

def exercise_a():
    '''
    function that generates all the necessary results to answer exercise A
    '''
    accelerations = {'a1':A(1), 'a2':A(2), 'a3':A(3), 'a4':A(4)} 

    for i in range(4):
        accelerations['a'+str(i+1)].graph()
        accelerations['a'+str(i+1)].single_sided_magnitude_spectrum()
        accelerations['a'+str(i+1)].generate_latex_tables_peaks(accelerations, i)

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