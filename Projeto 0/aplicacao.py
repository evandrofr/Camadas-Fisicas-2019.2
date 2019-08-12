
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



# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM7"                  # Windows(variacao de)
print("abriu com")

def main():
    #Inicio do clock
    ini = time.time()
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

   

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("gerando dados para transmissao :")
  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
    #exemplo 1
    #ListTxBuffer =list()
    #for x in range(1,10):
    #    ListTxBuffer.append(x)
    #txBuffer = bytes(ListTxBuffer)
    
    #Testando com imagem
    with open("img.png", "rb") as image:
        f = image.read()
        txBuffer = bytearray(f)
        
    
    #exemplo2
#    txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    
    
    txLen    = len(txBuffer)
    txByte = txLen.to_bytes(8,byteorder="big")
 
    print("tentado transmitir .... {} bytes".format(len(txByte)))
    com.sendData(txByte)
    rxBuffer, nRx = com.getData(8)
    if txByte == rxBuffer:
        com.sendData(txBuffer)
    
    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
         pass
    
#    rxConfirm, nConfirm = com.getData(txByteLen)
#    if nConfirm ==  txLen:   
#    
#        # Transmite dado
#        print("tentado transmitir .... {} bytes".format(txLen))
#        com.sendData(txBuffer)
#    
#       
#        
#        
#        # Atualiza dados da transmissão
#        txSize = com.tx.getStatus()
#        print ("Transmitido       {} bytes ".format(txSize))
#
#    # Faz a recepção dos dados
#    print ("Recebendo dados .... ")
#    rxBuffer, nRx = com.getData(txLen)
#    print ("Lido              {} bytes ".format(nRx))
    #repare que o tamanho da mensagem a ser lida é conhecida!     
#    rxBuffer, nRx = com.getData(txLen)
#    open("../Imagem/toad.png",'wb').write(rxBuffer)
    

    # log
#    print ("Lido              {} bytes ".format(nRx))
    
#    print (rxBuffer)
    
    
    
    #Fim do clock
    fim = time.time()
    
    print("Tempo de transmissão:" + str(fim - ini))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
