import pickle
from bitarray import bitarray


""" EMISOR """
# Aplicación
# msg = str(input('Ingrese un mensaje')) # string
msg = "Hola mundo"
# Verificación
msg = msg.encode('ascii') # ascii encoding
bitarr = bitarray()
bitarr.frombytes(msg) # bitarray
## Correción/Detección
# Ruido
# Transmission
msg = pickle.dumps(bitarr)


""" RECEPTOR """
## Transmission
msg = pickle.loads(msg)
print("repector - transmission:", msg)
## Verificación
### Correción/Detección
msg = bitarray.tobytes(msg)
print("receptor - verificación:", msg)
msg = msg.decode()
print(str(msg))




# # RECEPTOR
# # message = 'Ingrese un mensaje'

# pickleMessage = pickle.dumps(message)

# response = bitarray()
# response.frombytes(pickleMessage)

# print(response)

# #Ruido

# # byteMessage = response.tobytes()
# messageDecode = pickle.loads(response)

# # print(response)
# print(messageDecode)