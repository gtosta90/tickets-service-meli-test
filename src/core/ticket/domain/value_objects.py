from enum import IntEnum, StrEnum, unique

@unique
class Status(IntEnum):
    OPEN = 1
    IN_SERVICE = 2
    COMPLETED = 3
    CLOSED = 4

@unique
class Level(IntEnum):
    ISSUE_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4