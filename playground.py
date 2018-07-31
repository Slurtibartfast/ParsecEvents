import uuid
from uuid import UUID

from constants import *
import transport
from event import Event
import xtensions
from event import EventItem

test = Event.create_command(10, uuid.uuid4())
test.items.append(EventItem.create(ParamKey.pkWorkstation, ParamType.ptGuid, uuid.uuid4()))

w_id = test.workstation_id

door_id = uuid.uuid4()

transport.send_command(DoorCommand.Open, door_id)


def received(data: Event):
    print(data.json())


soures = [UUID("{1e896af9-0df0-46fb-b501-97dfe2453015}"), UUID("{dfbb1f3b-2641-4742-9ce5-6a7b109ef84f}"),
          UUID("{60b5b66d-0def-4529-bc77-f680f532cd87}"), UUID("{b96092e7-51f0-4148-9cb2-0502a0210d45}")]
listener = transport.listen_events_from(received, soures)

user_input = input()
while user_input != "exit":
    print(user_input)
    user_input = input()

listener.stop()
