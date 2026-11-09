from gtfs.constants.csv_column_headers.route_headers import ROUTE_ID_COL_HEADER, ROUTE_TYPE_COL_HEADER, \
    ROUTE_URL_COL_HEADER, ROUTE_BACKGROUND_COLOUR_COL_HEADER, ROUTE_TEXT_COLOUR_COL_HEADER, ROUTE_SORT_ORDER_COL_HEADER
from gtfs.domain.enums.route_types import RouteType
from gtfs.domain.route import Route
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.constants.gtfs_constants import ROUTES_FILE_NAME
from gtfs.exceptions.gtfs_row_error import GTFSInstanceError, GTFSAttributeError
from gtfs.validation.general_validator import validate_and_parse_url, validate_and_parse_colour, \
    validate_and_parse_integer_str, parse_optional_str, validate_and_parse_nonempty_str, \
    assert_that_elements_are_unique


def validate_route_collection(routes: list[Route]) -> None:
    """
    Throws an exception if the same route ID appears more than once in the
    given list of routes.
    """
    try:
        assert_that_elements_are_unique([route.id for route in routes])
    except ValueError as e:
        raise GTFSCollectionError(
            file_name=ROUTES_FILE_NAME,
            names_of_columns_with_violated_restrictions=[ROUTE_ID_COL_HEADER]
        ) from e

def validate_route_attribute_combination(short_name: str | None,
                                         long_name: str | None,
                                         row: str,
                                         row_num: int) -> None:
    """
    Throws an exception if both of the given route names are None.
    """
    if short_name is None and long_name is None:
        raise GTFSInstanceError(
            file_name=ROUTES_FILE_NAME,
            row=row,
            row_num=row_num
        )

def validate_and_parse_route_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace.
    Otherwise, the trimmed string is returned.
    """
    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_route_name(raw: str, row_num: int) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    return parse_optional_str(raw)

def validate_and_parse_route_type(raw: str, row_num: int) -> RouteType:
    """
    Throws an exception if the given string is not an integer corresponding
    to a valid RouteType; otherwise, the corresponding RouteType object is
    returned.
    """
    try:
        return RouteType(validate_and_parse_integer_str(raw))
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_TYPE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_route_url(raw: str, row_num: int) -> Url | None:
    """
    Throws an exception if the given string is not a valid URL; otherwise
    returns the corresponding Url object.
    """
    try:
        return validate_and_parse_url(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_URL_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_route_background_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_BACKGROUND_COLOUR_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_route_text_colour(raw: str, row_num: int) -> Colour | None:
    """
    Returns None if the given string is empty or only whitespace. Otherwise,
    returns the corresponding Colour object, or throws an exception if the
    given string is not a 6-character hexadecimal string.
    """
    try:
        return validate_and_parse_colour(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_TEXT_COLOUR_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_route_sort_order(raw: str, row_num: int) -> int | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the corresponding integer or throws an exception if the given string
    is not a non-negative integer.
    """
    raw = raw.strip()

    if not raw:
        return None

    try:
        sort_order = validate_and_parse_integer_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_SORT_ORDER_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    if sort_order < 0:
        raise GTFSAttributeError(
            file_name=ROUTES_FILE_NAME,
            column_name=ROUTE_SORT_ORDER_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        )

    return sort_order
