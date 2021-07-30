import socket
import sys
import threading
import pickle
from bitarray import bitarray

RUNNING = False

BUFF_SIZE = 1000

if len(sys.argv) != 3:
    print("usage: client.py <server-ip> <port>")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

server_address = (server_ip, server_port)

def sender_thread():
    

    global RUNNING
    while not RUNNING:
        
        message = input('Ingrese un mensaje')

        #Pickle para serializar el mensaje
        # message = input('Ingrese un mensaje')

        pickleMessage = pickle.dumps(message)

        bitarr = bitarray()
        bitarr.frombytes(pickleMessage)
        

        #Agragar ruido al binario

        sock.send(bitarr)

        print("Enviando el movimiento al server...")
        # board.move_piece(best_move[0], best_move[1])
        # board.change_turn()

        # a = 1 # TODO: remove when you have done the above task...
        

def start():
    # this function launches the game
    sender = threading.Thread(target=sender_thread)
    sender.daemon = True
    sender.start()

def initialize():
    print(f"Conectandose al server en el puerto: {server_ip}...")
    sock.connect(server_address)

initialize()
start()