import json
import uuid
from datetime import datetime
from struct import unpack

from CommonEnums import MessageType, SourceType, DataBit, Method
from EventItem import EventItem


# привет
class Event:
    def __init__(self):
        self.id = None
        self.parentId = None
        self.componentId = None
        self.timestamp = None
        self.method = Method.miAddUser
        self.sourceType = SourceType.stErrRestore
        self.subSystem = 0
        self.dataBits = DataBit.dbUndefined
        self.messageType = MessageType.mtEvent
        self.hardware = 0
        self.items = []

    def fromByteArray(value: bytes):
        result = Event()

        # skip 36 bytes envelope
        offset = 36

        result.id = uuid.UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.parentId = uuid.UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.componentId = uuid.UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        time, \
        code, \
        itemsCount = unpack("QII", value[offset:offset + 16])

        offset += 16

        result.timestamp = datetime.fromtimestamp(time)

        result.method = Method(code & 0xff)
        result.sourceType = SourceType((code >> 8) & 0x1f)
        result.subSystem = (code >> 13) & 0x7
        result.dataBits = DataBit((code >> 16) & 0xff)
        result.messageType = MessageType((code >> 24) & 0x1f)
        result.hardware = (code >> 29) & 0x7

        for index in range(itemsCount):
            result.items.append(EventItem.fromByteArray(value[offset:offset + EventItem.binarySize]))
            offset += EventItem.binarySize

        return result

    def toByteArray(self):
        result = self.id.bytes_le
        result += self.parentId.bytes_le
        result += self.componentId.bytes_le
        result += int(self.timestamp()).to_bytes(length=4, byteorder="little")

        code = 0
        code |= (self.hardware & 0x7) << 29
        code |= (self.messageType & 0x1f) << 24
        code |= (self.dataBits & 0xff) << 16
        code |= (self.subSystem & 0x7) << 13
        code |= (self.sourceType & 0x1f) << 8
        code |= self.method & 0xff

        result += code.to_bytes(4, "little")
        result += len(self.items).to_bytes(4, "little")

        for item in self.items:
            result += item.toByteArray()

        return result

    def json(self):
        return json.dumps({
            "id": self.id,
            "parentId": self.parentId,
            "componentId": self.componentId,
            "timestamp": self.timestamp,
            "method": self.method,
            "sourceType": self.sourceType,
            "subSystem": self.subSystem,
            "dataBits": self.dataBits,
            "messageType": self.messageType,
            "hardware": self.hardware,
            "items": list(map(lambda x: x.json(), self.items))},
            default=str,
            indent=4)

    """
    def create(id : mId, parentId : mParentId, componentId : mComponentId, timestamp: mDate, \
               method: mOperationCode, sourceType: mSourceType, subSystem: mSubSystem, \
               dataBits: mDataBits, messageType: mMessageType, hardware: mHardware, value=None):
        result = Event()
        result.id = id
        result.parentId = parentId
        result.componentId = componentId
        result.timestamp = timestamp
        result.method = method
        result.sourceType = sourceType
        result.subSystem = subSystem
        result.dataBits = dataBits
        result.messageType = messageType
        result.hardware = hardware
        if value:
            result.items = value
        return result



    def json(self):
        return {
            "operationCode": self.operationCode
            "sourceType": self.sourceType
            "subSystem": self.subSystem
            "dataBits": self.dataBits
            "messageType": self.messageType
            "hardware": self.hardware
            
        }

"""
