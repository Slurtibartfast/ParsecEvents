from datetime import datetime

buffer = bytearray(16)
print(type(buffer))
print(buffer)

print(datetime.min)

initial = datetime.fromtimestamp(float(100000))
print(type(initial))
print(initial)



print(int(initial.timestamp()))

#initialBinary = int(initial.timestamp()).to_bytes(4,)

"""
buffer[0:len(initialBinary)] = initialBinary
print(type(buffer))
print(buffer)
print(len(buffer))

value = struct.unpack("d", buffer[:8])[0]
print(type(value))
print(value)


datetime.datetime.fromtimestamp(int(self.__data))
"""