from enum import Enum, unique


@unique
class TaskStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
