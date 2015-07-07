'''
Created on Jul 7, 2015

@author: Mathieu Benoit (Mathieu.benoit@CERN.CH)
'''

from basil.HL.HardwareLayer import HardwareLayer



class CaribouI2C(HardwareLayer):
    '''
    Caribou's I2C interface to DAC,Current/Voltage Monitor,I2C expander
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        
        
        
class CaribouDAC7678(HardwareLayer):
    '''
    Caribou's 12-bit, Octal channel DAC
    '''

    def __init__(self, params):
        '''
        Constructor
        '''




class CaribouINA226(HardwareLayer):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''


class CaribouPCA9539(HardwareLayer):
    '''
    Caribou's I2C and SMBus I/O Expander
    '''

    def __init__(self, params):
        '''
        Constructor
        '''




class CaribouCard(CaribouI2C,CaribouDAC7678,CaribouINA226,CaribouPCA9539):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        
        Constructor
        '''
        