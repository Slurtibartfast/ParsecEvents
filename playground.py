import uuid
from uuid import UUID

import ini
import local_db
from constants import *
import transport
from event import Event
import xtensions


door_id = uuid.uuid4()
# transport.send_command(DoorCommand.Open, door_id)

sources = [ini.transport.local_guid, ini.transport.server_guid]

dictionary = local_db.Dictionary()
sources += dictionary.get_root_ids()

# callback
def received(data: Event):
    print(data.json())


listener = transport.listen_events_from(received, sources)

user_input = input()
while user_input != "exit":
    print(user_input)
    user_input = input()

listener.stop()
