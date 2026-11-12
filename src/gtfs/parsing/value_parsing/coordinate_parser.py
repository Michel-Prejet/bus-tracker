from gtfs.constants.gtfs_constants import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.parsing.value_parsing.primitive_parser import parse_float


def parse_latitude(raw: str) -> float:
    """
    Throws an exception if the given string is not a floating-point value
    in the interval [-90, 90]; otherwise returns the value as a float.
    """
    latitude = parse_float(raw)

    if not (MIN_LATITUDE <= latitude <= MAX_LATITUDE):
        raise ValueParsingError

    return latitude

def parse_longitude(raw: str) -> float:
    """
    Throws an exception if the given string is not a floating-point value
    in the interval [-180, 180]; otherwise returns the value as a float.
    """
    longitude = parse_float(raw)

    if not (MIN_LONGITUDE <= longitude <= MAX_LONGITUDE):
        raise ValueParsingError

    return longitude