from uuid import UUID

_uuid_empty = UUID(bytes_le=bytes(16))


# add UUID.empty() to represent empty UUID

def uuid_empty():
    return _uuid_empty


UUID.empty = uuid_empty

# ----------------------------------------
