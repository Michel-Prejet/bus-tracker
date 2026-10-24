from gtfs.constants.csv_column_headers.stop_headers import STOP_ID_COL_HEADER, STOP_NAME_COL_HEADER, \
    STOP_LATITUDE_COL_HEADER, STOP_LONGITUDE_COL_HEADER, STOP_CODE_COL_HEADER, STOP_URL_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file, get_opt_attribute
from gtfs.domain.stop import Stop
from gtfs.domain.values.coordinates import Coordinates
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.stop_validator import validate_stop_collection, validate_and_parse_stop_id, \
    validate_and_parse_stop_code, validate_and_parse_stop_name, validate_and_parse_stop_latitude, \
    validate_and_parse_stop_longitude, validate_and_parse_stop_url
from invariant_helper import require_not_none


STOP_REQUIRED_COLUMNS = [
    STOP_ID_COL_HEADER,
    STOP_NAME_COL_HEADER,
    STOP_LATITUDE_COL_HEADER,
    STOP_LONGITUDE_COL_HEADER
]

def parse_stops(file_name: str) -> list[Stop]:
    """
    Creates a list of stop objects from the rows in the given file, or
    raises an exception if the file or its contents are invalid.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=STOP_REQUIRED_COLUMNS,
        object_builder_from_row=_create_stop_from_row,
        collection_validator=validate_stop_collection
    )

def _create_stop_from_row(row: dict[str, str | None], row_num: int) -> Stop:
    require_not_none(
        row=row,
        row_number=row_num
    )
    require_valid_row_num(row_num)

    stop_id = validate_and_parse_stop_id(row[STOP_ID_COL_HEADER], row_num)

    stop_code = get_opt_attribute(
        column_name=STOP_CODE_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_stop_code
    )

    name = validate_and_parse_stop_name(row[STOP_NAME_COL_HEADER], row_num)

    latitude = validate_and_parse_stop_latitude(row[STOP_LATITUDE_COL_HEADER], row_num)
    longitude = validate_and_parse_stop_longitude(row[STOP_LONGITUDE_COL_HEADER], row_num)
    coordinates = Coordinates(latitude, longitude)

    stop_url = get_opt_attribute(
        column_name=STOP_URL_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_stop_url
    )

    return Stop(
        stop_id=stop_id,
        stop_code=stop_code,
        name=name,
        coordinates=coordinates,
        stop_url=stop_url
    )

