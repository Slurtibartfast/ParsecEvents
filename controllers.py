from enum import Enum


class SystemStateBits(Enum):
    InactiveState = 31,
    UndefinedState = 30,
    DisabledState = 28,
    AlarmState = 27,
    DirtyState = 26,
    DisabledByLicenseState = 25


class ControllerState:

    def __init__(self):
        self.Accumulator = OkFailure.Ok
        self.Power = (1 << 1),  # 0 - off, 1 - on(BoxState.PowerState 1 == off )
        self.Battery = (1 << 2),  # 0 - falure, 1 - ok(BoxState.Load 1 == falure )
    Case = (1 << 3),  # 0 - open, 1 - closed(BoxState.Tamper 1 == open )
    EnterSwitch = (1 << 4),  # 0 - off, 1 - on(Door_states.LockState)
    ExitSwitch = (1 << 5),  # 0 - off, 1 - on(Door_states.Rele2)
    AdditionalSwitch = (1 << 6),  # 0 - off, 1 - on(Door_states.Rele2)
    CardReceiverSwitch = (1 << 7),  # 0 - off, 1 - on ???
    AbsoluteBlock = (1 << 8),  # 0 - off, 1 - on(Door_states.AbsoluteBlock)
    RelativeBlock = (1 << 9),  # 0 - off, 1 - on(Door_states.RelativeBlock)
    EmergencyDoorOpen = (1 << 10),  # 0 - off, 1 - on(Door_states.Emergency)
    Guard = (1 << 11),  # 0 - off, 1 - on(Door_states.GuardOnOff)
    GuardSensor = (1 << 12),  # 0 - off, 1 - on(Door_states.GuardState)
    EnterSensor = (1 << 13),  # 0 - closed, 1 - open(Door_states.DCState)
    ExitSensor = (1 << 14),  # 0 - closed, 1 - open(Door_states.Unlock)

    Attention = (1 << 24),  # 0 - normal, 1 - require attention
        Disabled = False
        Inactive = False
        Undefined = False


class Door_states(Enum):
    Norm = 0,
    DCState = (1 << 0),
    LockState = (1 << 1),
    AbsoluteBlock = (1 << 2),
    RelativeBlock = (1 << 3),
    Emergency = (1 << 4),
    GuardOnOff = (1 << 5),
    GuardState = (1 << 6),
    Rele2 = (1 << 8),
    Unlock = (1 << 9),
    Full = Norm | DCState | LockState | AbsoluteBlock | RelativeBlock | Emergency | \
           GuardOnOff | GuardState | Rele2 | Unlock,
    Last = (1 << 31)


class OkFailure(Enum):
    Ok = 0
    Failure = 1


class OpenClosed(Enum):
    Closed = 0
    Opened = 1


class EnabledDisabled(Enum):
    Disabled = 0
    Enabled = 1

class OnOff

class States(Enum):
    Closed = 0,
    Opened = 1,
    Disabled = 0,
    Enabled = 1,
    SwitchedOn = 0,
    SwitchedOff = 1,
    GuardOn = 1,
    GuardOff = 0,


class Controller:
    def __init__(self):
        self.model = None
        self.addres = None
        self.id = None
        self.doc = None


class Nc_controller(Controller):
    def __init__(self):
        super().__init__()
        self.door_id = None
        self.box_id = None
        self.dop_relay_part_no = 33554433
        self.dop_relay1_part_no = 0
        self.parts = []
        self.commands = []


class nc100k(Nc_controller):
    def __init__(self):
        super().__init__()
        self.commands = []
