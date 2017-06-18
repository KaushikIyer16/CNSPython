import socket
import Crypto
import Crypto.Cipher.AES as aes
import pickle
from Crypto.PublicKey import DSA
from Crypto.Random import random
import psutil
import os
import blowfish as bf
import serpent as sp

socketDict = {
              'DSASocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'AESSocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'RSASocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'SerpentSocket'   : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'BlowfishSocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM)
              }

bindConfig = {
                'DSAConfig' : (socket.gethostname() , 9001),
                'AESConfig' : (socket.gethostname() , 9002),
                'RSAConfig' : (socket.gethostname() , 9003),
                'BlowfishConfig' : (socket.gethostname() , 9004),
                'SerpentConfig' : (socket.gethostname(),9005)
            }
socketConfig = {
                    'DSASocket' : 'DSAConfig',
                    'AESSocket' : 'AESConfig',
                    'RSASocket' : 'RSAConfig',
                    'BlowfishSocket' : 'BlowfishConfig',
                    'SerpentSocket'  : 'SerpentConfig'
            }

def aesEncryption(PUBLIC_KEY):
    encryption = aes.AESCipher(PUBLIC_KEY)

    socketDict['AESSocket'].listen(5)
    while True:
        clientSocket,clientAddress = socketDict['AESSocket'].accept()
        # print 'the client address is ',clientAddress
        clientSocket.send(encryption.encrypt("this ralloc project is a piece of trash & a pain"))
        printStatistics()
        # print "after statistics"
        socketDict['AESSocket'].close()
        break;

def blowfishEncryption(PUBLIC_KEY):
    socketDict['BlowfishSocket'].listen(5)

    while True:
        clientSocket,clientAddress = socketDict['BlowfishSocket'].accept()

        clientSocket.send(bf.cryptBlowfish(PUBLIC_KEY,"this ralloc project is a piece of trash & a pain"))
        printStatistics()

        socketDict['BlowfishSocket'].close()
        break;

def serpentEncryption(PUBLIC_KEY):
    socketDict['SerpentSocket'].listen(5)
    encryption = sp.Serpent(PUBLIC_KEY)
    while True:
        clientSocket,clientAddress = socketDict['SerpentSocket'].accept()
        clientSocket.send(encryption.encrypt("this ralloc proj"))
        printStatistics()
        break;

def dsaEncryption(message):

    print "message is ",message

    encryptionKey = DSA.generate(1024)
    x = random.StrongRandom().randint(1,encryptionKey.q-1)
    signature = encryptionKey.sign(message,x)

    socketDict['DSASocket'].listen(5)
    while True:
        clientSocket,clientAddress = socketDict['DSASocket'].accept()
        print 'the client address is ',clientAddress
        # now we will send the key followed by hthe signature
        clientSocket.send(pickle.dumps(encryptionKey))
        clientSocket.send(pickle.dumps(signature))
        printStatistics()
        socketDict['DSASocket'].close()
        break;


# dsaEncryption()

def printStatistics():
    currentProcess = psutil.Process(pid = os.getpid())
    with currentProcess.oneshot():
        currCpuConsumption = currentProcess.cpu_times().system
        currMemConsumption = currentProcess.memory_info().vms

    print "Network consumption:\n  Bytes Sent: ",psutil.net_io_counters().bytes_sent,"\n  Bytes Recieved: ",psutil.net_io_counters().bytes_sent
    print "CPU Consumption ",currCpuConsumption/psutil.cpu_times().system
    print "Memory Consumption ",float(currMemConsumption)/float(psutil.virtual_memory().total)


for index in socketConfig:
    # socketList.get(index) = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # hostname = socket.gethostname()
    # socketList.get(index).bind((hostname,port))
    socketDict[index].bind(bindConfig[socketConfig[index]]);

keySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
keySocket.connect((socket.gethostname(),9000))
keySocket.send("server")
print keySocket.recv(2048)

encType = keySocket.recv(2048)
print encType
if encType == "AES":
    PUBLIC_KEY = keySocket.recv(2048)
    aesEncryption(PUBLIC_KEY)

elif encType == "BlowFish":
    PUBLIC_KEY = keySocket.recv(2048)
    blowfishEncryption(PUBLIC_KEY)

elif encType == "DSA":
    MESSAGE = keySocket.recv(2048)
    dsaEncryption(MESSAGE)

elif encType == "Serpent":
    PUBLIC_KEY = keySocket.recv(2048)
    serpentEncryption(PUBLIC_KEY)
