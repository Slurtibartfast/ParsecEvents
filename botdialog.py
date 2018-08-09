import uuid
from uuid import UUID
from botmenue import *
from constants import *
import transport
# from event import Event
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import xtensions

token = 'de69daa37e9b587a3f23878c9d60514b484d946af62eb910712d0fce3edfc5cb2bd4e5d8a61474b6d2e17'
my_vk_id = 4073426
nc_8k_144_dev_id = '5D20F328-473E-4024-BBFA-DC1216FB513B'
nc_8k_144_door = 'D874D77B-409A-4505-9866-414E7D722A8E'         # NC-8000 192.168.0.144 door comp_no = 83886081
nc_8k_144_drive = '71914484-1072-47BB-B825-5D820B062F4A'        # NC-8000 192.168.0.144 box  comp_no = 0
part_no = 33554433                                              # relay_part_no
err_mes = 'Передать нужно цифру, соответствующую пункту меню'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def console_log(id, text):
    print('id{}: "{}"'.format(id, text), end=' ')
    print(' ok')

#----------------------------------------------- Flags ----------------------------------------------------------------
menue_main_flag = False
menue_controllers_flag = False
menue_controller_flag = False
menue_door_command_flag = False
menue_relay_command_flag = False
menue_status_flag = False
#----------------------------------------------------------------------------------------------------------------------

def flags():
    global menue_main_flag, menue_controllers_flag, menue_controller_flag, menue_door_command_flag, \
        menue_relay_command_flag, menue_status_flag
    menue_main_flag = False
    menue_controllers_flag = False
    menue_controller_flag = False
    menue_door_command_flag = False
    menue_relay_command_flag = False
    menue_status_flag = False


def send_message(userid, mesage):
    vk.messages.send(user_id=userid, message=mesage)

#--------------------------- Ожидаю новое сообщение в виде текста для бота---------------------------------------------

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id == my_vk_id and event.text == '/меню':
            flags()
            menue_main_flag = True # Возможно нужно сбросить остальные флаги
            menue = MainMenue()
            send_message(event.user_id, menue.create_menue())

#--------------------------- Ожидаю выбора пункта главного меню (пока только первый пункт)-----------------------------

        elif event.user_id == my_vk_id and event.text == '1' and menue_main_flag:
            menue_main_flag = False
            menue_controllers_flag = True
            menue_controllers = Controllers_menue()
            menue_controllers.get_controllers()
            send_message(event.user_id, menue_controllers.create_menue())


#--------------------------- Ожидаю выбора контроллера, чтобы провалиться в его меню ----------------------------------

        elif event.user_id == my_vk_id and event.text and menue_controllers_flag:
            indexr = int(event.text) if event.text.isdigit() else 0
            if 0 < indexr <= len(menue_controllers.items):
                menue_controllers_flag = False
                menue_controller_flag = True
                menue_controller = Controller_menue(indexr, menue_controllers.items)
                send_message(event.user_id, menue_controller.create_menue())
            else:
                send_message(event.user_id, err_mes)

#-----------------------------Меню дверь, реле или просмотр статусов -------------------------------------------

        elif event.user_id == my_vk_id and event.text and menue_controller_flag:
            indexr = int(event.text) if event.text.isdigit() else 0
            if 0 < indexr <= len(menue_controller.items):
                menue_controller_flag = False
                if indexr == 1:
                    menue_door_command_flag = True
                    menue_door_command = Door_command_menue(menue_controller.iteme[0])
                    send_message(event.user_id, menue_door_command.create_menue())

                elif indexr == 2:
                    menue_relay_command_flag = True
                    menue_relay_command = Relay_command_menue(menue_controller.iteme[0])
                    send_message(event.user_id, menue_relay_command.create_menue())

                elif indexr == 3:
                    menue_status_flag = True
                    menue_status = Status_menue(menue_controller.iteme[0])
                    send_message(event.user_id, menue_status.create_menue())

            else:
                send_message(event.user_id, err_mes)

