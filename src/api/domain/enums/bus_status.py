from enum import Enum


class BusStatus(Enum):
    ACTIVE = "active"
    MISSING = "missing"
    RETIRED = "retired"