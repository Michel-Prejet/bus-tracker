from gtfs.constants.gtfs_constants import HEX_COLOUR_LENGTH
from gtfs.domain.values.colour import Colour
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.utilities.is_hex import is_hex


def parse_colour(raw: str) -> Colour:
    """
    Throws an exception if the given string does not consist of exactly six
    hexadecimal characters; returns a Colour object otherwise.
    """
    raw = raw.strip()

    if len(raw) != HEX_COLOUR_LENGTH or not is_hex(raw):
        raise ValueParsingError

    return Colour(raw)