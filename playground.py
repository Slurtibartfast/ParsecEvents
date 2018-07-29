from uuid import UUID
from Transport import Transport
from Event import Event
import xtensions


test = Transport()
test.send_command(UUID.empty(), UUID.empty(), Event())
