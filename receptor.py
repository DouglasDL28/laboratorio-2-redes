import socket
import sys
import threading
import pickle
import config
from bitarray import bitarray
from crc32 import crc32Calculator

RUNNING = False

if len(sys.argv) <= 1:
    print("Usage: receptor.py <port>")
    sys.exit()

def trans(conn):
    #Se recibe el mensaje
    response = conn.recv(config.BUFF_SIZE)
    
    #Se deserealiza el mensaje
    message = pickle.loads(response)

    return message

def coding(biteMessage):
    #Se convierte el mensaje de bitarray a bytes 
    return biteMessage.tobytes()

def verify(message):
    #Se aplican los algoritmos de detección y corrección
    #TODO
    #Detección de errores con el algoritmo CRC-32
    crc32 = crc32Calculator(message)
    print(crc32)

    #Se convierte a texto
    return ''.join(map(chr,message))

def app(message):
    #Print response
    print("Message:", message)

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
        
        #Recibir objeto
        print("Waiting for message...")
        biteResponse = trans(conn)

        #Codificación
        byteResponse = coding(biteResponse)

        #Verificación
        message = verify(byteResponse)

        #Aplicación
        app(message)
    
    
    # Close connection
    sock.close()
