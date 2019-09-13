# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:23:12 2019

@author: mihan
"""

class dPackage (object):
    
    def __init__(self, enlace):
        self.EOPStuff = bytes([0x00, 0xFF, 0x00, 0xFE, 0x00, 0xFD, 0x00, 0xFC])
        self.EOP = bytes([0xFF, 0xFE, 0xFD, 0xFC])
        self.com = enlace
        self.headerSize = 10
        self.EOPsize = 4
        
    def read(self):
        rxBuffer, nRx = self.com.getData(self.headerSize)
        print (rxBuffer)
        self.rxBufferint = int.from_bytes(rxBuffer, byteorder='big')
        print (self.rxBufferint)
        self.message, nRx = self.com.getData(self.rxBufferint + self.EOPsize)
        self.payload = self.message[ :self.rxBufferint]
        self.EOPindex = self.message.find(self.EOP)
        print (self.message)
#        self.recivedEOP = self.payload[rxBufferint-4, :]
        
    def checaErro(self):
        if self.EOPindex == -1:
            print("fudeu1")
        elif self.EOPindex != self.rxBufferint-self.EOPsize:
            print("fudeu2")
        
        
    def deStuff(self):
        self.payload = self.payload.replace(self.EOPStuff, self.EOP)
        
    def getPayload(self):
        return self.message
    
    def dePackage(self):
        self.read()
#        self.checaErro()
        self.deStuff()
        self.getPayload()
#        open("../camada/teste.png", 'wb').write(self.payload)
        return self.payload

        
        
        
    
        
        