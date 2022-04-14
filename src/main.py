import numpy as np
from a import A
from b import B, Performance
import matplotlib.pyplot as plt

def exercise_a():
    '''
    function that generates all the necessary results to answer exercise A
    '''
    accelerations = {'a1':A(1), 'a2':A(2), 'a3':A(3), 'a4':A(4)} 

    for i in accelerations:
        accelerations[i].graph()
        accelerations[i].single_sided_magnitude_spectrum()
        accelerations[i].generate_latex_tables_peaks(accelerations, int(i.split('a')[1]))

def exercise_b():
    '''
    function that generates all the necessary results to answer exercise b
    '''           
    errors = {'Error H':B('Error H'), 'Error V':B('Error V')}
    for i in errors:
        errors[i].graph(errors[i].error, i+"PE", '[m]')

    protection_limits = {'NS_HPL':B('NS_HPL'), 'NS_VPL':B('NS_VPL')}
    for i in protection_limits:
        protection_limits[i].graph()

    available_satelites = B('NSV_LOCK')
    used_satelites = B('NSV_USED')

    data_available = available_satelites.collect_data('NSV_LOCK')
    data_used = used_satelites.collect_data('NSV_USED')
    data_difference = [data_available[i]-data_used[i] for i in range((len(data_available)))]

    available_satelites.graph()
    used_satelites.graph()
    used_satelites.graph(data_difference, 'Satélites Restantes', '[nº satélites]')

    # Accuracy and Integrity
    # modes: name: [[HPE Limit, HPE percentil],[VPE limit, VPE percentil], [HAL limit, HAL percentil], [VAL limit, VAL percentil]]
    modes = {'APV-I':{'HPE':[16, 95],
                      'VPE':[20, 95],   
                      'HAL':[40, 99], 
                      'VAL':[50, 99]
                     },
             'APV-II':{'HPE':[16, 95],
                      'VPE':[8, 95],   
                      'HAL':[40, 99], 
                      'VAL':[20, 99]
                     },
             'CAT-I':{'HPE':[16, 95],
                      'VPE':[5, 95],   
                      'HAL':[40, 99], 
                      'VAL':[12, 99]
                     },
            }
    data = Performance(modes)
    accuracies = data.limit_percentil(errors['Error H'].error, errors['Error V'].error, 'HPE', 'VPE')
    data.generate_latex_tables_limit_percentil(accuracies, 'HPE', 'VPE', 'accuracy')

    integrities = data.limit_percentil(protection_limits['NS_HPL'].variable, protection_limits['NS_VPL'].variable, 'HAL', 'VAL')
    data.generate_latex_tables_limit_percentil(integrities, 'HAL', 'VAL', 'integrity')

    integrity_events = data.integrity_event(protection_limits['NS_HPL'].variable, errors['Error H'].error, protection_limits['NS_VPL'].variable, errors['Error V'].error)
    data.generate_latex_tables_integrity_event(integrity_events)

    availability = data.availability(protection_limits['NS_HPL'].variable, protection_limits['NS_VPL'].variable, 'HAL', 'VAL')
    data.generate_latex_tables_availability(availability)

    continuity = [round(float(i.split('%')[0])/100,3) for i in availability]
    data.generate_latex_tables_continuity(continuity)
    
def main():
    '''
    main function
    '''
    exercise_a()
    exercise_b()
    #plt.show()
    print("Ended Results")

if __name__ == '__main__':
    main()