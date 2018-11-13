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

def operator_comments_get(self) -> str:
    return self.get_string(ParamKey.pkOperatorComments)


def operator_comments_set(self, value: str):
    self.set_string(ParamKey.pkOperatorComments, value)


Event.operator_comments = property(operator_comments_get, operator_comments_set)
