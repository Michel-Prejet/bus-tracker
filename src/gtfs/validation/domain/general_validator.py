import validators
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from gtfs.gtfs_constants import HEX_COLOUR_LENGTH
from utilities.invariant_helper import require_not_none, require_state
from utilities.is_hex import is_hex


def validate_and_parse_optional_str(raw: str) -> str | None:
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
    require_not_none(raw_url=raw)

    url = validate_and_parse_optional_str(raw)

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
    require_not_none(raw_background_colour=raw)

    colour = validate_and_parse_optional_str(raw)

    if colour is None:
        return None

    if len(colour) != HEX_COLOUR_LENGTH or not is_hex(colour):
        raise ValueError

    return Colour(colour)

def validate_and_parse_numeric_str(raw: str) -> int:
    """
    Throws an exception if the given string does not correspond to a valid
    GTFS integer value; otherwise returns the value as an integer.
    """
    require_not_none(numeric_string=raw)

    raw = raw.strip()

    digits = raw[1:] if raw.startswith("-") else raw

    if not digits.isascii() or not digits.isdecimal():
        raise ValueError

    return int(raw)

