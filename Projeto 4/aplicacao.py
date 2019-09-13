
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
serialName = "COM7"                  # Windows(variacao de)
print("abriu com")

def main():
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
    server = int(input("Para qual server devo enviar? (número pequeno)   "))
    byteServer = server.to_bytes(1,byteorder="big")
    
    arquivo = open('InfoEnvio.txt', 'a')
    #Inicio do clock
    
    
    with open(imagem, "rb") as image:
        f = image.read()
        imgByte = bytearray(f)

        
    pacote = package(imgByte)
    
#    txBuffer = pacote.putInPackage()
    pacoteStuff = pacote.byteStuffing()
    packList, packageNumberTotal = pacote.fragmenta(pacoteStuff)
    packList = pacote.putHeader(packList, byteServer)
    packList = pacote.putEOP(packList)
    txBuffer = packList
    txBufferType = []
    for msg in txBuffer:
        msg3 = pacote.putType(3, msg)
        txBufferType.append(msg3)
        

    
    print("Arquivo empacotado...")    
    
    
    overhead = len(b''.join(txBuffer))/len(imgByte)
    
    NumberTotalByte = packageNumberTotal.to_bytes(4,byteorder="big")
    
    pacote1 = package(NumberTotalByte)
    pacote1Stuff = pacote1.byteStuffing()
    packList1, packageNumberTotal1 = pacote.fragmenta(pacote1Stuff)
    packList2 = pacote1.putHeader(packList1, byteServer)
    packList3 = pacote1.putEOP(packList2)
    mensagem1 = packList3[0]
    mensagem1Type = pacote1.putType(1,mensagem1)
    
    ini = time.time()
    recivedType2 = False
    while not recivedType2:
        com.sendData(mensagem1Type)
        print("Permissão enviada...: ")
        arquivo.write("Msg: 1 – enviada: {0} – destinatário: {1}\n".format(time.ctime(int(time.time())),server))
        time.sleep(0.4)
        headerMensagem2, headerMensagem2Size = com.getData(12)
        if (len(headerMensagem2)>0):
            print("Header recebido!")
            if (headerMensagem2[0] == 2):
                recivedType2 = True
                lixo, lenLixo = com.getData(int.from_bytes(headerMensagem2[10:12], byteorder="big")+4)
                print("Permissão concedida!")
                arquivo.write("Msg: 2 – Recebido: {0} – destinatário: {1}\n".format(time.ctime(int(time.time())),1))
        
    byteSize = headerMensagem2[10:12]
    size = int.from_bytes(byteSize, byteorder="big")
    mensagem2, mensagem2Size = com.getData(size+4)
    
    cont = 1
    timeStart = time.time()
    while cont <= packageNumberTotal:
        com.rx.clearBuffer()
        com.sendData(txBufferType[cont-1])
        print("Enviando Pacote {0} de {1}...".format(cont,packageNumberTotal))
        arquivo.write("Enviando Pacote {0} de {1}...\n".format(cont,packageNumberTotal))
        arquivo.write("Msg: 3 – enviada: {0} – destinatário: {1}\n".format(time.ctime(int(time.time())),1))
        time.sleep(0.1)
        recived4, recived4Len = com.getData(12)
        if len(recived4)>0:
            lixo2, lenLixo2 = com.getData(int.from_bytes(recived4[10:12], byteorder="big")+4)
            if (recived4[0] == 4) and (int.from_bytes(recived4[2:6], byteorder="big") == cont):
                print("Pacote {0} de confirmação recebida!".format(cont))
                arquivo.write("Pacote {0} de confirmação recebida!\n".format(cont))
                arquivo.write("Msg: 4 – Recebido: {0} – destinatário: {1}".format(time.ctime(int(time.time())),1))
                cont += 1
                timeStart = time.time()
            elif (recived4[0] == 4) and (int.from_bytes(recived4[2:6], byteorder="big") != cont):
                print("Pacote {0} de confirmação NÃO recebida!".format(cont))
                arquivo.write("Pacote {0} de confirmação NÃO recebida!\n".format(cont))
                print("Novo pacote a REenviar: {0}".format(int.from_bytes(recived4[2:6], byteorder="big")))
                arquivo.write("Novo pacote a reenviar: {0} \n".format(int.from_bytes(recived4[2:6], byteorder="big")))
                cont = int.from_bytes(recived4[2:6], byteorder="big")+1
                
            elif (recived4[0] == 6):    
                print("Erro no envio do pacote {0}.".format(int.from_bytes(recived4[2:6], byteorder="big")))
                arquivo.write("Erro no envio do pacote {0}.\n".format(int.from_bytes(recived4[2:6], byteorder="big")))
                arquivo.write("Msg: 6 – Recebida: {0} – destinatário: {1}".format(time.ctime(int(time.time())),1))
                cont = int.from_bytes(recived4[2:6], byteorder="big")+1
    #            timeStart = time.time()
            
        timeEnd = time.time()
        deltat = timeEnd - timeStart
        if deltat > 21:
            print("Timeout! Envio cancelado!")
            arquivo.write("Timeout! Envio cancelado!\n")
            msg5 = pacote.putType(5, txBuffer[cont-1])
            com.sendData(msg5)
            break
        
 
    
    print("Envio FINALIZADO!!!! NÃO QUER QUISER QUE FOI BEM SUCEDIDO!!")

     
    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
    
    
    
    #Fim do clock
    fim = time.time()
    dt = fim - ini
    print("Overhead: {0}".format(overhead))
    print("ThroughPut: {0}".format(len(imgByte)/dt))
    arquivo.write("ThroughPut: {0} \n".format(len(imgByte)/dt))
#    print("Tempo de transmissão:" + str(txLen/t))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    arquivo.close()
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
