from enum import Enum


class NumTransfers(Enum):
    """
    Represents the number of transfers associated with a fare product.
    """

    NONE = 0
    ONE = 1
    TWO = 2
    UNLIMITED = 3