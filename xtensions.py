from uuid import UUID

from constants import ParamKey, ParamType
from event import EventItem, Event

# add UUID.empty() to represent empty UUID

_uuid_empty = UUID(bytes_le=bytes(16))


def uuid_empty():
    return _uuid_empty


UUID.empty = uuid_empty


# ----------------------------------------

# add Event.workstation_id property

def workstation_id_get(self):
    found = self.find_items(ParamKey.pkWorkstation, ParamType.ptGuid)
    return found[0].data if len(found) > 0 else None


def workstation_id_set(self, value):
    found = self.find_items(ParamKey.pkWorkstation, ParamType.ptGuid)
    if len(found) == 0:
        self.items.add(EventItem.create(ParamKey.pkWorkstation, ParamType.ptGuid, value))
    else:
        found[0].data = value


Event.workstation_id = property(workstation_id_get, workstation_id_set)


# ----------------------------------------

# add Event.operator_id property

def operator_id_get(self):
    found = self.find_items(ParamKey.pkOperator, ParamType.ptGuid)
    return found[0].data if len(found) > 0 else None


def operator_id_set(self, value):
    found = self.find_items(ParamKey.pkOperator, ParamType.ptGuid)
    if len(found) == 0:
        self.items.add(EventItem.create(ParamKey.pkOperator, ParamType.ptGuid, value))
    else:
        found[0].data = value


Event.operator_id = property(operator_id_get, operator_id_set)

# ----------------------------------------

# add Event.user_id property

def user_id_get(self):
    found = self.find_items(ParamKey.pkUser, ParamType.ptGuid)
    return found[0].data if len(found) > 0 else None

def user_id_set(self, value):
    found = self.find_items(ParamKey.pkUser, ParamType.ptGuid)
    if len(found) == 0:
        self.items.add(EventItem.create(ParamKey.pkUser, ParamType.ptGuid, value))
    else:
        found[0].data = value

Event.user_id = property(user_id_get, user_id_set)

#-----------------------------------------