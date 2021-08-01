from array import array


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

def crc32Calculator(string):
    #Se inicializa el valor inicial de CRC-32 
    crc32 = 0xFFFFFFFF
    #Se recorre la cadena por byte
    for byte in string:
        crc32 = table[(byte ^ crc32) & 0xFF] ^ (crc32 >> 8)
    #Se finaliza el valor de CRC-32 invirtiendo todos los bits
    return crc32 ^ 0xFFFFFFFF

message = b'Ingrese un mensaje'
corruptMessage = b'Ingrese un mensaji'


a = crc32Calculator(message)
print(a)

b = crc32Calculator(corruptMessage)
print(b)

print(a==b)