import struct
import uuid

buffer = bytearray(16)
print(type(buffer))
print(buffer)

initial = 123456.6
print(type(initial))
print(initial)

initialBinary = struct.pack("d",initial)

buffer[0:len(initialBinary)] = initialBinary
print(type(buffer))
print(buffer)
print(len(buffer))

value = struct.unpack("d", buffer[:8])[0]
print(type(value))
print(value)