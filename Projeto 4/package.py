# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:21:06 2019

@author: 55419
"""

class package(object):
    
    def __init__(self,message):
        self.message = message
        self.EOP = bytes([0xFF,0xFE,0xFD,0xFC])
        self.EOPStuff = bytes([0x00,0xFF,0x00,0xFE,0x00,0xFD,0x00,0xFC])
        self.EOPSize = 4
        self.packSizeNumber = 2
        self.packNumberTotal = 4
        self.packNumberOrder = 4
        self.headerSize = self.packSizeNumber + self.packNumberTotal + self.packNumberOrder
        
    def byteStuffing(self):
        copy = self.message
        messageStuff = copy.replace(self.EOP,self.EOPStuff)
        return messageStuff
    
    #Fragmenta a mensagem  e devolve uma lista com os pedaços
    def fragmenta(self, messageStuff):
        packList = []
        copy = messageStuff
        size = len(messageStuff)
        packNumber = size // 128
        for n in range(0,packNumber):            
            pkg = copy[:128]
            packList.append(pkg)
            copy = copy[128:]
        packList.append(copy)
        packageNumberTotal = packNumber + 1              
        return packList, packageNumberTotal
        
                
    def putHeader(self, packList, server):
#        server = int(input("Para qual server devo enviar? (número pequeno)   "))
#        byteServer = server.to_bytes(1,byteorder="big")
        packListHeader = []
        i = 1
        packLen = len(packList)
        for messageStuff in packList:
            messageLen = len(messageStuff)
            header = i.to_bytes(self.packNumberOrder, byteorder="big")
            header = header + packLen.to_bytes(self.packNumberTotal, byteorder="big")
            header = header + messageLen.to_bytes(self.packSizeNumber,byteorder="big")
            header = server + header 
            headerMessage = header + messageStuff
            packListHeader.append(headerMessage)
            i += 1
        return packListHeader
        
    def putEOP(self, packListHeader):
        packListHeaderEOP = []
        for headerMessage in packListHeader:
            headerMessageEOP = headerMessage + self.EOP
            packListHeaderEOP.append(headerMessageEOP)
        return packListHeaderEOP
    
    #Pega uma mensagem com header e EOP e adiciona type em um byte na frente
    def putType(self,typeNumber, message):
        byteTypeNumber = typeNumber.to_bytes(1,byteorder="big")
        typeMessage = byteTypeNumber + message
        return typeMessage
        

    
    
        
#    def putInPackage(self):
#        messageStuff = self.byteStuffing()
#        print("1")
#        messageStuffPack = self.fragmenta(messageStuff)
#        print("2")
#        headerMessage = self.putHeader(messageStuffPack)
#        print("3")
#        headerMessageEOP = self.putEOP(headerMessage)
#        print("4")
#        typeHeaderMessageEOP = self.putType(headerMessageEOP, )
#        return typeHeaderMessageEOP
        
    