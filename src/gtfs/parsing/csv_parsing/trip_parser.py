from gtfs.constants.csv_column_headers.trips_headers import TRIP_ID_COL_HEADER, TRIP_HEADSIGN_COL_HEADER, \
    TRIP_BLOCK_ID_COL_HEADER, TRIP_DIRECTION_ID_COL_HEADER, TRIP_ROUTE_ID_COL_HEADER, TRIP_SERVICE_ID_COL_HEADER, \
    TRIP_SHAPE_ID_COL_HEADER
from gtfs.constants.gtfs_constants import TRIPS_FILE_NAME, ROUTES_FILE_NAME, SERVICE_PATTERNS_FILE_NAME, \
    SHAPES_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.trip.trip import Trip
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.collection_validator import validate_trips
from gtfs.parsing.value_parsing.direction_parser import parse_direction_id
from gtfs.parsing.value_parsing.primitive_parser import parse_string
from gtfs.parsing.value_parsing.wpg_block_id_parser import parse_winnipeg_block_id


TRIPS_REQUIRED_COLUMNS = [
    TRIP_ID_COL_HEADER,
    TRIP_ROUTE_ID_COL_HEADER,
    TRIP_SERVICE_ID_COL_HEADER,
    TRIP_BLOCK_ID_COL_HEADER
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
        collection_validator=validate_trips
    )

    return {trip.id: trip for trip in trips}

def _create_trip_from_row(
        row: dict[str, str | None],
        row_num: int,
        routes: dict[str, Route],
        service_patterns: dict[str, ServicePattern],
        shapes: dict[str, Shape]
) -> Trip:
    parser = RowParsingFactory(
        file_name=TRIPS_FILE_NAME,
        row=row,
        row_num=row_num
    )

    trip_id = parser.get_attribute(
        column_name=TRIP_ID_COL_HEADER,
        parser=parse_string
    )

    headsign = parser.get_attribute(
        column_name=TRIP_HEADSIGN_COL_HEADER,
        parser=parse_string,
        optional=True
    )

    block = parser.get_attribute(
        column_name=TRIP_BLOCK_ID_COL_HEADER,
        parser=parse_winnipeg_block_id
    )

    direction = parser.get_attribute(
        column_name=TRIP_DIRECTION_ID_COL_HEADER,
        parser=parse_direction_id,
        optional=True
    )

    route = parser.get_attribute_as_foreign_key(
        column_name=TRIP_ROUTE_ID_COL_HEADER,
        referenced_objs=routes,
        referenced_file_name=ROUTES_FILE_NAME,
        parser=parse_string
    )

    service_pattern = parser.get_attribute_as_foreign_key(
        column_name=TRIP_SERVICE_ID_COL_HEADER,
        referenced_objs=service_patterns,
        referenced_file_name=SERVICE_PATTERNS_FILE_NAME,
        parser=parse_string
    )

    shape = parser.get_attribute_as_foreign_key(
        column_name=TRIP_SHAPE_ID_COL_HEADER,
        referenced_objs=shapes,
        referenced_file_name=SHAPES_FILE_NAME,
        parser=parse_string,
        optional=True
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