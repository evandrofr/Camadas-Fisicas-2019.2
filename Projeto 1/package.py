# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:21:06 2019

@author: 55419
"""

class package(object):
    
    def __init__(self,message):
        self.message = message
        self.headerSize = 10
        self.EOP = bytes([0xFF,0xFE,0xFD,0xFC])
        self.EOPStuff = bytes([0x00,0xFF,0x00,0xFE,0x00,0xFD,0x00,0xFC])
        self.EOPSize = 4
        
    def byteStuffing(self):
        copy = self.message
        messageStuff = copy.replace(self.EOP,self.EOPStuff)
        return messageStuff
                
    def putHeader(self, messageStuff):
        messageLen = len(messageStuff)
        print(messageLen)
        header = messageLen.to_bytes(self.headerSize,byteorder="big")
        headerMessage = header + messageStuff
        return headerMessage
        
    def putEOP(self, headerMessage):
        headerMessageEOP = headerMessage + self.EOP
        return headerMessageEOP
    
    
        
    def getMessage(self, headerMessageEOP):
        return headerMessageEOP
    
    
        
    def putInPackage(self):
        messageStuff = self.byteStuffing()
        print("1")
        headerMessage = self.putHeader(messageStuff)
        print("2")
        headerMessageEOP = self.putEOP(headerMessage)
        print("3")
        x = self.getMessage(headerMessageEOP)
        print("4")
        return x
        
    