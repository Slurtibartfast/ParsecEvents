import enum
import uuid
import threading
from uuid import UUID

from constants import MessageCategory, ParamKey, ParamType, Method
from event import Event, EventItem
import win32file
import pywintypes
import xtensions
import event_xtensions


def send_command(code,
                 destination_id: UUID,
                 workstation_id: UUID = None,
                 operator_id: UUID = None,
                 customization = None):
    event = Event.create_command(code, destination_id)

    if workstation_id:
        event.workstation_id = workstation_id

    if operator_id:
        event.operator_id = operator_id

    if customization:
        customization(event)

    send_command_data(event)


# send command to relay
# `destination_id` is ID of box controller component
def send_relay_command(code,
                       destination_id: UUID,
                       part_number: int,
                       workstation_id: UUID = None,
                       operator_id: UUID = None,
                       customization = None):
    event = Event.create_command(code, destination_id)
    event.items.append(EventItem.create(ParamKey.pkPart, ParamType.ptDword, part_number))

    if workstation_id:
        event.workstation_id = workstation_id

    if operator_id:
        event.operator_id = operator_id

    if customization:
        customization(event)

    send_command_data(event)


def send_command_data(data: Event):
    _send_control_message(_control_message_send(data, data.workstation_id))


def send_event(code,
               source_id: UUID,
               destinations: list,
               categories: MessageCategory):
    event = Event.create_event(code, source_id)
    send_event_data(event, destinations, categories)


def send_event_data(data: Event,
                    destinations: list,
                    categories: MessageCategory):
    _send_control_message(_control_message_event(data, destinations, categories))


def listen_events_from(callback,
                       sources: list,
                       categories: MessageCategory = MessageCategory.All):
    result = EventsListener(callback, sources, categories)
    result.start()
    return result


def listen_commands_to(callback, destinations: list):
    result = CommandsListener(callback, destinations)
    result.start()
    return result


def request_component_state(id: UUID) -> int:
    result = 0

    received = threading.Event()

    def received_callback(data: Event):
        nonlocal result
        result = data.get_state_by_id(id)
        # print(result)
        received.set()

    listener = listen_events_from(received_callback, [id], MessageCategory.Status)
    send_command_data(Event.create_invoke(Method.miGetComponentState, id))
    received.wait()
    listener.stop()

    return result


class _CMA(enum.Enum):
    CMA_SUBSCRIBE = 1
    CMA_SEND = 2
    CMA_EVENT = 3
    CMA_REGISTER = 4
    CMA_UNREGISTER = 5
    CMA_UNSUBSCRIBE = 6
    CMA_STOREDATA = 10


def _transport_control_slot():
    return r"\\.\mailslot\parsec_transport_control"


def _control_message_send(data: Event, workstation_id: UUID = None):
    result = _CMA.CMA_SEND.value.to_bytes(length=4, byteorder="little")
    result += workstation_id.bytes_le if workstation_id else UUID.empty().bytes_le
    result += data.component_id.bytes_le
    result += data.to_bytes()
    return result


def _control_message_event(data: Event, destinations: list, categories: MessageCategory):
    result = _CMA.CMA_EVENT.value.to_bytes(length=4, byteorder="little")
    result += categories.value.to_bytes(length=8, byteorder="little")
    result += len(destinations).to_bytes(length=4, byteorder="little")
    result += bytes(8)
    result += data.to_bytes()

    for destination in destinations:
        result += destination.bytes_le

    return result


def _control_message_generic(action: _CMA, listener_id: UUID, ids: list):
    result = action.value.to_bytes(length=4, byteorder="little")

    buffer = bytearray(256)
    buffer[:72] = str(listener_id).encode("utf-16-le")
    result += buffer

    result += bytearray(4)
    result += len(ids).to_bytes(length=4, byteorder="little")

    for source in ids:
        result += source.bytes_le

    return result


def _control_message_subscribe(listener_id: UUID, sources: list, categories: MessageCategory):
    result = _CMA.CMA_SUBSCRIBE.value.to_bytes(length=4, byteorder="little")

    buffer = bytearray(256)
    buffer[:72] = str(listener_id).encode("utf-16-le")
    result += buffer

    result += categories.value.to_bytes(length=8, byteorder="little")
    result += len(sources).to_bytes(length=4, byteorder="little")

    for source in sources:
        result += source.bytes_le

    return result


def _control_message_unsubscribe(listener_id: UUID, sources: list):
    return _control_message_generic(_CMA.CMA_UNSUBSCRIBE, listener_id, sources)


def _control_message_register(listener_id: UUID, destinations: list):
    return _control_message_generic(_CMA.CMA_REGISTER, listener_id, destinations)


def _send_control_message(data: bytes):
    slot = win32file.CreateFile(_transport_control_slot(),
                                win32file.GENERIC_WRITE,
                                win32file.FILE_SHARE_READ,
                                None,
                                win32file.OPEN_EXISTING,
                                0,
                                None)
    win32file.WriteFile(slot, data)
    win32file.CloseHandle(slot)


class __Listener(threading.Thread):

    def __init__(self, callback):
        super().__init__()
        self.id = uuid.uuid4()
        self.__slot_name = r"\\.\mailslot\{0}".format(self.id)
        self.__slot = None
        self.__stopped = threading.Event()
        self.__callback = callback

    def __del__(self):
        self.stop()

    def run(self):
        self.__stopped.clear()

        timeout = 100
        buffer_size = 4096
        envelope_size = 36

        try:
            self.__slot = win32file.CreateMailslot(self.__slot_name, 0, timeout, None)
            self._subscribe()

            while not self.__is_stopped():
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
            self._unsubscribe()

    def _subscribe(self):
        pass

    def _unsubscribe(self):
        pass

    def stop(self):
        if self.is_alive():
            self.__stopped.set()
            self.join()

    def __is_stopped(self):
        return self.__stopped.is_set()


class EventsListener(__Listener):

    def __init__(self, callback, sources: list, categories: MessageCategory):
        super().__init__(callback)
        self.sources = sources
        self.categories = categories

    def _subscribe(self):
        _send_control_message(_control_message_subscribe(self.id, self.sources, self.categories))

    def _unsubscribe(self):
        _send_control_message(_control_message_unsubscribe(self.id, self.sources))


class CommandsListener(__Listener):

    def __init__(self, callback, destinations: list):
        super().__init__(callback)
        self.destinations = destinations

    def _subscribe(self):
        _send_control_message(_control_message_register(self.id, self.destinations))

    def _unsubscribe(self):
        _send_control_message(_control_message_unsubscribe(self.id, self.destinations))
