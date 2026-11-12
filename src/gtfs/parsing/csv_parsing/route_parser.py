from gtfs.constants.csv_column_headers.route_headers import ROUTE_ID_COL_HEADER, ROUTE_SHORT_NAME_COL_HEADER, \
    ROUTE_LONG_NAME_COL_HEADER, ROUTE_TYPE_COL_HEADER, ROUTE_URL_COL_HEADER, ROUTE_BACKGROUND_COLOUR_COL_HEADER, \
    ROUTE_TEXT_COLOUR_COL_HEADER, ROUTE_SORT_ORDER_COL_HEADER
from gtfs.constants.gtfs_constants import ROUTES_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.attribute_validator import assert_nonnegative
from gtfs.parsing.validation.collection_validator import validate_routes
from gtfs.parsing.validation.instance_validator import assert_at_least_one_not_none
from gtfs.parsing.value_parsing.colour_parser import parse_colour
from gtfs.parsing.value_parsing.enum_parser import parse_route_type
from gtfs.parsing.value_parsing.primitive_parser import parse_integer, parse_string
from gtfs.parsing.value_parsing.url_parser import parse_url
from gtfs.domain.route import Route


ROUTE_REQUIRED_COLUMNS = [
    ROUTE_ID_COL_HEADER,
    ROUTE_TYPE_COL_HEADER
]

def parse_routes(file_name: str) -> dict[str, Route]:
    """
    Creates a dictionary of Route objects from the rows in the given file
    (keyed by route IDs) or throws an exception if the file or its content are
    invalid.
    """
    routes = parse_gtfs_file(
        file_name=file_name,
        required_column_names=ROUTE_REQUIRED_COLUMNS,
        object_builder_from_row=_create_route_from_row,
        collection_validator=validate_routes
    )

    return {route.id: route for route in routes}

def _create_route_from_row(row: dict[str, str | None], row_num: int) -> Route:
    parser = RowParsingFactory(
        file_name=ROUTES_FILE_NAME,
        row=row,
        row_num=row_num
    )

    route_id = parser.get_attribute(
        column_name=ROUTE_ID_COL_HEADER,
        parser=parse_string
    )

    short_name = parser.get_attribute(
        column_name=ROUTE_SHORT_NAME_COL_HEADER,
        parser=parse_string,
        optional=True
    )

    long_name = parser.get_attribute(
        column_name=ROUTE_LONG_NAME_COL_HEADER,
        parser=parse_string,
        optional=True
    )

    route_type = parser.get_attribute(
        column_name=ROUTE_TYPE_COL_HEADER,
        parser=parse_route_type
    )

    route_url = parser.get_attribute(
        column_name=ROUTE_URL_COL_HEADER,
        parser=parse_url,
        optional=True
    )

    background_colour = parser.get_attribute(
        column_name=ROUTE_BACKGROUND_COLOUR_COL_HEADER,
        parser=parse_colour,
        optional=True
    )

    text_colour = parser.get_attribute(
        column_name=ROUTE_TEXT_COLOUR_COL_HEADER,
        parser=parse_colour,
        optional=True
    )

    sort_order = parser.get_attribute(
        column_name=ROUTE_SORT_ORDER_COL_HEADER,
        parser=parse_integer,
        validator=assert_nonnegative,
        optional=True
    )

    parser.assert_valid_instance(
        instance_validator=lambda: assert_at_least_one_not_none(short_name, long_name)
    )

    return Route(
        route_id=route_id,
        short_name=short_name,
        long_name=long_name,
        route_type=route_type,
        route_url=route_url,
        background_colour=background_colour,
        text_colour=text_colour,
        sort_order=sort_order
    )


