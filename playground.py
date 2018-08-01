import uuid
from uuid import UUID

import ini
from constants import *
import transport
from event import Event
import xtensions



door_id = uuid.uuid4()

transport.send_command(DoorCommand.Open, door_id)

# use to receive messages to workstation. ex. desktop readers'
# taken from `parsec.ini`
workstation_id = UUID("{1e896af9-0df0-46fb-b501-97dfe2453015}")

# use to receive hardware messages
# taken from parsec3.dictionary.dat
territories_root_id = UUID("{60b5b66d-0def-4529-bc77-f680f532cd87}")

# use to receive audit messages
# taken from MS SQL Parsec3 DB only =(
operator_security_group_id = UUID("{dfbb1f3b-2641-4742-9ce5-6a7b109ef84f}")
personel_root_id = UUID("{b96092e7-51f0-4148-9cb2-0502a0210d45}")

sources = [workstation_id,
           territories_root_id,
           operator_security_group_id,
           personel_root_id]


# callback
def received(data: Event):
    print(data.json())


listener = transport.listen_events_from(received, sources)

user_input = input()
while user_input != "exit":
    print(user_input)
    user_input = input()

listener.stop()
