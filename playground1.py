# import uuid
#
# test = str(uuid.uuid4()).encode("utf-16-le")
# test1 = bytearray(256)
# test1[0:72] = test
# print(test1.hex())
# import time

# test = Event()
# user_id = uuid.uuid4()
# print(user_id)
# test.user_id = user_id
# print(test.user_id)
#
# b = test.to_bytes()
# test1 = Event.from_bytes(b)
# print(test1.user_id)



# use to receive messages to workstation. ex. desktop readers'
# taken from `parsec.ini`
# workstation_id = UUID("{1e896af9-0df0-46fb-b501-97dfe2453015}") #  fb2f05a8-12df-4f0f-80e3-dfaf97be7e6f workstation_id

# use to receive hardware messages
# taken from parsec3.dictionary.dat
# territories_root_id = UUID("{60b5b66d-0def-4529-bc77-f680f532cd87}") # 9A0BB8FB-FBC7-45D8-985F-144CFCA6410D root_id

# use to receive audit messages
# taken from MS SQL Parsec3 DB only =(
# operator_security_group_id = UUID("{dfbb1f3b-2641-4742-9ce5-6a7b109ef84f}")
# personel_root_id = UUID("{b96092e7-51f0-4148-9cb2-0502a0210d45}")
#
# sources = [workstation_id,
#            territories_root_id,
#            operator_security_group_id,
#            personel_root_id]


# callback
#def received(data: Event):
#    print(data.json())


#listener = transport.listen_events_from(received, sources)

#user_input = input()
#while user_input != "exit":
#    print(user_input)
#    user_input = input()

#listener.stop()
from uuid import UUID

import transport
# from local_db import Dictionary
#
# db = Dictionary()
#
# listener = transport.listen_events_from(received, db.get_root_ids())
# print(listener)
from constants import ParamKey
from controllers import ControllerState

# data = transport.request_component_state(UUID('71914484-1072-47BB-B825-5D820B062F4A'))
# nc_state = ControllerState()
# print(nc_state.EnterSwitch)
# nc_state.initialize(data)
# print(nc_state.EnterSwitch)


from event_xtensions import *
st = Event()
st.operator_comments = 'йцукенгшщзфывапролдж'

print(st.json())
print(st.operator_comments)
