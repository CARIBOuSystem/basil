'''
Created on Jul 7, 2015

@author: Mathieu Benoit (Mathieu.benoit@CERN.CH)
'''
import socket
import select
import struct
from array import array
from threading import Thread, Lock
from basil.TL.SiTransferLayer import SiTransferLayer




class CaribouTcp (SiTransferLayer):



    def __init__(self, conf):
        pass 
    
    
    
    def init(self, **kwargs):
        pass
    
    
    
    def write(self, addr, data):
        pass

    def read(self, addr, size):
        pass
