from uuid import UUID

from constants import ParamKey, ParamType
from event import EventItem, Event

# add Event.workstation_id property
from local_db import Dictionary


def workstation_id_get(self) -> UUID:
    return self.get_item_data(ParamKey.pkWorkstation, ParamType.ptGuid, 0)


def workstation_id_set(self, value: UUID):
    self.set_item_data(ParamKey.pkWorkstation, ParamType.ptGuid, 0, value)


Event.workstation_id = property(workstation_id_get, workstation_id_set)


# ----------------------------------------

# add Event.operator_id property

def operator_id_get(self) -> UUID:
    return self.get_item_data(ParamKey.pkOperator, ParamType.ptGuid, 0)


def operator_id_set(self, value: UUID):
    self.set_item_data(ParamKey.pkOperator, ParamType.ptGuid, 0, value)


Event.operator_id = property(operator_id_get, operator_id_set)


# ----------------------------------------

# add Event.user_id property

def user_id_get(self) -> UUID:
    return self.get_item_data(ParamKey.pkUser, ParamType.ptGuid, 0)


def user_id_set(self, value: UUID):
    self.set_item_data(ParamKey.pkUser, ParamType.ptGuid, 0, value)


Event.user_id = property(user_id_get, user_id_set)


# -----------------------------------------

# add Event.card_code property

def card_code_get(self) -> str:
    return self.get_item_data(ParamKey.pkUser, ParamType.ptChar, 0)


def card_code_set(self, value: UUID):
    self.set_item_data(ParamKey.pkUser, ParamType.ptChar, 0, value)


Event.card_code = property(card_code_get, card_code_set)


# -----------------------------------------

# add Event.workstation_name property

def workstation_name_get(self) -> str:
    return Dictionary().get_object_name(self.workstation_id)


Event.workstation_name = property(workstation_name_get)


# -----------------------------------------

# add Event.operator_name property

def operator_name_get(self) -> str:
    return Dictionary().get_object_name(self.operator_id)


Event.operator_name = property(operator_name_get)


# -----------------------------------------

# add Event.name property

def name_get(self) -> str:
    return Dictionary().get_event_name(self.code)


Event.name = property(name_get)


# -----------------------------------------

# add Event.user_name property

def user_name_get(self) -> str:
    return Dictionary().get_object_name(self.user_id)


Event.user_name = property(user_name_get)


# -----------------------------------------

# add Event.operator_comments property

def get_string(self, key: ParamKey) -> str:
    short_comment = self.get_item_data(key, ParamType.ptChar, 0)
    if short_comment:
        return short_comment.encode('utf-8')
    else:
        long_comment_length = self.get_item_data(key, ParamType.ptDword, 0)
        if long_comment_length:
            long_comment = None
            instance = 0
            while long_comment_length > 0:
                long_comment_length -= 16
                instance += 1
                long_comment += self.get_item_data(ParamKey.pkOperatorComments, ParamType.ptByteBuffer, instance)
            return long_comment.encode('utf-8')


def set_string(self, key: ParamKey, value: str):
    str_len = len(value)
    # Почистить результат выполнения предыдущих запусков данной функции
    pass


Event.operator_comments = property(get_string, set_string)
