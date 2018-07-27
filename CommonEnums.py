import enum

class ComponentMask(enum.Enum):
    DoorBit = 0
    TwoReaderBit = 1
    APBBit = 2
    ComplexScheduleBit = 3
    UsedAsDesktopReaderBit = 4
    AlarmAreaBit = 5
    VideoCameraBit = 6
    TurnstileBit = 7
    LightBit = 8
    DoNotUseScheduleBit = 9
    SoftwareControler = 10
    TextTarget = 11
    LicenseFree = 12
    Elevator = 13
    CountsPeopleInside = 14
    DoorWithAutoClose = 15
    DoNotUseInAPB = 16
    DisabledBit = 62
    DisabledByLicense = 63

class SourceType(enum.Enum):
    stErrRestore = 0
    stNC = 1
    stAC = 2
    stHardWareCommon = 3
    stUI = 4
    stAudit = 5
    stArgus = 6
    stVideo = 7
    stUmirs = 8
    stIntegral = 9
    stLast = 255

class CodeType(enum.Enum):
    # The type of user identifier
    ctParsecAccess = 0
    ctParsecGuard = 1
    ctArgusGuard = 2
    ctCarNumber = 3
    ctBioData = 4
    ctIntegralGuard = 5
    ctCotag = 6
    ctBosch = 7
    ctLast = 255

class Privileges(enum.Enum):
    canSoundOff = 0x0001
    canDoorArmDisarm = 0x0002
    canCrossLock = 0x0004
    canGetAlarm = 0x0008
    canAreaArm = 0x0010
    canAreaDisarm = 0x0020
    canCrossAPB = 0x0040
    canGuest = 0x0080
    canPrivileges = 0x0100
    canNotExit = 0x0200
    canExitOffTime = 0x0400
    canOperator = 0x0800
    canNeverUseThisBit = 0x1000
    canUnlock4LongTime = 0x2000
    canIgnorePassCounter = 0x4000
    canNotEnter = 0x8000
    canCanConfigure = 0x010000
    canNotPassWithoutLead = 0x020000
    canStrictCheckReturnTime = 0x040000

class MessageType(enum.Enum):
    #for transactions, match category
    mtEvent = 0
    mtState = 1
    mtResponse = 2
    #for commands
    mtCommand = 5
    mtDriverCommand = 6
    mtInvoke = 7

class ParamKey(enum.Enum):
    pkAny = 0
    pkUser = 2              # user
    pkCommandData = 4
    pkComponent = 5         # component
    pkState = 6
    pkPart = 7              # part
    pkDevice = 8
    pkTransportAddressee = 9
    pkTransportSenderPath = 10
    pkEventMask = 11
    pkWorkstation = 12      # workstation
    pkOperator = 13         # operator
    pkObject = 14           # task, schedule, access group and other audit object (and not only audit)
    pkHierarchyRoots = 15   # message security
    pkTaskID = 16           # task identifier
    pkViewerID = 17         # identificator of plugin capable to view this event
    pkServerID = 18         # server aplied to this event
    pkTime = 19             # time associated with event
    pkImage = 20            # image associated with event
    pkCarPlate = 21         # detected license plate number
    pkImageArea = 22        # area of the event on the associated image
    pkOperatorComments = 23 # operator comments for audit events
    pkChannelType = 24      # computer channel type
    pkSoundID = 25          # sound guid
    pkLinkedEventID = 26
    pkTextMessage = 27
    pkTextSubject = 28

class DataBit(enum.IntFlag):
    dbUndefined = 0
    dbComponent = 1
    dbWorkStation = 2
    dbOperator = 4
    dbUser = 8
    dbPart = 16
    dbObject = 32
    dbLast = 256

class ParamType(enum.Enum):
    ptAny = 0
    ptDword = 1
    ptDouble = 2
    ptI64 = 3
    ptGuid = 4
    ptChar = 5
    ptTime = 6
    ptByteBuffer = 7
    ptBinary = 8
    ptRect = 9               # 4x4int
    ptLast = None

