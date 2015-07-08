'''
Created on Jul 7, 2015

@author: Mathieu Benoit (Mathieu.benoit@CERN.CH)
'''
import socket
import struct
from basil.TL.SiTransferLayer import SiTransferLayer


class CaribouTcp (SiTransferLayer):

    HOST = '192.168.0.10'  # The remote host
    PORT = 7  # The same port as used by the server
    XIIC_STOP = 0x00
    XIIC_REPEAT_START = 0x01


    def __init__(self, conf):
        self.CaribouSocket= None  
    
    def init(self, **kwargs):
        self.CaribouSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CaribouSocket.settimeout(15) # wait 15 seconds before forfeiting!
        
        print"Server is", self.HOST, "@ Port:", self.PORT
        print"Trying to connect server..."
        
        try :         
            self.CaribouSocket.connect((self.HOST, self.PORT))
        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc
            raise IOError('CaribouTcp:Connect - Cannot establish connection ')           
        print"Connection is established!"
       
    
    def write(self, addr, data):
        "TCP write, data should be a list"
        length = len(data)
        # print length
        fmt = "=%dL" % (3 + length)
        cmd = struct.pack(fmt, 0x02, addr, length, *data)
        # print repr (cmd)
        self.CaribouSocket.send(cmd)
        ack = self.CaribouSocket.recv(2)
        if ack=="OK" : 
            pass
        else:
            raise IOError('CaribouTcp:read - something is wrong, ack not OK')           
 


    def read(self, addr, size):
        cmd = struct.pack("=3L", 0x01, addr, size)
        # print repr (cmd)
        self.CaribouSocket.send(cmd)
        recvbuf = self.CaribouSocket.recv(size * 4)  # Now can only receive one u32 data
        fmt = "=%dL" % size
        recvdat = struct.unpack(fmt, recvbuf)
        return list(recvdat)
        # returned data is tuple
        

    def i2c_read(self,addr, reg_addr, length):
        self.i2c_write(addr, [reg_addr], "repeat")
        # wait(30)
        cmd = struct.pack("=3L", 0x07, addr, length)
        # print repr (cmd)
        self.CaribouSocket.send(cmd)
        recvbuf = self.CaribouSocket.recv(length)  # Now can only receive one u32 data
        fmt = "=%dB" % length
        # print fmt
        recvdat = struct.unpack(fmt, recvbuf)
    
        return list(recvdat)
        # returned data is a list
    
    
    def i2c_write(self,addr, data, stop_sel):
    
        stop_sel_i = stop_sel.upper()
        if stop_sel_i == "STOP":
            iic_stop_i = self.XIIC_STOP
        elif stop_sel_i == "REPEAT":
            iic_stop_i = self.XIIC_REPEAT_START
        else:
            print "stop selection error!"
    
        "TCP write, data should be a list"
        length = len(data)
        # print length
        fmt = "=%dL" % (4 + length)
        cmd = struct.pack(fmt, 0x06, addr, length, iic_stop_i, *data)
        # print repr (cmd)
        self.CaribouSocket.send(cmd)
        ack = self.CaribouSocket.recv(2)
        if ack=="OK" : 
            pass
        else:
            raise IOError('CaribouTcp:write - something is wrong, ack not OK')           
        
        
        
        
        
