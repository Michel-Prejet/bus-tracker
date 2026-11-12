from gtfs.constants.csv_column_headers.stop_headers import STOP_ID_COL_HEADER, STOP_NAME_COL_HEADER, \
    STOP_LATITUDE_COL_HEADER, STOP_LONGITUDE_COL_HEADER, STOP_CODE_COL_HEADER, STOP_URL_COL_HEADER
from gtfs.constants.gtfs_constants import STOPS_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.value_parsing.coordinate_parser import parse_latitude, parse_longitude
from gtfs.parsing.value_parsing.primitive_parser import parse_string
from gtfs.parsing.value_parsing.url_parser import parse_url
from gtfs.domain.stop import Stop
from gtfs.domain.values.coordinates import Coordinates
from gtfs.parsing.validation.collection_validator import validate_stops


STOP_REQUIRED_COLUMNS = [
    STOP_ID_COL_HEADER,
    STOP_NAME_COL_HEADER,
    STOP_LATITUDE_COL_HEADER,
    STOP_LONGITUDE_COL_HEADER
]

def parse_stops(file_name: str) -> dict[str, Stop]:
    """
    Creates a dictionary of stop objects (keyed by stop ID) from the rows in
    the given file, or raises an exception if the file or its contents are
    invalid.
    """
    stops = parse_gtfs_file(
        file_name=file_name,
        required_column_names=STOP_REQUIRED_COLUMNS,
        object_builder_from_row=_create_stop_from_row,
        collection_validator=validate_stops
    )

    return {stop.id: stop for stop in stops}

def _create_stop_from_row(row: dict[str, str | None], row_num: int) -> Stop:
    parser = RowParsingFactory(
        file_name=STOPS_FILE_NAME,
        row=row,
        row_num=row_num
    )

    stop_id = parser.get_attribute(
        column_name=STOP_ID_COL_HEADER,
        parser=parse_string
    )

    stop_code = parser.get_attribute(
        column_name=STOP_CODE_COL_HEADER,
        parser=parse_string,
        optional=True
    )

    name = parser.get_attribute(
        column_name=STOP_NAME_COL_HEADER,
        parser=parse_string
    )

    coordinates = Coordinates(
        parser.get_attribute(
            column_name=STOP_LATITUDE_COL_HEADER,
            parser=parse_latitude
        ),
        parser.get_attribute(
            column_name=STOP_LONGITUDE_COL_HEADER,
            parser=parse_longitude
        )
    )

    stop_url = parser.get_attribute(
        column_name=STOP_URL_COL_HEADER,
        parser=parse_url,
        optional=True
    )

    return Stop(
        stop_id=stop_id,
        stop_code=stop_code,
        name=name,
        coordinates=coordinates,
        stop_url=stop_url
    )

