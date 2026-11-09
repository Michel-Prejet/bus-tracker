from datetime import timedelta
from gtfs.constants.csv_column_headers.stop_visit_headers import STOP_VISIT_TRIP_ID_COL_HEADER, \
    STOP_VISIT_DEPARTURE_TIME_COL_HEADER, STOP_VISIT_ARRIVAL_TIME_COL_HEADER, STOP_VISIT_STOP_ID_COL_HEADER, \
    STOP_VISIT_STOP_SEQUENCE_COL_HEADER
from gtfs.constants.gtfs_constants import STOP_VISITS_FILE_NAME, TRIPS_FILE_NAME, STOPS_FILE_NAME
from gtfs.domain.stop import Stop
from gtfs.domain.trip.stop_visit import StopVisit
from gtfs.domain.trip.trip import Trip
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError
from gtfs.exceptions.gtfs_row_error import GTFSAttributeError, GTFSForeignKeyError, GTFSInstanceError
from gtfs.validation.general_validator import validate_and_parse_nonempty_str, \
    validate_and_parse_time, validate_and_parse_integer_str, assert_that_elements_are_unique


def validate_stop_visit_collection(stop_visits: dict[Trip, list[StopVisit]]) -> None:
    """
    Throws an exception if the same sequence order appears more than once in
    any of the lists of stop visits in the given dictionary.
    """
    try:
        for stop_visit_list in stop_visits.values():
            assert_that_elements_are_unique(
                [str(visit.sequence_order) for visit in stop_visit_list]
            )
    except ValueError as e:
        raise GTFSCollectionError(
            file_name=STOP_VISITS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[STOP_VISIT_STOP_SEQUENCE_COL_HEADER]
        ) from e

def validate_stop_visit_attribute_combination(
    arrival_time: timedelta ,
    departure_time: timedelta,
    row: str,
    row_num: int
) -> None:
    """
    Throws an exception if the given arrival time is greater than the given
    departure time.
    """
    if arrival_time > departure_time:
        raise GTFSInstanceError(
            file_name=STOP_VISITS_FILE_NAME,
            row_num=row_num,
            row=row
        )

def validate_and_parse_trip_id_as_foreign_key(
        raw: str,
        trips: dict[str, Trip],
        row_num: int
) -> Trip:
    """
    Throws an exception if the given string is not a valid trip ID referencing
    a trip in the given dictionary; otherwise returns the corresponding trip from
    the dictionary.
    """
    try:
        trip_id = validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_TRIP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    trip = trips.get(trip_id)
    if trip is None:
        raise GTFSForeignKeyError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_TRIP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw,
            referenced_file_name=TRIPS_FILE_NAME
        )

    return trip

def validate_and_parse_stop_visit_arrival_time(raw: str, row_num: int) -> timedelta:
    """
    Throws an exception if the given string is not a valid
    time in HH:MM:SS format; otherwise returns a timedelta object.
    """
    try:
        return validate_and_parse_time(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_ARRIVAL_TIME_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_stop_visit_departure_time(raw: str, row_num: int) -> timedelta:
    """
    Throws an exception if the given string is not a valid
    time in HH:MM:SS format; otherwise returns a timedelta object.
    """
    try:
        return validate_and_parse_time(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_DEPARTURE_TIME_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

def validate_and_parse_stop_id_as_foreign_key(
        raw: str,
        stops: dict[str, Stop],
        row_num: int
) -> Stop:
    """
    Throws an exception if the given string is not a valid stop ID referencing
    a stop in the given dictionary; otherwise returns the corresponding stop
    from the dictionary.
    """
    try:
        stop_id = validate_and_parse_nonempty_str(raw)
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_STOP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

    stop = stops.get(stop_id)
    if stop is None:
        raise GTFSForeignKeyError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_STOP_ID_COL_HEADER,
            row_num=row_num,
            invalid_token=raw,
            referenced_file_name=STOPS_FILE_NAME
        )

    return stop

def validate_and_parse_stop_visit_sequence_number(raw: str, row_num: int) -> int:
    """
    Throws an exception if the given string is not a non-negative integer;
    otherwise returns the value as an integer.
    """
    try:
        stop_sequence_number = validate_and_parse_integer_str(raw)

        if stop_sequence_number < 0:
            raise ValueError

        return stop_sequence_number
    except ValueError as e:
        raise GTFSAttributeError(
            file_name=STOP_VISITS_FILE_NAME,
            column_name=STOP_VISIT_STOP_SEQUENCE_COL_HEADER,
            row_num=row_num,
            invalid_token=raw
        ) from e

