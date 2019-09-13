# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:29:37 2019

@author: mihan
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time
from dPackage import *
from package import *


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)
print("abriu com")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    com.fisica.flush()
    dpackage = dPackage(com)
    pacote = package(b'/x00')
    
    server = 1
    serverByte = server.to_bytes (1, byteorder = "big")
    arquivo = open('InfoRecebe.txt', 'a')
   

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    ocioso = True
    
    while ocioso:
        time.sleep(0.1)
        message1, size = com.getData(12)
        if len(message1)>0:
            serverNumber, typeNumber, packNumber, packNumberTotal, rxBufferSize = dpackage.readHeader(message1)
            lixo, lixoSize = com.getData(rxBufferSize+4)
            if (serverNumber == 1) and (typeNumber == 1):
                ocioso = False
                arquivo.write("Msg: 1 – recebida: " + str(time.ctime(int(time.time()))) + "– destinatário: 2 \n")
                print ("recebeu mensagaem tipo 1")
        
    time.sleep(0.2)
    msg2 = pacote.packUniMessage(server, packNumber, packNumberTotal, 0)
    txBuffer = msg2
    txBuffered = pacote.putType(2,txBuffer)
    com.sendData(txBuffered)
    time.sleep(1)
    arquivo.write("Msg: 2 – enviada: "+ str(time.ctime(int(time.time()))) +" – destinatário: 2 \n")
    print("mandou mensagem tipo 2")
    com.fisica.flush()
    
    start=time.time()
    start1=time.time()
    cont = 1
    concat=[]
    while cont <= packNumberTotal:
        com.fisica.flush()
        com.rx.clearBuffer()
        msg3, size = com.getData(12)
        if len(msg3)>=1:
            serverNumber, typeNumber, packNumber, packNumberTotal, rxBufferSize = dpackage.readHeader(msg3)
            msg3pay, size = com.getData(rxBufferSize+4)
            payload, eop =dpackage.readPayload(msg3pay, rxBufferSize)
            erro = dpackage.checaErro(msg3pay,eop,rxBufferSize)[0]
            time.sleep(0.4)
            print (msg3)
            arquivo.write("Msg: 3 – recebida: "+ str(time.ctime(int(time.time()))) +"– destinatário: 2 \n")
            if (typeNumber == 3) and (packNumber == cont) and (erro == 0) and len(payload)>0:
                msg4=pacote.packUniMessage(server, packNumber, packNumberTotal, 0)
                txBuffer = msg4
                txBuffer = pacote.putType(4,txBuffer)
                com.sendData(txBuffer)
                concat.append(payload)
                start=time.time()
                arquivo.write("Msg: 4 – enviada:"+ str(time.ctime(int(time.time()))) +"– destinatário: 2 \n")
                print("enviou confirmação pacote ", cont, "de", packNumberTotal)
                cont +=1
                print (msg3)
            elif len(payload)>0 and len(msg3)>0:
                msg6=pacote.packUniMessage(server, packNumber, packNumberTotal, 0)
                txBuffer = msg6
                txBuffer = pacote.putType(6,txBuffer)
                arquivo.write("Msg: 6 – enviada: "+ str(time.ctime(int(time.time()))) + "– destinatário: 2 \n")
                print("enviou erro pacote ", cont, "de", packNumberTotal)
                com.sendData(txBuffer)
                print (msg3)
            end=time.time()
            delta=end-start
            if delta>21:
                msg5=pacote.packUniMessage(server, packNumber, packNumberTotal, 0)
                txBuffer = msg5
                txBuffer = pacote.putType(5,txBuffer)
                com.sendData(txBuffer)
                arquivo.write("Msg: 5 – enviada: "+ str(time.ctime(int(time.time()))) + "– destinatário: 2 \n")
                print ("TIME OUT")
                break
        else:
            time.sleep(1)
            msg4=pacote.packUniMessage(server, packNumber, packNumberTotal, 0)
            txBuffer = msg4
            txBuffer = pacote.putType(4,txBuffer)
            com.sendData(txBuffer)
            arquivo.write("Msg: 4 – enviada:"+ str(time.ctime(int(time.time()))) +"– destinatário: 2 \n")
            continue
    real=b''.join(concat)
    arquivo.close()
    open("../camada/toad.png", 'wb').write(real)
    print ("recebido!")
    
       
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
