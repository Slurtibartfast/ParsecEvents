from uuid import UUID

def uuid_empty():
    return UUID(bytes_le=bytes(16))

UUID.empty = uuid_empty