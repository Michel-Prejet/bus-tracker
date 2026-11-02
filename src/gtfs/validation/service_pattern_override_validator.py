from datetime import date
from gtfs.constants.csv_column_headers.service_pattern_override_headers import OVERRIDE_DATE_COL_HEADER, \
    OVERRIDE_TYPE_COL_HEADER, OVERRIDE_SERVICE_ID_COL_HEADER
from gtfs.constants.gtfs_constants import SERVICE_PATTERN_OVERRIDES_FILE_NAME, SERVICE_PATTERNS_FILE_NAME
from gtfs.domain.enums.service_pattern_override_type import ServicePatternOverrideType
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError, GTFSForeignKeyError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_date, validate_and_parse_integer_str, \
    validate_and_parse_nonempty_id_str
from invariant_helper import require_not_none


def validate_service_pattern_override_collection(
        override_assignments: list[tuple[ServicePattern, ServicePatternOverride]]
) -> None:
    """
    Throws an exception if the same (serviceID, overrideDate) tuple appears more
    than once in the given list.
    """
    require_not_none(service_pattern_override_dictionary=override_assignments)
    for pattern, override in override_assignments:
        require_not_none(
            service_pattern_in_dictionary=pattern,
            service_pattern_override_in_dictionary=override
        )

    keys_seen: set[tuple[str, date]] = set()

    for pattern, override in override_assignments:
        service_id = pattern.service_id

        if (service_id, override.date) in keys_seen:
            raise GTFSCollectionError(
                SERVICE_PATTERN_OVERRIDES_FILE_NAME,
                [OVERRIDE_SERVICE_ID_COL_HEADER, OVERRIDE_DATE_COL_HEADER]
            )
        keys_seen.add((service_id, override.date))

def validate_and_parse_override_service_id_as_foreign_key(
        raw: str,
        service_patterns: list[ServicePattern],
        row_num: int
) -> ServicePattern:
    """
    Throws an exception if given string is not a valid service ID referencing a
    service pattern in the given list; otherwise returns the corresponding
    service pattern from the list.
    """
    require_not_none(raw_service_id=raw)
    require_valid_row_num(row_num)

    try:
        service_id =  validate_and_parse_nonempty_id_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERN_OVERRIDES_FILE_NAME,
            column_name=OVERRIDE_SERVICE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    for pattern in service_patterns:
        if pattern.service_id == service_id:
            return pattern

    raise GTFSForeignKeyError(
        file_name=SERVICE_PATTERN_OVERRIDES_FILE_NAME,
        column_name=OVERRIDE_SERVICE_ID_COL_HEADER,
        row_num=row_num,
        invalid_token=service_id,
        referenced_file_name=SERVICE_PATTERNS_FILE_NAME
    )

def validate_and_parse_override_date(raw: str, row_num: int) -> date:
    """
    Throws an exception if the given string is not a valid date in
    YYYYMMDD format; returns a date object otherwise.
    """
    require_not_none(raw_override_date=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_date(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERN_OVERRIDES_FILE_NAME,
            column_name=OVERRIDE_DATE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_override_type(raw: str, row_num: int) -> ServicePatternOverrideType:
    """
    Throws an exception if the given string is not an integer corresponding
    to a valid ServicePatternOverrideType; otherwise, the corresponding
    ServicePatternOverrideType object is returned.
    """
    require_not_none(raw_override_type=raw)
    require_valid_row_num(row_num)

    try:
        return ServicePatternOverrideType(validate_and_parse_integer_str(raw))
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERN_OVERRIDES_FILE_NAME,
            column_name=OVERRIDE_TYPE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e