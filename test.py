import uuid
from datetime import datetime

from CommonEnums import ParamType, ParamKey
from EventItem import EventItem
header = 0x16162717
arr = header.to_bytes(4, "little")
arr+=b"AA"

int

print(arr.hex())
item = EventItem.create(ParamKey.pkUser, ParamType.ptDword, value=0xCAFE)


print(item.toByteArray())





