from gtfs.constants.csv_column_headers.trips_headers import TRIP_ID_COL_HEADER, TRIP_ROUTE_ID_COL_HEADER, \
    TRIP_SERVICE_ID_COL_HEADER, TRIP_SHAPE_ID_COL_HEADER, TRIP_BLOCK_ID_COL_HEADER, TRIP_DIRECTION_ID_COL_HEADER
from gtfs.constants.gtfs_constants import TRIPS_FILE_NAME, ROUTES_FILE_NAME, SERVICE_PATTERNS_FILE_NAME, \
    SHAPES_FILE_NAME, TRIP_DIRECTION_VALUES, WPG_BLOCK_ID_TOKEN_DELIMITER, WPG_BLOCK_ID_NUM_TOKENS
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.trip.trip import Trip
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError, GTFSForeignKeyError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, parse_optional_str, \
    validate_and_parse_integer_str, assert_that_elements_are_unique
from invariant_helper import require_not_none


def validate_trip_collection(trips: list[Trip]) -> None:
    """
    Throws an exception if two or more trips in the given list share the
    same trip ID.
    """
    require_not_none(trip_list=trips)
    for trip in trips:
        require_not_none(trip_in_list=trip)

    try:
        assert_that_elements_are_unique([trip.id for trip in trips])
    except ValueError as e:
        raise GTFSCollectionError(
            file_name=TRIPS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[TRIP_ID_COL_HEADER]
        ) from e

def validate_and_parse_trip_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace;
    otherwise returns the trimmed string.
    """
    require_not_none(raw_trip_id=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_trip_headsign(raw: str, row_num: int) -> str | None:
    """
    Returns None if the given string is empty or only whitespace; otherwise
    returns the trimmed string.
    """
    require_not_none(raw_trip_headsign=raw)
    require_valid_row_num(row_num)

    return parse_optional_str(raw)

def validate_and_parse_winnipeg_block_id(raw: str, row_num: int) -> WinnipegBlockID | None:
    """
    Throws an exception if the given string is both non-empty and not a valid
    Winnipeg block ID; otherwise returns a WinnipegBlockID object, or None if
    the string was empty.
    """
    require_not_none(raw_block_id=raw)
    require_valid_row_num(row_num)

    block_id_str = parse_optional_str(raw)
    if block_id_str is None:
        return None

    block_id_tokens = block_id_str.split(WPG_BLOCK_ID_TOKEN_DELIMITER)
    if len(block_id_tokens) != WPG_BLOCK_ID_NUM_TOKENS:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_BLOCK_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        )

    for token in block_id_tokens:
        try:
            validate_and_parse_integer_str(token)
        except ValueError as e:
            raise GTFSAttributeError(
                file_name=TRIPS_FILE_NAME,
                column_name=TRIP_BLOCK_ID_COL_HEADER,
                row_num=row_num,
                invalid_token=raw
            ) from e

    return WinnipegBlockID(block_id_str)

def validate_and_parse_trip_direction(raw: str, row_num: int) -> int | None:
    """
    Throws an exception if the given string is not an integer corresponding
    to a legal direction ID; otherwise returns the value as an integer.
    """
    require_not_none(raw_trip_direction_id=raw)
    require_valid_row_num(row_num)

    direction_str = parse_optional_str(raw)
    if direction_str is None:
        return None

    try:
        direction_int = validate_and_parse_integer_str(raw)

        if direction_int not in TRIP_DIRECTION_VALUES:
            raise ValueError
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_DIRECTION_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    return direction_int

def validate_and_parse_route_id_as_foreign_key(
        raw: str,
        routes: dict[str, Route],
        row_num: int
) -> Route:
    """
    Throws an exception if the given string is not a valid route ID referencing
    a route in the given dictionary; otherwise returns the corresponding route
    from the dictionary.
    """
    try:
        route_id = validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_ROUTE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    route = routes.get(route_id)

    if route is None:
        raise GTFSForeignKeyError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_ROUTE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw,
            referenced_file_name=ROUTES_FILE_NAME
        )

    return route

def validate_and_parse_service_id_as_foreign_key(
        raw: str,
        service_patterns: dict[str, ServicePattern],
        row_num: int
) -> ServicePattern:
    """
    Throws an exception if given string is not a valid service ID referencing a
    service pattern in the given dictionary; otherwise returns the corresponding
    service pattern from the dictionary.
    """
    try:
        service_id = validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_SERVICE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    pattern = service_patterns.get(service_id)
    if pattern is None:
        raise GTFSForeignKeyError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_SERVICE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw,
            referenced_file_name=SERVICE_PATTERNS_FILE_NAME
        )

    return pattern

def validate_and_parse_shape_id_as_foreign_key(
        raw: str,
        shapes: dict[str, Shape],
        row_num: int
) -> Shape | None:
    """
    Throws an exception if the given string is both non-empty and not a valid
    shape ID referencing a shape in the given dictionary; otherwise returns the
    corresponding shape from the dictionary, or None if the given string was
    empty.
    """
    shape_id_str = parse_optional_str(raw)
    if shape_id_str is None:
        return None

    try:
        shape_id = validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_SHAPE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    shape = shapes.get(shape_id)
    if shape is None:
        raise GTFSForeignKeyError(
            file_name=TRIPS_FILE_NAME,
            column_name=TRIP_SHAPE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw,
            referenced_file_name=SHAPES_FILE_NAME
        )

    return shape

