from os import error
import socket
import sys
import pickle
import config
import time
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
    response = pickle.loads(response)
    #Se deserealiza el mensaje (bitarray)
    return response

def verify(message):
    """ Se aplican los algoritmos de detección y corrección """

    r = None

    if config.ALGORITHM == "crc32":
        message, error = crc32Check(message)
        if error:
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

    return str(message.decode("ascii", errors='ignore')), error, r, len(message.decode("ascii", errors='ignore'))


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
        response = trans(conn)    
        start = time.time()
        #Codificación
        byteResponse = coding(response)

        #Verificación
        message, error, redundancy, msg_len = verify(byteResponse)

        #Aplicación
        app(message)
        end = time.time()

        if config.ALGORITHM == 'hamming':
            error_det, error_corr = False, False
            if error:
                error_det, error_corr = True, True
                if error > msg_len:
                    error_corr = False

            csv_row = f"\n{config.PROBABILITY},{msg_len},{config.PROBABILITY},{bool(error)},{error_corr},{error_det},{redundancy}"

            with open('./tests/hamming/hamming.csv','a') as fd:
                fd.write(csv_row)
        
        if config.ALGORITHM == 'crc32':
            csv_row = f"\n{config.PROBABILITY},{msg_len},{config.ALGORITHM},{bool(error)},{end-start}"

            with open('./tests/crc32/crc32.csv','a') as fd:
                fd.write(csv_row)
    
    
    # Close connection
    sock.close()
