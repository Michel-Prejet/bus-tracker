from gtfs.constants.csv_column_headers.route_headers import ROUTE_ID_COL_HEADER, ROUTE_TYPE_COL_HEADER, \
    ROUTE_URL_COL_HEADER, ROUTE_BACKGROUND_COLOUR_COL_HEADER, ROUTE_TEXT_COLOUR_COL_HEADER, ROUTE_SORT_ORDER_COL_HEADER
from gtfs.domain.enums.route_types import RouteType
from gtfs.domain.route import Route
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_attribute_error import GTFSAttributeError
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_instance_error import GTFSInstanceError
from gtfs.constants.gtfs_constants import ROUTES_FILE_NAME
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_url, validate_and_parse_colour, \
    validate_and_parse_integer_str, validate_and_parse_optional_str
from invariant_helper import require_not_none, require_state


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
            raise GTFSCollectionError(ROUTES_FILE_NAME, [ROUTE_ID_COL_HEADER])
        ids_seen.add(route.id)

def validate_route_attribute_combination(short_name: str | None,
                                         long_name: str | None,
                                         row: str,
                                         row_num: int) -> None:
    """
    Throws an exception if both of the given route names are None.
    """
    require_not_none(row=row)
    require_valid_row_num(row_num)

    if short_name is None and long_name is None:
        raise GTFSInstanceError(ROUTES_FILE_NAME, row, row_num)

def validate_and_parse_route_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace.
    Otherwise, the trimmed string is returned.
    """
    require_not_none(raw_route_id=raw)
    require_valid_row_num(row_num)

    raw = raw.strip()

    if not raw:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_ID_COL_HEADER,
                                 row_num, raw)

    return raw

def validate_and_parse_route_name(raw: str, row_num: int) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    require_not_none(raw_short_name=raw)
    require_valid_row_num(row_num)

    return validate_and_parse_optional_str(raw)

def validate_and_parse_route_type(raw: str, row_num: int) -> RouteType:
    """
    Throws an exception if the given string is not an integer corresponding
    to a valid RouteType; otherwise, the corresponding RouteType object is
    returned.
    """
    require_not_none(raw_route_type=raw)
    require_valid_row_num(row_num)

    try:
        return RouteType(validate_and_parse_integer_str(raw))
    except ValueError as e:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_TYPE_COL_HEADER, row_num, raw) from e

def validate_and_parse_route_url(raw: str, row_num: int) -> Url | None:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns the corresponding Url object.
    """
    require_not_none(raw_route_url=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_url(raw)
    except ValueError as e:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_URL_COL_HEADER, row_num, raw) from e

def validate_and_parse_route_background_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    require_not_none(raw_route_background_colour=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_BACKGROUND_COLOUR_COL_HEADER,
                                 row_num, raw) from e

def validate_and_parse_route_text_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    require_not_none(raw_route_text_colour=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_TEXT_COLOUR_COL_HEADER,
                                 row_num, raw) from e

def validate_and_parse_route_sort_order(raw: str, row_num: int) -> int | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the corresponding integer or throws an exception if the given string
    is not a non-negative integer.
    """
    require_not_none(raw_route_sort_order=raw)
    require_valid_row_num(row_num)

    raw = raw.strip()

    if not raw:
        return None

    try:
        sort_order = validate_and_parse_integer_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_SORT_ORDER_COL_HEADER,
                                 row_num, raw) from e

    if sort_order < 0:
        raise GTFSAttributeError(ROUTES_FILE_NAME, ROUTE_SORT_ORDER_COL_HEADER,
                                 row_num, raw)

    return sort_order
