from gtfs.domain.enums.route_types import RouteType
from gtfs.domain.route import Route
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from gtfs.validation.domain.general_validator import validate_and_parse_url, validate_and_parse_colour, \
    validate_and_parse_numeric_str, validate_and_parse_optional_str
from utilities.invariant_helper import require_not_none, require_state
from gtfs.exceptions.domain_validation.route_error import EmptyRouteIdError, InvalidRouteTypeError, \
    InvalidRouteUrlError, \
    InvalidRouteBackgroundColourError, InvalidRouteTextColourError, InvalidRouteSortOrderError, MissingRouteNameError, \
    DuplicateRouteIdError


def validate_route_collection(routes: list[Route]) -> None:
    """
    Throws an exception if the same route ID appears more than once in the
    given list of routes.
    """
    require_not_none(route_list=routes)
    for route in routes:
        require_not_none(route_in_list=route)

    ids_seen = set()

    for route in routes:
        if route.id in ids_seen:
            raise DuplicateRouteIdError(route.id)
        ids_seen.add(route.id)

def validate_route_attribute_combination(short_name: str | None,
                                         long_name: str | None,
                                         row_num: int) -> None:
    """
    Throws an exception if both of the given route names are None.
    """
    require_not_none(row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    if short_name is None and long_name is None:
        raise MissingRouteNameError(row_num)

def validate_and_parse_route_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace.
    Otherwise, the trimmed string is returned.
    """
    require_not_none(raw_route_id=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    raw = raw.strip()

    if len(raw) == 0:
        raise EmptyRouteIdError(row_num)

    return raw

def validate_and_parse_route_name(raw: str, row_num: int) -> str:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    require_not_none(raw_short_name=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    return validate_and_parse_optional_str(raw)

def validate_and_parse_route_type(raw: str, row_num: int) -> RouteType:
    """
    Throws an exception if the given string is not an integer corresponding
    to a valid RouteType; otherwise, the corresponding RouteType object is
    returned.
    """
    require_not_none(raw_route_type=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    try:
        return RouteType(validate_and_parse_numeric_str(raw))
    except ValueError as e:
        raise InvalidRouteTypeError(row_num) from e

def validate_and_parse_route_url(raw: str, row_num: int) -> Url | None:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns the corresponding Url object.
    """
    require_not_none(raw_route_url=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    try:
        return validate_and_parse_url(raw)
    except ValueError as e:
        raise InvalidRouteUrlError(row_num) from e

def validate_and_parse_route_background_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    require_not_none(raw_route_background_colour=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise InvalidRouteBackgroundColourError(row_num) from e

def validate_and_parse_route_text_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    require_not_none(raw_route_text_colour=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise InvalidRouteTextColourError(row_num) from e

def validate_and_parse_route_sort_order(raw: str, row_num: int) -> int | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the corresponding integer or throws an exception if the given string
    is not a non-negative integer.
    """
    require_not_none(raw_route_sort_order=raw, row_number=row_num)
    require_state(row_num >= 0, "Row number should not be negative.")

    raw = raw.strip()

    if not raw:
        return None

    try:
        sort_order = validate_and_parse_numeric_str(raw)
    except ValueError as e:
        raise InvalidRouteSortOrderError(row_num) from e

    if sort_order < 0:
        raise InvalidRouteSortOrderError(row_num)

    return sort_order
