from datetime import date, datetime, timedelta
from math import isfinite
import validators
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from gtfs.constants.gtfs_constants import HEX_COLOUR_LENGTH, MIN_LATITUDE, MAX_LATITUDE, MAX_LONGITUDE, MIN_LONGITUDE, \
    RAW_TIMEDELTA_NUM_TOKENS, RAW_TIMEDELTA_MAX_MINUTES, RAW_TIMEDELTA_MAX_SECONDS
from gtfs.utilities.is_hex import is_hex


def assert_that_elements_are_unique(raw: list[str]) -> None:
    """
    Throws an exception if the same string appears more than once in the given
    list.
    """
    seen = set()

    for raw_str in raw:
        if raw_str in seen:
            raise ValueError
        seen.add(raw_str)

def validate_and_parse_nonempty_str(raw: str) -> str:
    """
    Throws an exception if the given string is empty or only whitespace;
    otherwise returns the trimmed string.
    """
    raw = raw.strip()

    if not raw:
        raise ValueError

    return raw

def parse_optional_str(raw: str) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    raw = raw.strip()

    if not raw:
        return None

    return raw

def validate_and_parse_url(raw: str) -> Url | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Url object, or throws an exception if the given
    string is not a valid URL.
    """
    url = parse_optional_str(raw)

    if url is None:
        return None

    if not validators.url(url):
        raise ValueError()

    return Url(url)

def validate_and_parse_colour(raw: str) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    colour = parse_optional_str(raw)

    if colour is None:
        return None

    if len(colour) != HEX_COLOUR_LENGTH or not is_hex(colour):
        raise ValueError

    return Colour(colour)

def validate_and_parse_integer_str(raw: str) -> int:
    """
    Throws an exception if the given string does not correspond to a valid
    GTFS integer value; otherwise returns the value as an integer.
    """
    raw = raw.strip()

    digits = raw[1:] if raw.startswith("-") else raw

    if not digits.isascii() or not digits.isdecimal():
        raise ValueError

    return int(raw)

def validate_and_parse_float_str(raw: str) -> float:
    """
    Throws an exception if the given string does not correspond to a valid
    GTFS floating-point value; otherwise returns the value as a float.
    """
    raw = raw.strip()

    digits = raw[1:] if raw.startswith("-") else raw
    digits = digits.replace(".", "", 1)

    if not digits.isascii() or not digits.isdecimal():
        raise ValueError

    value = float(raw)

    if not isfinite(value):
        raise ValueError

    return value

def validate_and_parse_boolean_str(raw: str) -> bool:
    """
    Throws the exception if the given string is not "0" or "1"; returns the
    corresponding boolean otherwise.
    """
    raw = raw.strip()

    if raw == "0":
        return False
    elif raw == "1":
        return True
    else:
        raise ValueError

def validate_and_parse_latitude(raw: str) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -90 and 90 (inclusive); returns a float otherwise.
    """
    latitude = validate_and_parse_float_str(raw)

    if not (MIN_LATITUDE <= latitude <= MAX_LATITUDE):
        raise ValueError

    return latitude

def validate_and_parse_longitude(raw: str) -> float:
    """
    Throws an exception if the given string is not a floating-point value between
    -180 and 180 (inclusive); returns a float otherwise.
    """
    longitude = validate_and_parse_float_str(raw)

    if not (MIN_LONGITUDE <= longitude <= MAX_LONGITUDE):
        raise ValueError

    return longitude

def validate_and_parse_date(raw: str) -> date:
    """
    Throws an exception if the given string is not a valid date in
    YYYYMMDD format; returns a date object otherwise.
    """
    DATE_LENGTH = 8

    raw = raw.strip()

    if len(raw) != DATE_LENGTH:
        raise ValueError

    return datetime.strptime(raw, "%Y%m%d").date()

def validate_and_parse_time(raw: str) -> timedelta:
    """
    Throws an exception if the given string is not a valid time in HH:MM:SS
    format; otherwise returns a timedelta object.
    """
    tokens = raw.split(":")
    if len(tokens) != RAW_TIMEDELTA_NUM_TOKENS:
        raise ValueError

    hours, minutes, seconds = map(validate_and_parse_integer_str, tokens)
    if (hours < 0 or minutes < 0 or seconds < 0 or
            minutes > RAW_TIMEDELTA_MAX_MINUTES or
            seconds > RAW_TIMEDELTA_MAX_SECONDS):
        raise ValueError

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)








