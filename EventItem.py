import datetime
import struct
import uuid
from CommonEnums import ParamKey, ParamType


class EventItem:
    binarySize = 20

    def __init__(self):
        self.type = ParamType.ptAny
        self.key = ParamKey.pkAny
        self.instance = 0
        self.temporary = False
        self.__data = bytearray(16)

    @staticmethod
    def create(key: ParamKey, type: ParamType, instance: int = 0, value=None):
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

    def json(self):
        return {
            "key": self.key,
            "type": self.type,
            "instance": self.instance,
            "data": self.data,
        }

    @property
    def data(self):
        if self.type == ParamType.ptGuid:
            return uuid.UUID(bytes_le=bytes(self.__data))
        elif self.type == ParamType.ptChar:
            return self.__data.decode(encoding="ascii").rstrip('\0')
        elif self.type == ParamType.ptDouble:
            return struct.unpack("d", self.__data[:8])[0]
        elif self.type == ParamType.ptDword:
            return int.from_bytes(self.__data, byteorder="little", signed=False)
        elif self.type == ParamType.ptI64:
            return int.from_bytes(self.__data, byteorder="little", signed=False)
        elif self.type == ParamType.ptTime:
            if all(x == 0 for x in self.__data):
                return None
            else:
                return datetime.datetime.fromtimestamp(int.from_bytes(self.__data, byteorder="little", signed=False))
        elif self.type == ParamType.ptByteBuffer:
            return self.__data
        else:
            raise Exception()

    @data.setter
    def data(self, value):
        if self.type == ParamType.ptGuid:
            if type(value) is not uuid.UUID:
                raise Exception()
            bytes_value = value.bytes_le
        elif self.type == ParamType.ptChar:
            if type(value) is not str:
                raise Exception()
            bytes_value = value.encode(encoding="ascii")
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
            if type(value) is not datetime.datetime:
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
