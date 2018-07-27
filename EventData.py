from enum import IntFlag

class CommonEventData:
    pass

class ComponentEventData:
    pass

class EventData:
    pass

class ItemDataConst(IntFlag):
    MaxSize = 16

class ItemData:
    def __init__(self):
        self._key = None
        self._value = None
    #ItemData()
    #ItemData(key)
    def ParseKey(self, key):
        Instance = key & 0xFF
        IsTemporary = ((key & 0x80000000) != 0)
        self._key = key & 0x7FFFFF00
        Type = (ParamType)(self._key >> 24)

    pass

