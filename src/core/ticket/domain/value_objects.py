from enum import StrEnum, unique

@unique
class Status(StrEnum):
    OPEN = "OPEN"
    IN_SERVICE = "IN_SERVICE"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"

@unique
class Level(StrEnum):
    ISSUE_HIGH = "1"
    HIGH = "2"
    MEDIUM = "3"
    LOW = "4"