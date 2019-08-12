# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:15:34 2019

@author: 55419
"""
with open("img.png", "rb") as image:
    f = image.read()
    txBuffer = bytearray(f)
        
    
    
    
txLen    = len(txBuffer)
txByte = txLen.to_bytes(10,byteorder="big")
print(txByte)

print(txLen)

txBufferPlus =  txByte + txBuffer

print(len(txBufferPlus))
    
#    print(txLen)