import json
import uuid
import sqlite3
from constants import *
import transport

sqlite3.register_converter('uniqueidentifier', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


class MainMenue:
    def __init__(self):
        self.menue_name = '*********Главное меню**********\n' + '*' * 35 + '\n'
        self.description = ' ' * 22 + 'Аллоха!\nТы попал в меню vk-бота Paresc\n(Created by yvinogradov@mdo.ru)\n' \
                                 'Давай же начнем работу. Итак, перед тобой меню, \
                        выбирай пункт который тебе интересен и отправляй мне его номер:\n'
        self.items = ['1⃣ Контроллеры\n', '2⃣ Информация по карте\n', '3⃣ О программе\n']
        self.kvadratik = '⃣'

    def json(self):
        return json.dumps({
            'Название меню': self.menue_name,
            'Описание': self.description,
            'Пункты меню': self.items},
            default=str,
            indent=2,
            ensure_ascii=False
        )

    def create_menue(self):
        result = self.menue_name + self.description
        for x in self.items:
            result += x
        return result

class Controllers_menue(MainMenue):
    def __init__(self):
        MainMenue.__init__(self)
        self.menue_name = '**********Контроллеры**********\n' + '-' * 52 +'\n'
        self.description = 'Выбирай контроллер, с которым будем работать дальше. Жду его номер:\n'
        self.items = []

    def get_controllers(self):
        with sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.halconfig.dat",
                             detect_types=sqlite3.PARSE_DECLTYPES) as conn_halconfig:
            cursor_halconfig = conn_halconfig.cursor()
            cursor_halconfig.execute("""SELECT DEV_ID, DEV_MODEL, DEV_ADDR
                                        FROM cfg_device
                                        WHERE DEV_MODEL like 'NC%'""")
            self.items = cursor_halconfig.fetchall()

    def create_menue(self):
        if self.items:
            result = ''
            for x in range(1, len(self.items) + 1):
                if x == len(self.items) + 1:
                    continue
                elif x < 10:
                    result += str(x) + self.kvadratik + ' {0}({1})\n'.format(str(self.items[x - 1][1]),
                                                                             str(self.items[x - 1][2]))
                else:
                    result += str(x)[0] + self.kvadratik + str(x)[1] + self.kvadratik + \
                              ' {0}({1})\n'.format(str(self.items[x - 1][1]), str(self.items[x - 1][2]))
            result_full = self.menue_name + self.description + result
            return result_full
        else:
            return 'Контроллеров доступа в системе не обнаружено'


class Controller_menue(MainMenue):
    def __init__(self, indexr, itemes):
        MainMenue.__init__(self)
        self.index = indexr - 1
        self.iteme = itemes[self.index]
        self.description = 'Выбери действие:\n'
        self.items = ['1⃣ Управление дверью\n', '2⃣ Управление доп.реле\n', '3⃣ Просмотр статусов\n']
        self.menue_name = 'Контроллер {}\n'.format(str(self.iteme[1:])) + '-' * 52 + '\n'


class Door_command_menue(MainMenue):
    def __init__(self, id_device):
        MainMenue.__init__(self)
        self.menue_name = 'Управление дверью:\n' + '-' * 52 +'\n'
        self.description = 'Пришли мне номер команды, которую необходимо выполнить\n'
        self.commands = []
        self.dev_id = id_device
        self.door_id = None
        self.items = ['1⃣ Открыть дверь\n', '2⃣ Закрыть дверь\n', '3⃣ Включить относительную блокировку\n',
                      '4⃣ Выключить относительную блокировку\n', '5⃣ Включить абсолютную блокировку\n',
                      '6⃣ Выключить абсолютную блокировку\n', '7⃣ Поставить на охрану\n', '8⃣ Снять с охраны\n',
                      '9⃣ Открыть на вход\n', '1⃣0⃣ Открыть на выход\n', '1⃣1⃣ Снять АПБ\n']

    def get_door_id(self, dev_id):
        with sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.halconfig.dat",
                             detect_types=sqlite3.PARSE_DECLTYPES) as conn_halconfig:
            cursor_halconfig = conn_halconfig.cursor()
            cursor_halconfig.execute("""SELECT comp_id
                                        FROM component
                                        WHERE comp_no = 83886081 and dev_id = :devid""", {'devid': dev_id})
            self.door_id = cursor_halconfig.fetchone()[0]

    def door_open(self):
        transport.send_command(DoorCommand.Open, self.door_id)
        print(self.door_id)

    def door_close(self):
        transport.send_command(DoorCommand.Close, self.door_id)

    def door_relative_block_on(self):
        transport.send_command(DoorCommand.RelativeBlockSet, self.door_id)

    def door_relativ_block_off(self):
        transport.send_command(DoorCommand.RelativeBlockClear, self.door_id)

    def door_absolute_block_on(self):
        transport.send_command(DoorCommand.AbsoluteBlockSet, self.door_id)

    def door_absolute_block_off(self):
        transport.send_command(DoorCommand.AbsoluteBlockClear, self.door_id)

    def door_guard_on(self):
        transport.send_command(DoorCommand.GuardSet, self.door_id)

    def door_guard_off(self):
        transport.send_command(DoorCommand.GuardClear, self.door_id)

    def door_open_enter(self):
        transport.send_command(DoorCommand.Open4Enter, self.door_id)

    def door_open_exit(self):
        transport.send_command(DoorCommand.Open4Exit, self.door_id)

    def door_apb_clear(self):
        transport.send_command(DoorCommand.APBClear, self.door_id)



