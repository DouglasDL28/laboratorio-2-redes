from array import array
from bitarray import bitarray
from bitarray.util import int2ba


poly = 0xEDB88320

#Se inicializa la tabla CRCT que es un array de 256 constantes de 32-bit
table = array('L')
for byte in range(256):
    crc = 0
    #Se forman los 32 bits
    for bit in range(8):
        if (byte ^ crc) & 1:
            crc = (crc >> 1) ^ poly
        else:
            crc >>= 1
        byte >>= 1
    #Se insertan en la tabla
    table.append(crc)

def crc32Calculator(bitarrayStr: bitarray):
    bytearrayStr = bitarray.tobytes(bitarrayStr)
    #Se inicializa el valor inicial de CRC-32 
    crc32 = 0xFFFFFFFF
    #Se recorre la cadena por byte
    for byte in bytearrayStr:
        crc32 = table[(byte ^ crc32) & 0xFF] ^ (crc32 >> 8)
    #Se finaliza el valor de CRC-32 invirtiendo todos los bits
    return bitarrayStr + bitarray(int2ba(crc32 ^ 0xFFFFFFFF))

def crc32Check(bitarrayStr: bitarray):
    bytearrayStr = bitarray.tobytes(bitarrayStr[:len(bitarrayStr) - 32])
    bytearrayCRC32Check = bitarrayStr[-32:]
    #Se inicializa el valor inicial de CRC-32 
    crc32 = 0xFFFFFFFF
    #Se recorre la cadena por byte
    for byte in bytearrayStr:
        crc32 = table[(byte ^ crc32) & 0xFF] ^ (crc32 >> 8)
    #Se finaliza el valor de CRC-32 invirtiendo todos los bits
    return bitarrayStr[:len(bitarrayStr) - 32], bitarray(int2ba(crc32 ^ 0xFFFFFFFF)) != bytearrayCRC32Check

def tryAlgorithm():
    message = b'Un mensaje'
    bitarr = bitarray()
    bitarr.frombytes(message)
    corruptMessage = b'Un mensaji'
    corruptBitarr = bitarray()
    corruptBitarr.frombytes(corruptMessage)

    a = crc32Calculator(bitarr)

    b = crc32Calculator(corruptBitarr)

    print(crc32Check(bitarr + a[-32:]))
    print(crc32Check(bitarr + b[-32:]))