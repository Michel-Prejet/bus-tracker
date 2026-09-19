from enum import IntEnum


class RouteType(IntEnum):
    """
    Represents different route types as defined in the Official GTFS
    Schedule Reference.
    """

    TRAM = 0
    SUBWAY = 1
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    AERIAL_LIFT = 6
    FUNICULAR = 7
    TROLLEYBUS = 11
    MONORAIL = 12