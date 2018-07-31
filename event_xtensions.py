from CommonEnums import ParamKey, ParamType
from Event_old import Event
from EventItem import EventItem


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


def operator_id_get(self):
    found = self.find_items(ParamKey.pkOperator, ParamType.ptGuid)
    return found[0].data if len(found) > 0 else None


def operator_id_set(self, value):
    found = self.find_items(ParamKey.pkOperator, ParamType.ptGuid)
    if len(found) == 0:
        self.items.add(EventItem.create(ParamKey.pkOperator, ParamType.ptGuid, value))
    else:
        found[0].data = value


Event.operator_ie = property(operator_id_get, operator_id_set)
