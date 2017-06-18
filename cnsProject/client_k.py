import socket
import Crypto
import pickle
import Crypto.Cipher.AES as aes
import blowfish as bf
import serpent as sp

#clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#clientSocket.connect((socket.gethostname(),9000))
socketDict = {
              'DSASocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'AESSocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'RSASocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'SerpentSocket'   : socket.socket(socket.AF_INET , socket.SOCK_STREAM),
              'BlowfishSocket' : socket.socket(socket.AF_INET , socket.SOCK_STREAM)
              }

connectConfig = {
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

#for index in socketConfig:
    #socketDict[index].connect(connectConfig[socketConfig[index]]);

def requestAES(PUBLIC_KEY):
    socketDict['AESSocket'].connect(connectConfig[socketConfig['AESSocket']]);
    encryption = aes.AESCipher(PUBLIC_KEY)
    print encryption.decrypt(socketDict['AESSocket'].recv(1024))
    socketDict['AESSocket'].close()

def requestDSA(message):

    print "message is ",message
    socketDict['DSASocket'].connect(connectConfig[socketConfig['DSASocket']]);
    encryptionKey = pickle.loads(socketDict['DSASocket'].recv(2048))
    signature = pickle.loads(socketDict['DSASocket'].recv(1024))


    if encryptionKey.verify(message,signature):
        print 'signature has been verified'
    else:
        print 'signature verification has failed'

def requestBlowfish(PUBLIC_KEY):
    socketDict['BlowfishSocket'].connect(connectConfig[socketConfig['BlowfishSocket']])
    print bf.decryptBlowfish(socketDict['BlowfishSocket'].recv(1024),PUBLIC_KEY)
    socketDict['BlowfishSocket'].close()

def requestSerpent(PUBLIC_KEY):
    socketDict['SerpentSocket'].connect(connectConfig[socketConfig['SerpentSocket']])
    encryption = sp.Serpent(PUBLIC_KEY)
    print encryption.decrypt(socketDict['SerpentSocket'].recv(2048))
    socketDict['SerpentSocket'].close()


# requestDSA()
# DSASocket.close()
# RSASocket.close()
# DESSocket.close()
# BlowfishSocket.close()

keySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
keySocket.connect((socket.gethostname(),9000))
keySocket.send("client")

reqAlgo = int(input("Enter the encryption type from \n1. AES encryption \n2. Blowfish \n3.Serpent \n4. DSA \n5.RSA \n"))
if reqAlgo == 1:
    keySocket.send("AES")
    PUBLIC_KEY =  keySocket.recv(2048)
    requestAES(PUBLIC_KEY)

elif reqAlgo == 2:
    keySocket.send("BlowFish")
    PUBLIC_KEY = keySocket.recv(2048)
    requestBlowfish(PUBLIC_KEY)

elif reqAlgo == 3:
    keySocket.send("Serpent")
    PUBLIC_KEY = keySocket.recv(2048)
    requestSerpent(PUBLIC_KEY)

elif reqAlgo == 4:
    keySocket.send("DSA")
    MESSAGE = keySocket.recv(2048)
    requestDSA(MESSAGE)
