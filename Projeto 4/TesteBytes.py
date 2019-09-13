# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:15:34 2019

@author: 55419
"""
import time
i = bytes([0xFF,0xFE,0xFD,0xFC,0xFF]) #b'0xFF 0xFE 0xFD 0xFC'
#print(len(i))
#print(type(i))
#i=i.replace(b'\xff',b'\x00\xff\x00\xfe')
#print(i)

EOP = bytes([0xFF,0xFE,0xFD,0xFC])
EOPStuff = bytes([0x00,0xFF,0x00,0xFE,0x00,0xFD,0x00,0xFC])
x = b''
print(len(x))
#
#i = 0
#start = time.time()
#while i<1000000:
#    i += 1
#    now = time.time()
#    dt = now - start
#    print("i",i)
#    print("dt",dt)
#    if dt > 1:
#        break    
        
#print(len('0'))
#g = iByte + j
#print(g)
#print(type(g))