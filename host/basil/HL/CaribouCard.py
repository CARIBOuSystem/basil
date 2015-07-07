'''
Created on Jul 7, 2015

@author: Mathieu Benoit (Mathieu.benoit@CERN.CH)
'''

from basil.HL.HardwareLayer import HardwareLayer



class CaribouPowerRails(HardwareLayer):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        
        
        
class CaribouDAC(HardwareLayer):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''




class CaribouLDO(HardwareLayer):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''


class CaribouADC(HardwareLayer):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''






class CaribouCard(CaribouPowerRails,CaribouDAC,CaribouADC):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        