
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
from package import *
from dPackage import *




# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)
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
    
    imagem = str(input("Qual a imagem a ser enviada?"))
    with open(imagem, "rb") as image:
        f = image.read()
        imgByte = bytearray(f)
#    numero = 47893273
#    txBuffer = numero.to_bytes(36,byteorder="big")
        
    pacote = package(imgByte)
    
    txBuffer = pacote.putInPackage()
    overhead = len(txBuffer)/len(imgByte)
    com.sendData(txBuffer)
        
 
    print("tentado transmitir .... {} bytes".format(len(txBuffer)))
    print("5")

     
    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
    
    
    dpackage = dPackage(com)
    
    rxConfirm = dpackage.dePackage()
    print("pastel",rxConfirm)
    nEOP = rxConfirm[1:5]
    print("aquilo",nEOP)
    nMessage = rxConfirm[0:1]
    print("isso",nMessage)
    if (nMessage == b'\x00' ):
        print("Funcionou! Index = {0}".format(int.from_bytes(nEOP, byteorder="big")))
    elif (nMessage == b'\x01'):
        print("EOP não encontrado!")
    elif (nMessage == b'\x11'):
        print("EOP no local errado!")
    else:
        print("Fudeu!")
        
        
        
  
    
    
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
    dt = fim - ini
    print("Overhead: {0}".format(overhead))
    print("ThroughPut: {0}".format(len(txBuffer)/dt))
#    print("Tempo de transmissão:" + str(txLen/t))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
