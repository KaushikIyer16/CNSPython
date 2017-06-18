#  this should act as a key exchange client
import socket
import os
import psutil
import random
import string

kdcSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

kdcSocket.bind((socket.gethostname(),9000))
kdcSocket.listen(5)

clientSocket = None
serverSocket = None

while True:
    clientSocket,clientAddr = kdcSocket.accept()
    data = clientSocket.recv(2048)
    if data == "server":
        clientSocket.send("your a server")
        serverSocket = clientSocket
    elif data == "client":
        # clientSocket.send("your a client")
        encType = clientSocket.recv(2048)
        if encType == "AES":
            # create public key of 64 bit
            serverSocket.send("AES")

            PUBLIC_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(16))
            clientSocket.send(PUBLIC_KEY)
            serverSocket.send(PUBLIC_KEY)

        elif encType == "DSA":
            # generate (p,q)
            serverSocket.send("DSA")
            MESSAGE = ''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(16))
            clientSocket.send(MESSAGE)
            serverSocket.send(MESSAGE)

        elif encType == "RSA":
            serverSocket.send("RSA")
            MESSAGE = ''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(16))
            clientSocket.send(MESSAGE)
            serverSocket.send(MESSAGE)

        elif encType == "BlowFish":

            serverSocket.send("BlowFish")
            PUBLIC_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(16))
            clientSocket.send(PUBLIC_KEY)
            serverSocket.send(PUBLIC_KEY)

        elif encType == "Serpent":

            serverSocket.send("Serpent")
            PUBLIC_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits+string.ascii_lowercase) for _ in range(16))
            clientSocket.send(PUBLIC_KEY)
            serverSocket.send(PUBLIC_KEY)

    else:
        clientSocket.send("option not valid")

kdcSocket.close()
