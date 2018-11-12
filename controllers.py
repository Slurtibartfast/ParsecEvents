from enum import Enum, IntFlag
from imaplib import Flags


class SystemStateBits(Enum):
    InactiveState = 31,
    UndefinedState = 30,
    DisabledState = 28,
    AlarmState = 27,
    DirtyState = 26,
    DisabledByLicenseState = 25


class OkFailure(Enum):
    Failure = 0
    Ok = 1


class OpenClosed(Enum):
    Closed = 0
    Opened = 1


class AttentionNorm(Enum):
    Normal = 0
    Attention = 1


class OnOff(Enum):
    Off = 0
    On = 1


class ActiveNorm(Enum):
    Normal = 0
    Active = 1


class StateFlags(IntFlag):
    Accumulator = 1 << 0


class ControllerState:
    def __init__(self):
        self.Accumulator = OkFailure.Ok
        self.Power = OnOff.On
        self.Battery = OkFailure
        self.Case = OpenClosed.Closed
        self.EnterSwitch = OnOff.Off
        self.ExitSwitch = OnOff.Off
        self.AdditionalSwitch = OnOff.Off
        self.CardReceiverSwitch = OnOff.Off
        self.AbsoluteBlock = OnOff.Off
        self.RelativeBlock = OnOff.Off
        self.EmergencyDoorOpen = OnOff.Off
        self.Guard = OnOff.Off
        self.GuardSensor = OnOff.Off
        self.EnterSensor = OpenClosed.Closed
        self.ExitSensor = OpenClosed.Closed
        self.Attention = AttentionNorm.Normal
        self.Disabled = False
        self.Inactive = False
        self.Undefined = False

    def initialize(self, state: int):
        self.Accumulator = OkFailure((state >> 0) & 1)  # (1 << 0) 0 - failure, 1 - ok
        # self.Accumulator = OkFailure(int(state & StateFlags.Accumulator == StateFlags.Accumulator))
        self.Power = OnOff((state >> 1) & 1)  # (1 << 1) 0 - off, 1 - on(BoxState.PowerState 1 == off )
        self.Battery = OkFailure((state >> 2) & 1)  # (1 << 2) 0 - failure, 1 - ok(BoxState.Load 1 == failure )
        self.Case = OpenClosed((state >> 3) & 1)  # (1 << 3) 0 - open, 1 - closed(BoxState.Tamper 1 == open )
        self.EnterSwitch = OnOff((state >> 4) & 1)  # (1 << 4) 0 - off, 1 - on(Door_states.LockState)
        self.ExitSwitch = OnOff((state >> 5) & 1)  # (1 << 5) 0 - off, 1 - on(Door_states.Rele2)
        self.AdditionalSwitch = OnOff((state >> 6) & 1)  # (1 << 6) 0 - off, 1 - on(Door_states.Rele2)
        self.CardReceiverSwitch = OnOff((state >> 7) & 1)  # (1 << 7) 0 - off, 1 - on ???
        self.AbsoluteBlock = OnOff((state >> 8) & 1)  # (1 << 8) 0 - off, 1 - on(Door_states.AbsoluteBlock)
        self.RelativeBlock = OnOff((state >> 9) & 1)  # (1 << 9) 0 - off, 1 - on(Door_states.RelativeBlock)
        self.EmergencyDoorOpen = OnOff((state >> 10) & 1)  # (1 << 10) 0 - off, 1 - on(Door_states.Emergency)
        self.Guard = OnOff((state >> 11) & 1)  # (1 << 11) 0 - off, 1 - on(Door_states.GuardOnOff)
        self.GuardSensor = OnOff((state >> 12) & 1)  # (1 << 12) 0 - off, 1 - on(Door_states.GuardState)
        self.EnterSensor = OpenClosed((state >> 13) & 1)  # (1 << 13) 0 - closed, 1 - open(Door_states.DCState)
        self.ExitSensor = OpenClosed((state >> 14) & 1)  # (1 << 14) 0 - closed, 1 - open(Door_states.Unlock)
        self.Attention = AttentionNorm((state >> 24) & 1)  # (1 << 24) 0 - normal, 1 - require attention


class Door_states:
    def __init__(self):
        self.DCState = ActiveNorm.Normal
        self.LockState = OnOff.Off
        self.AbsoluteBlock = OnOff.Off
        self.RelativeBlock = OnOff.Off
        self.Emergency = OnOff.Off
        self.GuardOnOff = OnOff.Off
        self.GuardState = ActiveNorm.Normal
        self.Rele2 = OnOff.Off

    def initialize(self, state):
        self.DCState = ActiveNorm((state >> 0) & 1)  # (1 << 0)
        self.LockState = OnOff((state >> 1) & 1)  # (1 << 1)
        self.AbsoluteBlock = OnOff((state >> 2) & 1)  # (1 << 2)
        self.RelativeBlock = OnOff((state >> 3) & 1)  # (1 << 3)
        self.Emergency = OnOff((state >> 4) & 1)  # (1 << 4)
        self.GuardOnOff = OnOff((state >> 5) & 1)  # (1 << 5)
        self.GuardState = ActiveNorm((state >> 6) & 1)  # (1 << 6)
        self.Rele2 = OnOff((state >> 8) & 1)  # (1 << 8)
        self.Unlock = OnOff((state >> 9) & 1)  # (1 << 9)


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
