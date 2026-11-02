from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_FARE_URL_COL_HEADER, AGENCY_TIMEZONE_COL_HEADER, AGENCY_LANGUAGE_COL_HEADER, AGENCY_PHONE_COL_HEADER, \
    AGENCY_EMAIL_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import get_opt_attribute, parse_gtfs_file
from gtfs.domain.agency import Agency
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.agency_validator import validate_and_parse_agency_name, validate_and_parse_agency_url, \
    validate_and_parse_fare_url, validate_and_parse_agency_timezone, validate_and_parse_agency_language_code, \
    validate_and_parse_agency_phone_number, validate_and_parse_agency_email, validate_agency_collection
from invariant_helper import require_not_none


AGENCY_REQUIRED_COLUMNS = [
    AGENCY_NAME_COL_HEADER,
    AGENCY_URL_COL_HEADER,
    AGENCY_TIMEZONE_COL_HEADER
]

def parse_agencies(file_name: str) -> list[Agency]:
    """
    Creates a list of Agency objects from the rows in the given file, or
    throws an exception if the file or its contents are invalid.

    Note: the current implementation only supports the existence of one
    agency. An exception will be thrown if there is more than one row in the
    file other than the header.
    """
    return parse_gtfs_file(
        file_name=file_name,
        required_column_names=AGENCY_REQUIRED_COLUMNS,
        object_builder_from_row=_create_agency_from_row,
        collection_validator=validate_agency_collection
    )

def _create_agency_from_row(row: dict[str, str | None], row_num: int) -> Agency:
    require_not_none(row=row)
    require_valid_row_num(row_num)

    agency_name = validate_and_parse_agency_name(
        row[AGENCY_NAME_COL_HEADER],
        row_num
    )

    agency_url = validate_and_parse_agency_url(
        row[AGENCY_URL_COL_HEADER],
        row_num
    )

    fare_url = get_opt_attribute(
        column_name=AGENCY_FARE_URL_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_fare_url
    )

    timezone = validate_and_parse_agency_timezone(
        row[AGENCY_TIMEZONE_COL_HEADER],
        row_num
    )

    agency_language = get_opt_attribute(
        column_name=AGENCY_LANGUAGE_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_agency_language_code
    )

    phone_num = get_opt_attribute(
        column_name=AGENCY_PHONE_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_agency_phone_number
    )

    email = get_opt_attribute(
        column_name=AGENCY_EMAIL_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_agency_email
    )

    return Agency(
        name=agency_name,
        agency_url=agency_url,
        fare_url=fare_url,
        timezone=timezone,
        language=agency_language,
        phone_num=phone_num,
        email=email
    )