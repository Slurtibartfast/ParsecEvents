import json
import struct
from datetime import datetime
from enum import Enum
from uuid import UUID

from constants import ParamType, Method, SourceType, DataBit, MessageType, ParamKey
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
    def create_command(code, destination_id: UUID):
        return Event.__create(MessageType.mtCommand, code, destination_id)

    @staticmethod
    def create_event(code, source_id: UUID):
        return Event.__create(MessageType.mtEvent, code, source_id)

    @staticmethod
    def create_invoke(code, destination_id: UUID):
        return Event.__create(MessageType.mtInvoke, code, destination_id)

    @staticmethod
    def __create(type: MessageType, code, component_id: UUID):
        if isinstance(code, Enum):
            code = code.value

        result = Event()
        result.component_id = component_id
        result.code = (type.value << 24) | (code & 0x00ffffff)

        return result

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
        itemsCount = struct.unpack("QII", value[offset:offset + 16])

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
            "items": list(map(lambda x: x.json, self.items))},
            default=str,
            indent=4)

    def find_items(self, key: ParamKey, type: ParamType = None):
        return [x for x in self.items if x.key == key and (type is None or x.type == type)]

    def find_item(self, key: ParamKey, type: ParamType, instance: int):
        result = None
        for x in self.items:
            if x.key == key and x.type == type and x.instance == instance:
                result = x
                break
        return result

    def get_state_by_id(self, id: UUID):
        result = None
        for item in self.items:
            if (item.key == ParamKey.pkComponent and item.type == ParamType.ptGuid) or \
                    (item.key == ParamKey.pkPart and item.type == ParamType.ptGuid):
                if item.data == id:
                    found = self.find_item(ParamKey.pkState, ParamType.ptDword, item.instance)
                    result = found.data if found else None
                    break
                else:
                    continue
        return result

    def set_item_data(self, key: ParamKey, type: ParamType, instance: int, data):
        found = self.find_item(key, type, instance)
        if found:
            found.data = data
        else:
            self.items.append(EventItem.create(key, type, data, instance))

    def get_item_data(self, key: ParamKey, type: ParamType, instance: int):
        found = self.find_item(key, type, instance)
        return found.data if found else None

    def get_string(self, key: ParamKey) -> str or None:
        short_value = self.get_item_data(key, ParamType.ptChar, 0)
        if short_value:
            return short_value
        else:
            long_value_length = self.get_item_data(key, ParamType.ptDword, 0)
            if long_value_length:
                binary_long_value = bytearray()
                instance = 0
                while long_value_length > 0:
                    long_value_length -= 16
                    binary_long_value += self.get_item_data(key, ParamType.ptByteBuffer, instance)
                    instance += 1
                return binary_long_value.decode(encoding="utf-8")
            else:
                return None

    def set_string(self, key: ParamKey, value: str):
        if len(value) <= 16:
            self.set_item_data(key, ParamType.ptChar, 0, value)
        else:
            binary_value = value.encode("utf-8")
            value_length = len(binary_value)
            self.set_item_data(key, ParamType.ptDword, 0, value_length)
            instance = 0
            comment_length = 0
            end_index = 16
            while comment_length < value_length:
                self.set_item_data(key, ParamType.ptByteBuffer, instance,
                                   binary_value[comment_length:end_index])
                instance += 1
                comment_length = end_index
                end_index += 16


class EventItem:
    binarySize = 20

    def __init__(self):
        self.type = ParamType.ptAny
        self.key = ParamKey.pkAny
        self.instance = 0
        self.temporary = False
        self.__data = bytearray(16)

    @staticmethod
    def create(key: ParamKey, type: ParamType, value=None, instance: int = 0):
        result = EventItem()
        result.key = key
        result.type = type
        result.instance = instance
        if value:
            result.data = value

        return result

    @staticmethod
    def from_bytes(value: bytes):
        result = EventItem()
        header = int.from_bytes(value[:4], byteorder="little")
        result.__data = value[4:]
        result.temporary = (header & 0x80000000) != 0
        result.instance = header & 0xff
        result.type = ParamType((header & 0x7fffff00) >> 24)
        result.key = ParamKey((header >> 8) & 0xffff)

        return result

    def to_bytes(self):
        header = 0
        if self.temporary:
            header |= 1 << 31

        header |= (self.type.value & 0x7f) << 24
        header |= (self.key.value & 0xffff) << 8
        header |= (self.instance & 0xff)

        return header.to_bytes(4, "little") + self.__data

    @property
    def json(self):
        return {
            "key": self.key,
            "type": self.type,
            "instance": self.instance,
            "data": self.data}

    @property
    def data(self):
        if self.type == ParamType.ptGuid:
            return UUID(bytes_le=bytes(self.__data))
        elif self.type == ParamType.ptChar:
            return self.__data.decode(encoding="utf-8").rstrip('\0')
        elif self.type == ParamType.ptDouble:
            return struct.unpack("d", self.__data[:8])[0]
        elif self.type == ParamType.ptDword:
            return int.from_bytes(self.__data[:4], byteorder="little", signed=False)
        elif self.type == ParamType.ptI64:
            return int.from_bytes(self.__data[:8], byteorder="little", signed=False)
        elif self.type == ParamType.ptTime:
            if all(x == 0 for x in self.__data):
                return None
            else:
                return datetime.fromtimestamp(int.from_bytes(self.__data, byteorder="little", signed=False))
        elif self.type == ParamType.ptByteBuffer:
            return self.__data
        else:
            raise Exception()

    @data.setter
    def data(self, value):
        if self.type == ParamType.ptGuid:
            if type(value) is not UUID:
                raise Exception()
            bytes_value = value.bytes_le
        elif self.type == ParamType.ptChar:
            if type(value) is not str:
                print('тип данных: ', type(value))
                raise Exception()
            bytes_value = value.encode(encoding="utf-8")
        elif self.type == ParamType.ptDouble:
            if type(value) is not float:
                raise Exception()
            bytes_value = struct.pack("d", float(value))
        elif self.type == ParamType.ptDword:
            if type(value) is not int:
                raise Exception()
            bytes_value = value.to_bytes(length=4, byteorder="little")
        elif self.type == ParamType.ptI64:
            if type(value) is not int:
                raise Exception()
            bytes_value = value.to_bytes(length=8, byteorder="little")
        elif self.type == ParamType.ptTime:
            if type(value) is not datetime:
                raise Exception()
            bytes_value = int(value.timestamp()).to_bytes(length=4, byteorder="little")
        elif self.type == ParamType.ptByteBuffer:
            if (type(value) is bytes) or (type(value) is bytearray):
                bytes_value = value
            else:
                raise Exception()
        else:
            raise Exception()

        self.__data[0:len(bytes_value)] = bytes_value
