from gtfs.constants.csv_column_headers.stop_visit_headers import STOP_VISIT_TRIP_ID_COL_HEADER, \
    STOP_VISIT_ARRIVAL_TIME_COL_HEADER, STOP_VISIT_DEPARTURE_TIME_COL_HEADER, STOP_VISIT_STOP_ID_COL_HEADER, \
    STOP_VISIT_STOP_SEQUENCE_COL_HEADER
from gtfs.csv_parsing.csv_parsing_helper import get_opt_attribute, parse_gtfs_file
from gtfs.domain.stop import Stop
from gtfs.domain.trip.stop_visit import StopVisit
from gtfs.domain.trip.trip import Trip
from gtfs.utilities.dict_reader_row_to_csv import dict_reader_row_to_csv
from gtfs.validation.stop_visit_validator import validate_and_parse_trip_id_as_foreign_key, \
    validate_and_parse_stop_visit_arrival_time, validate_and_parse_stop_visit_departure_time, \
    validate_and_parse_stop_id_as_foreign_key, validate_stop_visit_attribute_combination, \
    validate_and_parse_stop_visit_sequence_number, validate_stop_visit_collection


STOP_VISIT_REQUIRED_COLUMNS = [
    STOP_VISIT_TRIP_ID_COL_HEADER,
    STOP_VISIT_STOP_ID_COL_HEADER,
    STOP_VISIT_STOP_SEQUENCE_COL_HEADER
]

def parse_stop_visits(
        file_name: str,
        trips: dict[str, Trip],
        stops: dict[str, Stop]
) -> list[StopVisit]:
    """
    Creates a list of StopVisit objects from the rows in the given file,
    then adds them to their corresponding trip in the given dictionary, throwing
    an exception if the file or its contents are invalid.
    """
    stop_visits = parse_gtfs_file(
        file_name=file_name,
        required_column_names=STOP_VISIT_REQUIRED_COLUMNS,
        object_builder_from_row=(lambda row, row_num:
        _create_stop_visit_from_row(row, row_num, trips, stops))
    )

    stop_visit_dict = _create_stop_visit_dict_from_tuples(stop_visits)

    validate_stop_visit_collection(stop_visit_dict)

    for trip, stop_visit_list in stop_visit_dict.items():
        for visit in stop_visit_list:
            trip.add_stop_visit(visit)

    return [visit for trip, visit in stop_visits]

def _create_stop_visit_from_row(
        row: dict[str, str | None],
        row_num: int,
        trips: dict[str, Trip],
        stops: dict[str, Stop]
) -> tuple[Trip, StopVisit]:
    trip = validate_and_parse_trip_id_as_foreign_key(
        row[STOP_VISIT_TRIP_ID_COL_HEADER],
        trips,
        row_num
    )

    arrival_time = get_opt_attribute(
        column_name=STOP_VISIT_ARRIVAL_TIME_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_stop_visit_arrival_time
    )

    departure_time = get_opt_attribute(
        column_name=STOP_VISIT_DEPARTURE_TIME_COL_HEADER,
        row=row,
        row_num=row_num,
        validator=validate_and_parse_stop_visit_departure_time
    )

    stop = validate_and_parse_stop_id_as_foreign_key(
        row[STOP_VISIT_STOP_ID_COL_HEADER],
        stops,
        row_num
    )

    sequence_order = validate_and_parse_stop_visit_sequence_number(
        row[STOP_VISIT_STOP_SEQUENCE_COL_HEADER],
        row_num=row_num
    )

    validate_stop_visit_attribute_combination(
        arrival_time=arrival_time, departure_time=departure_time,
        row=dict_reader_row_to_csv(row), row_num=row_num
    )

    return trip, StopVisit(
        stop=stop,
        scheduled_arrival=arrival_time,
        scheduled_departure=departure_time,
        sequence_order=sequence_order
    )

def _create_stop_visit_dict_from_tuples(
        stop_visits: list[tuple[Trip, StopVisit]]
) -> dict[Trip, list[StopVisit]]:
    """
    Creates a dictionary mapping trips to a list of their corresponding
    stop visits, given a list of (trip, stopVisit) tuples.
    """
    stop_visit_dict: dict[Trip, list[StopVisit]] = {}
    for trip, stop_visit in stop_visits:
        if trip not in stop_visit_dict:
            stop_visit_dict[trip] = []

        stop_visit_dict[trip].append(stop_visit)

    return stop_visit_dict




