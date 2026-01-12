from datetime import date, time

from domain.Ride import Ride
from domain.validation.exceptions.RideError import (EmptyBlockNumberError, EmptyDestinationError, EmptyRouteError,
                                                    InvalidBlockNumberError, TrackingNumberDigitError,
                                                    TrackingNumberLengthError, InvalidDateError, InvalidTimeError)
from utilities.InvariantHelper import require_not_none

TRACKING_NUMBER_LENGTH = 3
SINGLE_DIGIT_HOUR_TIME_LENGTH = 4
CURR_DATE_KEYWORD = "today"

def validate_date(raw: str) -> date:
    """
    Validates a given date string and raises an exception if it is
    not in the form YYYY-MM-DD. Returns today's date if the string
    corresponds to the 'today' keyword. Removes all leading and trailing
    whitespace before validation.

    :param raw: the date string to validate.
    :return: the valid date object corresponding to `raw`.
    """
    require_not_none(raw, "Date should not be None.")

    raw = raw.strip()

    if raw.lower() == CURR_DATE_KEYWORD:
        return date.today()

    try:
        return date.fromisoformat(raw)
    except ValueError:
        raise InvalidDateError

def validate_boarding_time(raw: str) -> time:
    """
    Validates a given time string and raises an exception if it is
    not in the form HH:MM or H:MM. Removes all leading and trailing
    whitespace before validation.

    :param raw: the time string to validate.
    :return: the valid time object corresponding to `raw`.
    """
    require_not_none(raw, "Boarding time should not be None.")

    raw = raw.strip()

    if len(raw) == SINGLE_DIGIT_HOUR_TIME_LENGTH:
        raw = "0" + raw

    try:
        return time.fromisoformat(raw)
    except ValueError:
        raise InvalidTimeError

def validate_route(raw: str) -> str:
    """
    Validates a given route and raises an exception if it is
    empty. Removes all leading and trailing whitespace before
    validation.

    :param raw: the route to validate.
    :return: the validated route, with all leading/trailing
    whitespace removed.
    """
    require_not_none(raw, "Route should not be None.")

    raw = raw.strip()

    if not raw:
        raise EmptyRouteError()

    return raw

def validate_tracking_number(raw: str) -> str:
    """
    Validates a given tracking number and raises an exception
    if it is not a number or not of length 3. Removes all leading
    and trailing whitespace before validation.

    :param raw: the tracking number to validate.
    :return: the validated tracking number, with all leading/trailing
    whitespace removed.
    """
    require_not_none(raw, "Tracking number should not be None.")

    raw = raw.strip()

    if not raw.isdigit():
        raise TrackingNumberDigitError()

    if len(raw) != Ride.TRACKING_NUMBER_LENGTH:
        raise TrackingNumberLengthError()

    return raw

def validate_destination(raw: str) -> str:
    """
    Validates a given destination and raises an exception if it is
    empty. Removes all leading and trailing whitespace before
    validation.

    :param raw: the destination to validate.
    :return: the validated destination, with all leading/trailing
    whitespace removed.
    """
    require_not_none(raw, "Destination should not be None.")

    raw = raw.strip()

    if not raw:
        raise EmptyDestinationError()

    return raw

def validate_block_number(raw: str) -> str:
    """
    Validates a given block number and raises an exception if it is
    invalid. To be valid, a block number cannot be empty, and must
    only contain digits, except for exactly one dash not at the start
    or the end of the string. Removes all leading and trailing whitespace
    before validation.

    :param raw: the block number to validate.
    :return: the validated block number, with all leading/trailing
    whitespace removed.
    """
    require_not_none(raw, "Block number should not be None.")

    raw = raw.strip()

    if not raw:
        raise EmptyBlockNumberError()

    for char in raw:
        if not char.isdigit() and char != "-":
            raise InvalidBlockNumberError()

    if raw.count("-") != 1:
        raise InvalidBlockNumberError()

    if not 0 < raw.find("-") < len(raw) - 1:
        raise InvalidBlockNumberError()

    return raw



