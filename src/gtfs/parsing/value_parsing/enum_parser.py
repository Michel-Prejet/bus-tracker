from gtfs.domain.enums.route_types import RouteType
from gtfs.domain.enums.service_pattern_override_type import ServicePatternOverrideType
from gtfs.exceptions.value_parsing_error import ValueParsingError
from gtfs.parsing.value_parsing.primitive_parser import parse_integer


def parse_route_type(raw: str) -> RouteType:
    """
    Throws an exception if the given string is not an integer corresponding to
    a valid RouteType; otherwise returns a RouteType object.
    """
    try:
        return RouteType(parse_integer(raw))
    except ValueError as e:
        raise ValueParsingError from e

def parse_override_type(raw: str) -> ServicePatternOverrideType:
    """
    Throws an exception if the given string is not an integer corresponding to
    a valid ServicePatternOverrideType; otherwise returns a
    ServicePatternOverrideType object.
    """
    try:
        return ServicePatternOverrideType(parse_integer(raw))
    except ValueError as e:
        raise ValueParsingError from e
