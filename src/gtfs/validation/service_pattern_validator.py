from typing import TypedDict
from gtfs.constants.csv_column_headers.service_pattern_headers import MONDAY_COL_HEADER, TUESDAY_COL_HEADER, \
    SUNDAY_COL_HEADER, SATURDAY_COL_HEADER, FRIDAY_COL_HEADER, THURSDAY_COL_HEADER, WEDNESDAY_COL_HEADER, \
    SERVICE_ID_COL_HEADER, SERVICE_PATTERN_START_DATE_COL_HEADER, SERVICE_PATTERN_END_DATE_COL_HEADER
from gtfs.constants.gtfs_constants import SERVICE_PATTERNS_FILE_NAME
from gtfs.domain.enums.day_of_week import DayOfWeek
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.values.date_range import DateRange
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSLogicError, GTFSAttributeError
from gtfs.utilities.require_valid_row_num import require_valid_row_num
from gtfs.validation.general_validator import validate_and_parse_boolean_str, validate_and_parse_nonempty_id_str, \
    validate_and_parse_date, assert_that_ids_are_unique
from invariant_helper import require_not_none
from datetime import date


def validate_service_pattern_collection(service_patterns: list[ServicePattern]) -> None:
    """
    Throws an exception if the same service pattern ID appears more than once
    in the given list of service patterns.
    """
    require_not_none(service_pattern_list=service_patterns)
    for pattern in service_patterns:
        require_not_none(service_pattern_in_list=pattern)

    try:
        assert_that_ids_are_unique([pattern.service_id for pattern in service_patterns])
    except ValueError:
        raise GTFSCollectionError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[SERVICE_ID_COL_HEADER]
        )

def validate_and_parse_service_id(raw: str, row_num: int) -> str:
    """
    Throws an exception if the given string is empty or only whitespace.
    Otherwise, the trimmed string is returned.
    """
    require_not_none(raw_service_id=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_nonempty_id_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            column_name=SERVICE_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

class RawWeekdayFlags(TypedDict):
    MONDAY: str
    TUESDAY: str
    WEDNESDAY: str
    THURSDAY: str
    FRIDAY: str
    SATURDAY: str
    SUNDAY: str
def validate_and_parse_active_weekdays(weekday_flags_raw: RawWeekdayFlags,
                                       row_num: int) -> set[DayOfWeek]:
    """
    Throws an exception if any of the flags in the given typed dictionary
    are invalid; otherwise, returns a list of weekdays containing each
    day of the week associated with a "1" flag.
    """
    require_not_none(collection_of_weekday_flags=weekday_flags_raw)
    for flag in weekday_flags_raw.values():
        require_not_none(value_in_collection_of_weekday_flags=flag)
    require_valid_row_num(row_num)

    active_weekdays: set[DayOfWeek] = set()

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["SUNDAY"],
        active_weekdays,
        DayOfWeek.SUNDAY,
        SUNDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["MONDAY"],
        active_weekdays,
        DayOfWeek.MONDAY,
        MONDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["TUESDAY"],
        active_weekdays,
        DayOfWeek.TUESDAY,
        TUESDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["WEDNESDAY"],
        active_weekdays,
        DayOfWeek.WEDNESDAY,
        WEDNESDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["THURSDAY"],
        active_weekdays,
        DayOfWeek.THURSDAY,
        THURSDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["FRIDAY"],
        active_weekdays,
        DayOfWeek.FRIDAY,
        FRIDAY_COL_HEADER,
        row_num
    )

    _validate_flag_and_append_weekday_if_true(
        weekday_flags_raw["SATURDAY"],
        active_weekdays,
        DayOfWeek.SATURDAY,
        SATURDAY_COL_HEADER,
        row_num
    )

    return active_weekdays

def _validate_flag_and_append_weekday_if_true(
        flag_raw: str,
        active_weekdays: set[DayOfWeek],
        weekday_to_append: DayOfWeek,
        column_name: str,
        row_num: int
) -> None:
    try:
        if validate_and_parse_boolean_str(flag_raw):
            active_weekdays.add(weekday_to_append)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            column_name=column_name,
            row_num=row_num,
            invalid_token=flag_raw
        ) from e

def validate_and_parse_service_pattern_date_range(start_date: date, end_date: date,
                                                  row_num: int) -> DateRange:
    """
    Throws an exception if the given start date comes before the given end
    date; otherwise returns a DateRange object.
    """
    require_not_none(
        start_date=start_date,
        end_date=end_date
    )
    require_valid_row_num(row_num)

    if start_date > end_date:
        raise GTFSLogicError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            row_num=row_num,
            col_names_and_invalid_tokens={
                SERVICE_PATTERN_START_DATE_COL_HEADER: start_date.isoformat(),
                SERVICE_PATTERN_END_DATE_COL_HEADER: end_date.isoformat()
            }
        )

    return DateRange(start_date, end_date)

def validate_and_parse_start_date(raw: str, row_num: int) -> date:
    """
    Throws an exception if the given string is not a valid date in
    YYYYMMDD format; returns a date object otherwise.
    """
    require_not_none(raw_start_date=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_date(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            column_name=SERVICE_PATTERN_START_DATE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_end_date(raw: str, row_num: int) -> date:
    """
    Throws an exception if the given string is not a valid date in
    YYYYMMDD format; returns a date object otherwise.
    """
    require_not_none(raw_end_date=raw)
    require_valid_row_num(row_num)

    try:
        return validate_and_parse_date(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            column_name=SERVICE_PATTERN_END_DATE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

