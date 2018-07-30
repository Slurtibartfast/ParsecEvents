import json
from enum import Enum
from uuid import UUID
from datetime import datetime
from struct import unpack
from CommonEnums import *
from EventItem import EventItem
import xtensions


class Event:
    def __init__(self):
        self.id = UUID.empty()
        self.parent_id = UUID.empty()
        self.component_id = UUID.empty()
        self.timestamp = datetime.now()
        self.code = 0
        self.operation_code = Method.miAddUser
        self.sourceType = SourceType.stErrRestore
        self.subSystem = 0
        self.dataBits = DataBit.dbUndefined
        self.messageType = MessageType.mtEvent
        self.hardware = 0
        self.items = []

    @staticmethod
    def from_bytes(value: bytes):
        result = Event()

        offset = 0
        result.id = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.parent_id = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        result.component_id = UUID(bytes_le=bytes(value[offset:offset + 16]))
        offset += 16

        time, \
        code, \
        itemsCount = unpack("QII", value[offset:offset + 16])

        offset += 16

        result.timestamp = datetime.fromtimestamp(time)

        result.code = code
        result.operation_code = code & 0xff
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
        result += self.parent_id.bytes_le
        result += self.component_id.bytes_le
        result += int(self.timestamp.timestamp()).to_bytes(length=8, byteorder="little")
        result += self.code.to_bytes(length=4, byteorder="little")
        result += len(self.items).to_bytes(length=4, byteorder="little")

        for item in self.items:
            result += item.to_bytes()

        return result

    def json(self):
        return json.dumps({
            "id": self.id,
            "parent_id": self.parent_id,
            "component_id": self.component_id,
            "timestamp": self.timestamp,
            "code": self.code,
            "operation_code": self.operation_code,
            "sourceType": self.sourceType,
            "subSystem": self.subSystem,
            "dataBits": self.dataBits,
            "messageType": self.messageType,
            "hardware": self.hardware,
            "items": list(map(lambda x: x.json(), self.items))},
            default=str,
            indent=4)

    @staticmethod
    def create_command(component_id: UUID, code):
        if isinstance(code, Enum):
            code = code.value

        result = Event()
        result.component_id = component_id
        result.code = (MessageType.mtCommand.value << 24) | (code & 0x00ffffff)

        return result

