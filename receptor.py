import socket
import sys
import threading
import pickle
import config
from bitarray import bitarray

RUNNING = False

if len(sys.argv) <= 1:
    print("Usage: receptor.py <port>")
    sys.exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    server_port = int(sys.argv[1])
    server_addr = (config.SERVER_DEFAULT_IP, server_port)

    sock.bind(server_addr)
    sock.listen(5)

    messenger = False

    while not messenger:
        print("Waiting for messenger... ")
        conn, addr = sock.accept()
        print(conn, addr)

        messenger = True if conn and addr else False

    print("Messenger ready!")

    while True:
        # Start to receive the messege
        print("Waiting for message...")
        response = conn.recv(config.BUFF_SIZE)

        print("response:", response)

        bitarr = bitarray()
        bitarr.frombytes(response)

        # Parse bytes response to string
        # response = response.decode()
        byte_msg = bitarr.tobytes()
        print("byte_msg:", byte_msg)

        # byteMessage = response.tobytes()
        
        #Decode response
        message = pickle.loads(byte_msg)
        print("Messege:", message)
            #Verify response

            #Print response
    
    
    # Close connection
    sock.close()
