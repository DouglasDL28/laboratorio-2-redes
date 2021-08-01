import socket
import sys
import threading
import pickle
import config
from bitarray import bitarray
from hamming import hamming_verification, rm_r_bits, calc_r_bits
from crc32 import crc32Check

RUNNING = False

if len(sys.argv) <= 1:
    print("Usage: receptor.py <port>")
    sys.exit()


def trans(conn):
    #Se recibe el mensaje
    response = conn.recv(config.BUFF_SIZE)

    return response


def coding(response):
    
    #Se deserealiza el mensaje (bitarray)
    return pickle.loads(response)

def verify(message):
    
    #Se aplican los algoritmos de detección y corrección
    if config.ALGORITHM == "crc32":
        message, isCorrupt = crc32Check(message)
        if isCorrupt:
            print("\tCRC32 - Error detected.")
        else:
            print(f"\tCRC32 - No error detected.")

    if config.ALGORITHM == 'hamming':
        r = calc_r_bits(len(message))
        error = hamming_verification(message, r)
        if error:
            if error > len(message):
                print("\tHAMMING - More than one error detected.")
            else:
                print(f"\tHAMMING - Found error in {error}. Corrected.")
                message.invert(-1*error)
        else:
            print("\tHAMMING - No error detected.")

        message = rm_r_bits(message)

    message = bitarray.tobytes(message)

    #Se retorna el mensaje en texto plano
    return str(message.decode())


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
