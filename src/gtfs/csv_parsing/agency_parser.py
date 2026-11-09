from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_TIMEZONE_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import parse_gtfs_file
from gtfs.domain.agency import Agency
from gtfs.validation.agency_validator import validate_and_parse_agency_name, validate_and_parse_agency_url, \
    validate_and_parse_agency_timezone, validate_agency_collection


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
        collection_validator=validate_agency_collection
    )

def _create_agency_from_row(row: dict[str, str | None], row_num: int) -> Agency:
    agency_name = validate_and_parse_agency_name(
        row[AGENCY_NAME_COL_HEADER],
        row_num
    )

    agency_url = validate_and_parse_agency_url(
        row[AGENCY_URL_COL_HEADER],
        row_num
    )

    timezone = validate_and_parse_agency_timezone(
        row[AGENCY_TIMEZONE_COL_HEADER],
        row_num
    )

    return Agency(
        agency_name=agency_name,
        agency_url=agency_url,
        timezone=timezone
    )