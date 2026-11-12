from gtfs.constants.gtfs_constants import TRIP_DIRECTION_VALUES
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.parsing.value_parsing.primitive_parser import parse_integer


def parse_direction_id(raw: str) -> int:
    """
    Throws an exception if the given string is not an integer corresponding
    to a legal direction ID; otherwise returns the value as an integer.
    """
    try:
        direction_id = parse_integer(raw)

        if direction_id not in TRIP_DIRECTION_VALUES:
            raise ValueParsingError
    except ValueError as e:
        raise ValueParsingError from e

    return direction_id