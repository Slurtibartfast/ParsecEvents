import json
from uuid import UUID
from datetime import datetime
from struct import unpack
from CommonEnums import *
from EventItem import EventItem
import xtensions


class Event:
    def __init__(self):
        self.id = UUID.empty()
        self.parentId = UUID.empty()
        self.componentId = UUID.empty()
        self.timestamp = datetime.now()
        self.code = 0
        self.method = Method.miAddUser
        self.sourceType = SourceType.stErrRestore
        self.subSystem = 0
        self.dataBits = DataBit.dbUndefined
        self.messageType = MessageType.mtEvent
        self.hardware = 0
        self.items = []

    def from_bytes(value: bytes):
        result = Event()

        # skip 36 bytes envelope
        offset = 36

        result.id = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.parentId = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.componentId = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        time, \
        code, \
        itemsCount = unpack("QII", value[offset:offset + 16])

        offset += 16

        result.timestamp = datetime.fromtimestamp(time)

        result.code = code
        result.method = Method(code & 0xff)
        result.sourceType = SourceType((code >> 8) & 0x1f)
        result.subSystem = (code >> 13) & 0x7
        result.dataBits = DataBit((code >> 16) & 0xff)
        result.messageType = MessageType((code >> 24) & 0x1f)
        result.hardware = (code >> 29) & 0x7

        for index in range(itemsCount):
            result.items.append(EventItem.from_bytes(value[offset:offset + EventItem.binarySize]))
            offset += EventItem.binarySize

        return result

    def to_bytes(self):
        result = self.id.bytes_le
        result += self.parentId.bytes_le
        result += self.componentId.bytes_le
        result += int(self.timestamp.timestamp()).to_bytes(length=8, byteorder="little")
        result += self.code.to_bytes(length=4, byteorder="little")
        result += len(self.items).to_bytes(length=4, byteorder="little")

        for item in self.items:
            result += item.to_bytes()

        return result

    def json(self):
        return json.dumps({
            "id": self.id,
            "parentId": self.parentId,
            "componentId": self.componentId,
            "timestamp": self.timestamp,
            "code": self.code,
            "method": self.method,
            "sourceType": self.sourceType,
            "subSystem": self.subSystem,
            "dataBits": self.dataBits,
            "messageType": self.messageType,
            "hardware": self.hardware,
            "items": list(map(lambda x: x.json(), self.items))},
            default=str,
            indent=4)

    def create_command(componentId: UUID, code: int):
        result = Event()
        result.componentId = componentId
        result.code = (MessageType.mtCommand.value << 24) | (code & 0x00ffffff)

        return result

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
