from enum import Enum


class ServicePatternOverrideType(Enum):
    """
    Represents different types of instructions for modifying service
    patterns on a specific date.
    """
    ADD = 1
    REMOVE = 2