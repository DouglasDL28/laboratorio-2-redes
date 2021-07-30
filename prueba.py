import pickle
from bitarray import bitarray

# message = input('Ingrese un mensaje')
message = 'Ingrese un mensaje'

pickleMessage = pickle.dumps(message)

response = bitarray()
response.frombytes(pickleMessage)

print(response)

#Ruido

byteMessage = response.tobytes()
messageDecode = pickle.loads(byteMessage)

# print(response)
print(messageDecode)