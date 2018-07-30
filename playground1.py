import uuid

test = str(uuid.uuid4()).encode("utf-16-le")
test1 = bytearray(256)
test1[0:72] = test
print(test1.hex())
