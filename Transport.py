import enum
from uuid import UUID
from Event import Event
import win32file
import xtensions


class Transport:
    class CMA(enum.Enum):
        CMA_SUBSCRIBE = 1
        CMA_SEND = 2
        CMA_EVENT = 3
        CMA_REGISTER = 4
        CMA_UNREGISTER = 5
        CMA_UNSUBSCRIBE = 6
        CMA_STOREDATA = 10

    TRANSPORT_CONTROL_SLOT = r"\\.\mailslot\parsec_transport_control"
    TRANSPORT_CONTROL_EVENT = r"Global\parsec_transport_control_event"

    def __init__(self):
        self.__slot = -1

    def __del__(self):
        if self.__slot != -1:
            win32file.CloseHandle(self.__slot)

    def __send_slot(self):
        if self.__slot == -1:
            try:
                self.__slot = win32file.CreateFile(Transport.TRANSPORT_CONTROL_SLOT,
                                                   win32file.GENERIC_WRITE,
                                                   win32file.FILE_SHARE_READ,
                                                   None,
                                                   win32file.OPEN_EXISTING,
                                                   0,
                                                   None)

            except:
                raise Exception()

        return self.__slot

    def __control_message_send(data: Event, destinationId: UUID = None, workstationId: UUID = None):
        result = Transport.CMA.CMA_SEND.value.to_bytes(length=4, byteorder="little")
        result += workstationId.bytes_le if workstationId else UUID.empty().bytes_le
        result += destinationId.bytes_le if destinationId else data.componentId.bytes_le
        result += data.to_bytes()
        return result

    def send_command(self, data: Event, destinationId: UUID = None, workstationId: UUID = None):
        win32file.WriteFile(self.__send_slot(), Transport.__control_message_send(
            data, destinationId, workstationId))
