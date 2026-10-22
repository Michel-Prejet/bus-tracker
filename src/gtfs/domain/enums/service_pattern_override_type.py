from enum import IntEnum


class ServicePatternOverrideType(IntEnum):
    """
    Represents different types of instructions for modifying service
    patterns on a specific date.
    """
    ADD = 1
    REMOVE = 2