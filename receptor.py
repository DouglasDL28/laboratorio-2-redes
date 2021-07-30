import socket
import sys
import threading
import pickle

RUNNING = False

BUFF_SIZE = 1000

if len(sys.argv) != 3:
    print("usage: client.py <server-ip> <port>")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

server_address = (server_ip, server_port)


def receptor_thread():
    # this function handles display
    global RUNNING
    while not RUNNING:
        response, _ = sock.recvfrom(BUFF_SIZE)

        # Parse bytes response to string
        # response = response.decode()
        byteMessage = response.tobytes()
        
        #Decode response
        message = pickle.loads(byteMessage)
        print(message)
        #Verify response

        #Print response
        

def start():
    # this function launches the game
    receptor = threading.Thread(target=receptor_thread)
    receptor.daemon = True
    receptor.start()

def initialize():
    print(f"Conectandose al server en el puerto: {server_ip}...")
    sock.connect(server_address)

initialize()
start()