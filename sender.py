import socket
import sys
import threading
import pickle
from bitarray import bitarray
import config
import random

RUNNING = True


if len(sys.argv) != 3:
    print("usage: client.py <server-ip> <port>")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

if sys.argv[1] == "default":
    server_ip = config.SERVER_DEFAULT_IP

server_addr = (server_ip, server_port)

def app():
    return str(input('Input the message:'))

def verify(message):
    #Se convierte el mensaje a Ascii
    asciiMessage = message.encode('utf-8')

    #Se convierte a bitarray  
    bitarr = bitarray()
    bitarr.frombytes(asciiMessage)
    return bitarr

def noice(message):
    #Se cambian algunos bites para agregarle ruido al mensaje
    for i in range(0, len(message)):
        if random.random() <= 0.005:
            message[i] = message[i] ^ 1
    messageWithNoice = message
    return messageWithNoice

def trans(message):
    #Pickle para serializar el mensaje
    pickleMessage = pickle.dumps(message)
    sock.send(pickleMessage)

def sender_thread():
    
    global RUNNING
    while RUNNING:
        
        #Aplicación
        message = app()

        #Verificación
        secureMessage = verify(message)

        #Ruido
        messageWithNoice = noice(secureMessage)

        #Transmisión
        trans(messageWithNoice)

        print("Sending messege to receptor...")
        

def start():
    # this function launches the game
    sender = threading.Thread(target=sender_thread)
    sender.daemon = True
    sender.start()

def initialize():
    print(f"Conectandose al server en el puerto: {server_ip}...")
    sock.connect(server_addr)

initialize()
# start()
sender_thread()