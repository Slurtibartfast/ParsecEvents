import uuid
from uuid import UUID

from constants import *
import transport
from event import Event, EventItem
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import xtensions

token = 'de69daa37e9b587a3f23878c9d60514b484d946af62eb910712d0fce3edfc5cb2bd4e5d8a61474b6d2e17'
my_vk_id = 4073426
nc_8k_144_door = 'D874D77B-409A-4505-9866-414E7D722A8E'         # NC-8000 192.168.0.144
nc_8k_144_drive = '71914484-1072-47BB-B825-5D820B062F4A'        #component 0
nc_8k_144_relay = 'C53016D1-3E70-44EB-B2FB-BCDE6F8E02D1'            #part relay
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def console_log(id, text):
    print('id{}: "{}"'.format(id, text), end=' ')
    print(' ok')

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id == my_vk_id and event.text == '/сим':
            door_id = uuid.UUID(nc_8k_144_door)
            transport.send_command(DoorCommand.Open, door_id)
            vk.messages.send(
                user_id=event.user_id,
                message='Выполняю команду: Открыть дверь(nc-8k-144)'
            )

        elif event.user_id == my_vk_id and event.text == '/р':
            drive_id = uuid.UUID(nc_8k_144_drive)
            relay_id = uuid.UUID(nc_8k_144_relay)
            transport.send_relay_command(RelayCommand.On, drive_id, relay_id)
            vk.messages.send(
                user_id=event.user_id,
                message='Выполняю команду: Включить реле(nc-8k-144)'
            )

        elif event.text == '/умри':
            vk.messages.send(
                user_id=event.user_id,
                message='Asta Lavista'
            )
            break
        console_log(event.user_id, event.text)



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
