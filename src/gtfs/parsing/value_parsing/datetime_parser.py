from datetime import date, datetime, timedelta
from gtfs.constants.gtfs_constants import YYYYMMDD_DATE_LENGTH, HOURS_TOKEN_LENGTH_MINIMUM, MINUTES_TOKEN_LENGTH, \
    SECONDS_TOKEN_LENGTH, HHMMSS_TIME_NUM_TOKENS, MAX_MINUTES, MAX_SECONDS
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.parsing.value_parsing.primitive_parser import parse_integer


def parse_date(raw: str) -> date:
    """
    Throws an exception if the given string is not a valid date in YYYYMMDD
    format; returns a date object otherwise.
    """
    raw = raw.strip()

    if len(raw) != YYYYMMDD_DATE_LENGTH:
        raise ValueParsingError

    try:
        return datetime.strptime(raw, "%Y%m%d").date()
    except ValueError as e:
        raise ValueParsingError from e

def parse_time(raw: str) -> timedelta:
    """
    Throws an exception if the given string is not a valid time in HH:MM:SS
    format; otherwise returns a timedelta object.
    """
    raw = raw.strip()

    tokens = raw.split(":")
    if len(tokens) != HHMMSS_TIME_NUM_TOKENS:
        raise ValueParsingError
    hours_raw, minutes_raw, seconds_raw = tokens

    if (len(hours_raw) < HOURS_TOKEN_LENGTH_MINIMUM or
        len(minutes_raw) != MINUTES_TOKEN_LENGTH or
        len(seconds_raw) != SECONDS_TOKEN_LENGTH):
        raise ValueParsingError

    try:
        hours, minutes, seconds = map(parse_integer,
                                      [hours_raw, minutes_raw, seconds_raw])
    except ValueParsingError as e:
        raise ValueParsingError from e

    if (hours < 0 or minutes < 0 or seconds < 0 or
        minutes > MAX_MINUTES or seconds > MAX_SECONDS):
        raise ValueParsingError

    try:
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except OverflowError as e:
        raise ValueParsingError from e
