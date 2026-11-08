from gtfs.constants.csv_column_headers.trips_headers import TRIP_ID_COL_HEADER, TRIP_HEADSIGN_COL_HEADER, \
    TRIP_BLOCK_ID_COL_HEADER, TRIP_DIRECTION_ID_COL_HEADER, TRIP_ROUTE_ID_COL_HEADER, TRIP_SERVICE_ID_COL_HEADER, \
    TRIP_SHAPE_ID_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import get_opt_attribute, parse_gtfs_file
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.trip.trip import Trip
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.trip_validator import validate_and_parse_trip_id, validate_and_parse_trip_headsign, \
    validate_and_parse_winnipeg_block_id, validate_and_parse_trip_direction, validate_and_parse_route_id_as_foreign_key, \
    validate_and_parse_service_id_as_foreign_key, validate_and_parse_shape_id_as_foreign_key, validate_trip_collection
from invariant_helper import require_not_none


TRIPS_REQUIRED_COLUMNS = [
    TRIP_ID_COL_HEADER,
    TRIP_ROUTE_ID_COL_HEADER,
    TRIP_SERVICE_ID_COL_HEADER,
    TRIP_SHAPE_ID_COL_HEADER
]

def parse_trips(
        file_name: str,
        routes: dict[str, Route],
        service_patterns: dict[str, ServicePattern],
        shapes: dict[str, Shape]
) -> dict[str, Trip]:
    """
    Creates a dictionary of Trip objects (keyed by trip ID) from the rows in the
    given file, or throws an exception if the file or its content are invalid.
    """
    trips = parse_gtfs_file(
        file_name=file_name,
        required_column_names=TRIPS_REQUIRED_COLUMNS,
        object_builder_from_row=(lambda row, row_num:
        _create_trip_from_row(row, row_num, routes, service_patterns, shapes)),
        collection_validator=validate_trip_collection
    )

    return {trip.id: trip for trip in trips}

def _create_trip_from_row(
        row: dict[str, str | None],
        row_num: int,
        routes: dict[str, Route],
        service_patterns: dict[str, ServicePattern],
        shapes: dict[str, Shape]
) -> Trip:
    require_not_none(
        row=row,
        route_list=routes,
        service_pattern_list=service_patterns,
        shape_list=shapes
    )
    require_valid_row_num(row_num)
    for route in routes:
        require_not_none(route_in_list=route)
    for sp in service_patterns:
        require_not_none(service_pattern_in_list=sp)
    for shape in shapes:
        require_not_none(shape_in_list=shape)

    trip_id = validate_and_parse_trip_id(row[TRIP_ID_COL_HEADER], row_num)

    headsign = get_opt_attribute(
        column_name=TRIP_HEADSIGN_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_trip_headsign
    )

    block = get_opt_attribute(
        column_name=TRIP_BLOCK_ID_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_winnipeg_block_id
    )

    direction = get_opt_attribute(
        column_name=TRIP_DIRECTION_ID_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_trip_direction
    )

    route = validate_and_parse_route_id_as_foreign_key(
        row[TRIP_ROUTE_ID_COL_HEADER],
        routes,
        row_num
    )

    service_pattern = validate_and_parse_service_id_as_foreign_key(
        row[TRIP_SERVICE_ID_COL_HEADER],
        service_patterns,
        row_num
    )

    shape = get_opt_attribute(
        column_name=TRIP_SHAPE_ID_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=(lambda raw, num:
            validate_and_parse_shape_id_as_foreign_key(raw, shapes, num)
        )
    )

    return Trip(
        trip_id=trip_id,
        route=route,
        service_pattern=service_pattern,
        block=block,
        shape=shape,
        headsign=headsign,
        direction=direction
    )