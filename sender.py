import socket
import sys
import threading
import pickle
from bitarray import bitarray
import config

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

def sender_thread():
    
    global RUNNING
    while RUNNING:
        
        message = str(input('Input the messege:'))

        #Pickle para serializar el mensaje
        # message = input('Ingrese un mensaje')

        pickleMessage = pickle.dumps(message)

        bitarr = bitarray()
        bitarr.frombytes(pickleMessage)
        

        #Agragar ruido al binario

        sock.send(bitarr)

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