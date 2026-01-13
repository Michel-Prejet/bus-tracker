from enum import Enum
from datetime import date, time

from domain.RideList import RideList
from logic.exceptions.RideManagerError import DateRangeError, RideFilterError
from utilities.InvariantHelper import require_not_none

def filter_by_date(ride_list: RideList, start: date, end: date) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` that
    occurred in the given date range.

    :param ride_list: the ride list to filter (not mutated).
    :param start: the start of the date range by which to filter (inclusive).
    :param end: the end of the date range by which to filter (inclusive).
    :return: a ride list containing all rides in `ride_list` that occurred
    in the given date range.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(start, "Start date should not be None.")
    require_not_none(end, "End date should not be None.")

    if start > end:
        raise DateRangeError()

    return _filter_ride_list(ride_list,
                             lambda r: start <= r.ride_date <= end)

def filter_by_time(ride_list: RideList, start: time, end: time) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` that
    occurred in the given time range (across all dates). Works for time
    ranges that wrap around midnight.

    :param ride_list: the ride list to filter (not mutated).
    :param start: the start of the time range by which to filter (inclusive).
    :param end: the end of the time range by which to filter (inclusive).
    :return: a ride list containing all rides in `ride_list` that occurred
    in the time date range.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(start, "Start time should not be None.")
    require_not_none(end, "End time should not be None.")

    if start > end:
        filterer = lambda r: start <= r.boarding_time or r.boarding_time <= end
    else:
        filterer = lambda r: start <= r.boarding_time <= end

    return _filter_ride_list(ride_list, filterer)

def filter_by_route(ride_list: RideList, route: str) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` with
    a given route.

    :param ride_list: the ride list to filter (not mutated).
    :param route: the route by which to filter.
    :return: a ride list containing all rides in `ride_list` with the
    given route.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(route, "Route should not be None.")

    return _filter_ride_list(ride_list,
                             lambda r: r.route.casefold() == route.strip().casefold())

def filter_by_tracking_number(ride_list: RideList, tracking_number: str) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` with
    a given block number.

    :param ride_list: the ride list to filter (not mutated).
    :param tracking_number: the tracking number by which to filter.
    :return: a ride list containing all rides in `ride_list` with the given tracking
    number.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(tracking_number, "Tracking number should not be None.")

    return _filter_ride_list(ride_list,
                             lambda r: r.tracking_number.strip() == tracking_number.strip())

def filter_by_block_number(ride_list: RideList, block_number: str) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` with
    a given block number.

    :param ride_list: the ride list to filter (not mutated).
    :param block_number: the block number by which to filter.
    :return: a ride list containing all rides in `ride_list` with the given block
    number.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(block_number, "Block number should not be None.")

    return _filter_ride_list(ride_list,
                                 lambda r: r.block_number.strip() == block_number.strip())

def filter_by_destination(ride_list: RideList, destination: str) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list` with
    a given destination.

    :param ride_list: the ride list to filter (not mutated).
    :param destination: the destination by which to filter.
    :return: a ride list containing all rides in `ride_list` with the given
    destination.
    """
    require_not_none(ride_list, "Ride list should not be None.")
    require_not_none(destination, "Destination should not be None.")

    return _filter_ride_list(ride_list,
                                 lambda r: r.destination.casefold().strip() == destination.casefold().strip())

def _filter_ride_list(ride_list: RideList, filterer) -> RideList:
    """
    Creates a new ride list containing only the rides in `ride_list`
    that satisfy a given boolean function.

    :param ride_list: the ride list to filter (not mutated).
    :param filterer: the boolean function that determines whether
    a given ride (the only parameter) should be included in the result.
    :return: a ride list containing all rides in `ride_list` for which
    `filterer` returns `True`.
    """
    result: RideList = RideList()

    for curr in ride_list:
        if filterer(curr):
            result.add_ride(curr)

    return result

class RideFilter(Enum):
    """
    Represents different types of filters that can
    be applied to a ride list.
    """
    DATE = "date"
    TIME = "time"
    ROUTE = "route"
    TRACKING_NUMBER = "tracking_number"
    BLOCK_ID = "block_id"
    DESTINATION = "destination"
    NONE = "none"

    @classmethod
    def from_string(cls, raw: str) -> "RideFilter":
        for curr in cls:
            if curr.value().casefold().strip() == raw.casefold().strip():
                return curr

        raise RideFilterError()

