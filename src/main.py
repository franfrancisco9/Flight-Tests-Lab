import numpy as np
from a import A


def main():
    '''main function'''
    a1 = A(1)
    a2 = A(2)
    a3 = A(3)
    a4 = A(4)

    a1.graph()
    a1.single_sided_magnitude_spectrum()
    a2.graph()
    a2.single_sided_magnitude_spectrum()
    a3.graph()
    a3.single_sided_magnitude_spectrum()
    a4.graph()
    a4.single_sided_magnitude_spectrum()
    print(a4.peaksf)
    print(a4.peaksm)



if __name__ == '__main__':
    main()