#------------------------------ Команды двери -------------------------------------------------------------------------

        elif event.user_id == my_vk_id and event.text and menue_door_command_flag:
            indexr = int(event.text) if event.text.isdigit() else 0
            if 0 < indexr <= len(menue_door_command.items):
                if indexr == 1:
                    menue_door_command.door_open()
                    send_message(event.user_id, 'Выполняю команду: Открыть дверь')

                elif indexr == 2:
                    menue_door_command.door_close()
                    send_message(event.user_id, 'Выполняю команду: Закрыть дверь')

                elif indexr == 3:
                    menue_door_command.door_relative_block_on()
                    send_message(event.user_id, 'Выполняю команду: Включить относительную блокировку')

                elif indexr == 4:
                    menue_door_command.door_relativ_block_off()
                    send_message(event.user_id, 'Выполняю команду: Выключить относительную блокировку')

                elif indexr == 5:
                    menue_door_command.door_absolute_block_on()
                    send_message(event.user_id, 'Выполняю команду: Включить абсолютную блокировку')

                elif indexr == 6:
                    menue_door_command.door_absolute_block_off()
                    send_message(event.user_id, 'Выполняю команду: Выключить абсолютную блокировку')

                elif indexr == 7:
                    menue_door_command.door_guard_on()
                    send_message(event.user_id, 'Выполняю команду: Взять под охрану')

                elif indexr == 8:
                    menue_door_command.door_guard_off()
                    send_message(event.user_id, 'Выполняю команду: Снять с охраны')

                elif indexr == 9:
                    menue_door_command.door_open_enter()
                    send_message(event.user_id, 'Выполняю команду: Открыть на вход')

                elif indexr == 10:
                    menue_door_command.door_open_exit()
                    send_message(event.user_id, 'Выполняю команду: Открыть на выход')

                elif indexr == 11:
                    menue_door_command.door_apb_clear()
                    send_message(event.user_id, 'Выполняю команду: Снять АПБ')

            else:
                send_message(event.user_id, err_mes)

#------------------------------ Команды реле --------------------------------------------------------------------------

        elif event.user_id == my_vk_id and event.text and menue_relay_command_flag:
            indexr = int(event.text) if event.text.isdigit() else 0
            if 0 < indexr <= len(menue_relay_command.items):
                if indexr == 1:
                    menue_relay_command.relay_switch_on()
                    send_message(event.user_id, 'Выполняю команду: Включить доп.реле')

                elif indexr == 2:
                    menue_relay_command.relay_switch_off()
                    send_message(event.user_id, 'Выполняю команду: Выключить доп.реле')
            else:
                send_message(event.user_id, err_mes)

#------------------------------ Аварийный выход. Сброс всех флагов меню -----------------------------------------------

        elif event.user_id == my_vk_id and event.text == '/выход':
            flags()
            send_message(event.user_id, 'Начнем сначала (/меню)')

#------------------------------- Ожидание команды для открытия захардкоденной двери -----------------------------------

        if event.user_id == my_vk_id and event.text == '/сим':
            door_id = uuid.UUID(nc_8k_144_door)
            transport.send_command(DoorCommand.Open, door_id)
            send_message(event.user_id, 'Выполняю команду: Открыть дверь(nc-8k-144)')

#-------------------------------- Ожидание команды для включения доп.реле (хардкод)------------------------------------

        elif event.user_id == my_vk_id and event.text == '/р':
            drive_id = uuid.UUID(nc_8k_144_drive)
            transport.send_relay_command(RelayCommand.On, drive_id, part_no)
            send_message(event.user_id, 'Выполняю команду: Включить реле(nc-8k-144)')

#-------------------------------- Ожидание команды для выключения доп.реле (хардкод)-----------------------------------

        elif event.user_id == my_vk_id and event.text == '/рвык':
            drive_id = uuid.UUID(nc_8k_144_drive)
            transport.send_relay_command(RelayCommand.Off, drive_id, part_no)
            send_message(event.user_id, 'Выполняю команду: Включить реле(nc-8k-144)')

# -------------------------------- Ожидание команды для останоки скрипта ----------------------------------------------

        elif event.text == '/умри':
            send_message(event.user_id, 'Asta Lavista')
            break
        console_log(event.user_id, event.text)

#----------------------------------------------------------------------------------------------------------------------




