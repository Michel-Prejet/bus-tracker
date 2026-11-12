from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_TIMEZONE_COL_HEADER
from gtfs.constants.gtfs_constants import AGENCY_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.agency import Agency
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.value_parsing.primitive_parser import parse_string
from gtfs.parsing.value_parsing.timezone_parser import parse_timezone
from gtfs.parsing.value_parsing.url_parser import parse_url
from gtfs.parsing.validation.collection_validator import validate_agencies


AGENCY_REQUIRED_COLUMNS = [
    AGENCY_NAME_COL_HEADER,
    AGENCY_URL_COL_HEADER,
    AGENCY_TIMEZONE_COL_HEADER
]

def parse_agencies(file_name: str) -> list[Agency]:
    """
    Creates a list of Agency objects from the rows in the given file, or
    throws an exception if the file or its contents are invalid.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=AGENCY_REQUIRED_COLUMNS,
        object_builder_from_row=_create_agency_from_row,
        collection_validator=validate_agencies
    )

def _create_agency_from_row(row: dict[str, str | None], row_num: int) -> Agency:
    parser = RowParsingFactory(
        file_name=AGENCY_FILE_NAME,
        row=row,
        row_num=row_num
    )

    agency_name = parser.get_attribute(
        column_name=AGENCY_NAME_COL_HEADER,
        parser=parse_string
    )

    agency_url = parser.get_attribute(
        column_name=AGENCY_URL_COL_HEADER,
        parser=parse_url
    )

    timezone = parser.get_attribute(
        column_name=AGENCY_TIMEZONE_COL_HEADER,
        parser=parse_timezone
    )

    return Agency(
        agency_name=agency_name,
        agency_url=agency_url,
        timezone=timezone
    )