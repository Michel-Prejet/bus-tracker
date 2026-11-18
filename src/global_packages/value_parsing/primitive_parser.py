from math import isfinite
from global_packages.exceptions.value_parsing_error import ValueParsingError


def parse_string(raw: str) -> str:
    """
    Returns the trimmed string.
    """
    return raw.strip()

def parse_integer(raw: str) -> int:
    """
    Throws an exception if the given string is not a valid GTFS integer;
    otherwise returns the value as an integer.
    """
    raw = raw.strip()

    digits = raw[1:] if raw.startswith("-") else raw

    if not digits.isascii() or not digits.isdecimal():
        raise ValueParsingError

    try:
        return int(raw)
    except ValueError as e:
        raise ValueParsingError from e

def parse_float(raw: str) -> float:
    """
    Throws an exception if the given string is not a valid GTFS floating-point
    number; otherwise returns the value as a float.
    """
    raw = raw.strip()

    digits = raw[1:] if raw.startswith("-") else raw
    digits = digits.replace(".", "", 1)

    if not digits.isascii() or not digits.isdecimal():
        raise ValueParsingError

    value = float(raw)

    if not isfinite(value):
        raise ValueParsingError

    return value

def parse_bool(raw: str) -> bool:
    """
    Returns False if the given string is "0" or "false", True if it is "1" or
    "true", and throws an exception otherwise.
    """
    raw = raw.strip().lower()

    if raw == "0" or raw == "false":
        return False
    if raw == "1" or raw == "true":
        return True

    raise ValueParsingError