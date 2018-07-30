import enum
import uuid
import threading
from uuid import UUID

from CommonEnums import MessageCategory
from Event import Event
import win32file
import pywintypes
import xtensions


class CMA(enum.Enum):
    CMA_SUBSCRIBE = 1
    CMA_SEND = 2
    CMA_EVENT = 3
    CMA_REGISTER = 4
    CMA_UNREGISTER = 5
    CMA_UNSUBSCRIBE = 6
    CMA_STOREDATA = 10


def transport_control_slot():
    return r"\\.\mailslot\parsec_transport_control"


def control_message_send(data: Event, destination_id: UUID = None, workstation_id: UUID = None):
    result = CMA.CMA_SEND.value.to_bytes(length=4, byteorder="little")
    result += workstation_id.bytes_le if workstation_id else UUID.empty().bytes_le
    result += destination_id.bytes_le if destination_id else data.component_id.bytes_le
    result += data.to_bytes()
    return result


def control_message_subscribe(listener_id: UUID, sources: list, categories: MessageCategory):
    result = CMA.CMA_SUBSCRIBE.value.to_bytes(length=4, byteorder="little")

    buffer = bytearray(256)
    buffer[:72] = str(listener_id).encode("utf-16-le")
    result += buffer

    result += categories.value.to_bytes(length=8, byteorder="little")
    result += len(sources).to_bytes(length=4, byteorder="little")

    for source in sources:
        result += source.bytes_le

    return result


def control_message_unsubscribe(listener_id: UUID, sources: list):
    result = CMA.CMA_UNSUBSCRIBE.value.to_bytes(length=4, byteorder="little")

    buffer = bytearray(256)
    buffer[:72] = str(listener_id).encode("utf-16-le")
    result += buffer

    result += bytearray(4)
    result += len(sources).to_bytes(length=4, byteorder="little")

    for source in sources:
        result += source.bytes_le

    return result


def send_control_message(data: bytes):
    slot = win32file.CreateFile(transport_control_slot(),
                                win32file.GENERIC_WRITE,
                                win32file.FILE_SHARE_READ,
                                None,
                                win32file.OPEN_EXISTING,
                                0,
                                None)
    win32file.WriteFile(slot, data)
    win32file.CloseHandle(slot)


def send_command(data: Event, destination_id: UUID = None, workstation_id: UUID = None):
    send_control_message(control_message_send(data, destination_id, workstation_id))


def listen_events_from(callback, sources: list, categories: MessageCategory = MessageCategory.All):
    result = EventsListener(sources, categories, callback)
    result.start()
    return result


class __Listener(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.id = uuid.uuid4()
        self.__slot_name = r"\\.\mailslot\{0}".format(self.id)
        self.__slot = None
        self.__stopped = threading.Event()
        self.__callback = callback

    def __del__(self):
        if self.__slot:
            win32file.CloseHandle(self.__slot)

    def run(self):
        self.__stopped.clear()

        timeout = 100
        buffer_size = 4096
        envelope_size = 36

        try:
            self.__slot = win32file.CreateMailslot(self.__slot_name, 0, timeout, None)
            while not self.is_stopped():
                try:
                    result, data = win32file.ReadFile(self.__slot, buffer_size, None)
                    if result == 0:
                        self.__callback(Event.from_bytes(data[envelope_size:]))
                except pywintypes.error:
                    # expected - timeout
                    pass

        finally:
            if self.__slot:
                win32file.CloseHandle(self.__slot)

            self.__slot = None

    def stop(self):
        self.__stopped.set()
        self.join()

    def is_stopped(self):
        self.__stopped.is_set()


class EventsListener(__Listener):

    def __init__(self, sources: list, categories: MessageCategory, callback):
        super().__init__(callback)
        self.sources = sources
        self.categories = categories

    def run(self):
        send_control_message(control_message_subscribe(self.id, self.sources, self.categories))
        super().run()
        send_control_message(control_message_unsubscribe(self.id, self.sources))
