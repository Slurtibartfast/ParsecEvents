import json
import uuid
import sqlite3

sqlite3.register_converter('uniqueidentifier', lambda b: uuid.UUID(bytes_le=b))
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)


class MainMenue:
    def __init__(self):
        self.menue_name = '*********Главное меню**********\n' + '*' * 35 + '\n'
        self.description = ' ' * 22 + 'Аллоха!\nТы попал в меню vk-бота Paresc\n(Created by yvinogradov@mdo.ru)\n' \
                                 'Давай же начнем работу. Итак, перед тобой меню, \
                        выбирай пункт который тебе интересен и отправляй мне его номер:\n'
        self.items = ['1⃣ Контроллеры\n']
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
        self.description = 'Выберете действие:\n'
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
        pass

    def door_close(self):
        pass

    def door_relative_block_on(self):
        pass

    def door_relativ_block_off(self):
        pass

    def door_absolute_block_on(self):
        pass

    def door_absolute_block_off(self):
        pass

    def door_guard_on(self):
        pass

    def door_guard_off(self):
        pass

    def door_open_enter(self):
        pass

    def door_open_exit(self):
        pass

    def door_apb_clear(self):
        pass



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
        pass

    def relay_switch_off(self):
        pass

class Status_menue():
    def __init__(self, id_device):
        self.menue_name = 'Просмотр статусов:\n' + '-' * 52 + '\n'
        self.dev_id = id_device

    def create_menue(self):
        return self.menue_name + str(self.dev_id)

# test = Door_command_menue('5D20F328-473E-4024-BBFA-DC1216FB513B')
# test.get_door_id(test.dev_id)
#
# testRelay = Relay_command_menue('5D20F328-473E-4024-BBFA-DC1216FB513B')
# testRelay.get_drive_id(testRelay.dev_id)