class Method(enum.Enum):
    miAddUser = 0
    miSetUser = 1
    miDelUser = 2
    miSendCommand = 3
    miSendCommandWithData = 4
    miDelSchedule = 5
    miSetSchedule = 6
    miSetConfig = 7
    #miSetAPBStorage = 8
    miSyncronizeDateTime = 9
    miGetComponentState = 0x0A
    miResetAlarm = 0x0B
    miResetDevice = 0x0C
    miRequestState = 0x0D
    miReadConfig = 0x0E
    miRescanDevices = 0x0F
    miNewSubscriber = 0x10
    miUpdateSchedules = 0x11
    miClearAPBBit = 0x15            # Clear APB bit for user or for all users in device
    miBackupDatabase = 0x16         # Backup parsec database
    miDelDevice = 0x18
    miUpdateComponent = 0x22
    miUpdatePart = 0x23
    miRequestConfig = 0x24          # Get configuration from device
    miCompleteMethod = 0x25         # After method complete
    miUpdateChannel = 0x26          # Update channel info
    miHalControl = 0x27
    miHalEnableUpdate = 0x28        # Replication client update notification
    miSetGuard = 0x29
    miClearGuard = 0x30
    miDetachDevice = 0x31
    miUpdateDeviceDB = 0x32         # Update whole device db, use DBConfig* as data
    miLast = None

class TaskMethods(enum.Enum):
    miResumeTask = 1                # Resume paused task. Called as a command from UI or from another task
    miPauseTask = 2                 # Pause scheduled task. Called as a command from UI or from another task
    miRunTask = 3                   # Pause scheduled task. Called as a command from taskeditor UI or from monitor
    miGetTaskState = 4
    miNewTaskSubscriber = 5
    miTextMessage = 6
    miTaskLast = None

class VideoMethods(enum.Enum):
    miStartRecord = 1
    miStopRecord = 2
    miArmCamera = 3
    miDisarmCamera = 4
    miReconnectCamera = 5
    miMarkRecord = 6
    miTakeSnapshot = 7
    miTakeSnapshotHistory = 8
    miVideoLast = None

class ErrorCodes(enum.Enum):
    errNotImplemented = 1
    errPortNotFound = 2
    errDeviceNotFound = 3
    errDeviceNotAvailable = 0x010004
    errBadPortModel = 5
    errBadDeviceModel = 0x010006
    errNoSink = 7
    errIncorrectFormat = 8
    errBadParameters = 9
    errEmptyMessage = 10
    errIOError = 11
    errDeviceNoSpace = 0x01000c
    errIncompatibleSchedule = 0x01000d
    errPortNotAvailable = 0x02000e
    errWorkstationDisconnected = 0x02000f
    errUDPGateDisconnected = 0x020010
    errLast = 128
    ecWorkstationConnected = errLast + 1 + 0x020000
    ecUDPGateConnected = errLast + 2 + 0x020000
    ecDeviceAvailable = errLast + 3 + 0x010000
    ecPortAvailable = errLast + 4 + 0x020000
    ecScanHardwareStarted = errLast + 5 + 0x20000
    ecScanHardwareStopped = errLast + 6 + 0x20000
    ecWorkstationAddressChanged = errLast + 8 + 0x20000

class EventCodes(enum.Enum):
    ecIdentity = 0x0301
    ecState = 0x0302
    ecCardOnDevice = 0x0303
    ecConfigurationLoaded = 0x0304
    ecCardOnDeviceIn = 0x0305
    ecCardOnDeviceOut = 0x0306

class MessageCategory(enum.Enum):
    Status = (1 << 0)
    AlarmControl = (1 << 1)
    Instant = (1 << 2)
    Trouble = (1 << 3)
    Alarm = (1 << 4)
    GuardFire = (1 << 5)
    NoAccess = (1 << 6)
    UnauthorizedAccess = (1 << 7)
    AuthorizedEnter = (1 << 8)
    AuthorizedExit = (1 << 9)
    AccessGranted = (1 << 10)
    AccessControl = (1 << 11)
    AuditActions = (1 << 12)
    AuditEditing = (1 << 13)
    VideoEvents = (1 << 14)
    HardwareDiagnostics = (1 << 15)
    NoAccessEnter = (1 << 16)
    NoAccessExit = (1 << 17)

class DevicePartType(enum.Enum):
    DeviceComponent = 0
    SensorPart = 1
    DrivePart = 2
    CommPart = 3
    AreaComponent = 4
    DoorComponent = 5
    KeyboardPart = 6
    GroupComponent = 7
    SystemPart = 8

class DevicePartFlagBit(enum.Enum):
    Disabled = 63
    Managed = 62
    ElevatorFloor = 1

class StateBits(enum.Enum):
    InactiveState = 31
    UndefinedState = 30
    DisabledState = 28
    AlarmState = 27
    DirtyState = 26
    DisabledByLicenseState = 25

