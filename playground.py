from uuid import UUID

from CommonEnums import *
from Transport import Transport
from Event import Event
import xtensions


doorId = UUID.empty()

test = Transport()
test.send_command(Event.create_command(doorId, DoorCommand.DoorOpen.value))
del test
