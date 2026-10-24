from gtfs.constants.csv_column_headers.route_headers import ROUTE_ID_COL_HEADER, ROUTE_SHORT_NAME_COL_HEADER, \
    ROUTE_LONG_NAME_COL_HEADER, ROUTE_TYPE_COL_HEADER, ROUTE_URL_COL_HEADER, ROUTE_BACKGROUND_COLOUR_COL_HEADER, \
    ROUTE_TEXT_COLOUR_COL_HEADER, ROUTE_SORT_ORDER_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import get_opt_attribute, parse_gtfs_file
from gtfs.domain.route import Route
from gtfs.utilities.dict_reader_row_to_csv import dict_reader_row_to_csv
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.route_validator import validate_and_parse_route_id, validate_and_parse_route_type, \
    validate_and_parse_route_url, validate_and_parse_route_background_colour, validate_and_parse_route_text_colour, \
    validate_and_parse_route_sort_order, validate_route_attribute_combination, validate_route_collection, \
    validate_and_parse_route_name
from invariant_helper import require_not_none


ROUTE_REQUIRED_COLUMNS = [
    ROUTE_ID_COL_HEADER,
    ROUTE_TYPE_COL_HEADER
]

def parse_routes(file_name: str) -> list[Route]:
    """
    Creates a list of Route objects from the rows in the given file, or
    raises an exception if the file or its content are invalid.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=ROUTE_REQUIRED_COLUMNS,
        object_builder_from_row=_create_route_from_row,
        collection_validator=validate_route_collection
    )

def _create_route_from_row(row: dict[str, str | None], row_num: int) -> Route:
    require_not_none(
        row=row,
        row_number=row_num
    )
    require_valid_row_num(row_num)

    route_id = validate_and_parse_route_id(row[ROUTE_ID_COL_HEADER], row_num)

    short_name = get_opt_attribute(
        column_name=ROUTE_SHORT_NAME_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_name
    )

    long_name = get_opt_attribute(
        column_name=ROUTE_LONG_NAME_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_name
    )

    route_type = validate_and_parse_route_type(row[ROUTE_TYPE_COL_HEADER], row_num)

    route_url = get_opt_attribute(
        column_name=ROUTE_URL_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_url
    )

    background_colour = get_opt_attribute(
        column_name=ROUTE_BACKGROUND_COLOUR_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_background_colour
    )

    text_colour = get_opt_attribute(
        column_name=ROUTE_TEXT_COLOUR_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_text_colour
    )

    sort_order = get_opt_attribute(
        column_name=ROUTE_SORT_ORDER_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_route_sort_order
    )

    validate_route_attribute_combination(short_name, long_name,
                                         dict_reader_row_to_csv(row), row_num)
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