class Relay_command_menue(MainMenue):
    def __init__(self, id_device):
        MainMenue.__init__(self)
        self.menue_name = 'Управление реле:\n' + '-' * 52 +'\n'
        self.description = 'Пришли мне номер команды, которую необходимо выполнить\n'
        self.dev_id = id_device
        self.drive_id = None
        self.part_no = 33554433
        self.items = ['1⃣ Включить реле\n', '2⃣ Выключить реле\n']

    def get_drive_id(self, dev_id):
        with sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.halconfig.dat",
                             detect_types=sqlite3.PARSE_DECLTYPES) as conn_halconfig:
            cursor_halconfig = conn_halconfig.cursor()
            cursor_halconfig.execute("""SELECT comp_id
                                        FROM component
                                        WHERE comp_no = 0 and dev_id = :devid""", {'devid': dev_id})
            self.drive_id = cursor_halconfig.fetchone()[0]
            print(type(self.drive_id))
            print(self.drive_id)
            print(self.dev_id)

    def relay_switch_on(self):
        transport.send_relay_command(RelayCommand.On, self.drive_id, self.part_no)

    def relay_switch_off(self):
        transport.send_relay_command(RelayCommand.Off, self.drive_id, self.part_no)

class Status_menue():
    def __init__(self, id_device):
        self.menue_name = 'Просмотр статусов:\n' + '-' * 52 + '\n'
        self.dev_id = id_device

    def create_menue(self):
        return self.menue_name + str(self.dev_id)

class Card_info_menue:
    def __init__(self):
        self.menue_name = 'Информация по карте:\n' + '-' * 52 +'\n'
        self.description = 'Давай код карты в hex-формате\n'
        self.pers_info = ''
        self.device_info = ''


    def create_menue(self):
        return self.menue_name + self.description + self.pers_info + self.device_info

    def get_person_info(self, cardcode):
        with sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.hallookup.dat",
                             detect_types=sqlite3.PARSE_DECLTYPES) as conn_lookup, \
                sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.dictionary.dat") as conn_dict:
            cursor_lookup = conn_lookup.cursor()
            cursor_dict = conn_dict.cursor()
            cursor_lookup.execute("""SELECT pers_id
                                     FROM person
                                     WHERE cardcode = :card""", {'card': cardcode})
            result_lookup = cursor_lookup.fetchone()

            if result_lookup:
                pers_id = result_lookup[0]
                cursor_dict.execute("""SELECT val
                                       FROM dictionary
                                       WHERE obj_id = :persid""", {'persid': pers_id})
                result_dict = cursor_dict.fetchone()
                self.pers_info = 'Карта выдана: {}\n'.format(result_dict[0])
                Card_info_menue.create_menue()
            else:
                self.pers_info = 'Совпадений не найдено\n'
                Card_info_menue.create_menue()

    def get_device_info(self, cardcode):
        with sqlite3.connect("C:/ProgramData/MDO/ParsecNET 3/parsec3.halconfig.dat") as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT channel_name, dev_addr, dev_model 
                              FROM cfg_device 
                              WHERE dev_id IN (SELECT dev_id 
                                                FROM cfg_user 
                                                WHERE cardcode = :card)""", {"card": cardcode})
            results = cursor.fetchall()

            if results:
                for channel, addres, device in results:
                    self.device_info = 'Канал: %s\n    Адрес: %s\n    Контроллер: %s\n' % (channel, addres, device)
                    Card_info_menue.create_menue()
            else:
                self.device_info = 'В базе данных указанной карты нет\n'
                Card_info_menue.create_menue()


about = 'Долгая история о том, как тестировщики учатся программировать'
