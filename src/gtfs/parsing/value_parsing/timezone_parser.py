from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from gtfs.exceptions.value_parsing_error import ValueParsingError


def parse_timezone(raw: str) -> ZoneInfo:
    """
    Throws an exception if the given string is not a valid IANA timezone;
    otherwise returns a ZoneInfo object.
    """
    raw = raw.strip()

    try:
        return ZoneInfo(raw)
    except (ZoneInfoNotFoundError, ValueError) as e:
        raise ValueParsingError from e