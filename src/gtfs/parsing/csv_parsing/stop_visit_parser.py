from gtfs.constants.csv_column_headers.stop_visit_headers import STOP_VISIT_TRIP_ID_COL_HEADER, \
    STOP_VISIT_ARRIVAL_TIME_COL_HEADER, STOP_VISIT_DEPARTURE_TIME_COL_HEADER, STOP_VISIT_STOP_ID_COL_HEADER, \
    STOP_VISIT_STOP_SEQUENCE_COL_HEADER
from gtfs.constants.gtfs_constants import STOP_VISITS_FILE_NAME, TRIPS_FILE_NAME, STOPS_FILE_NAME
from gtfs.parsing.helpers.gtfs_file_parser import parse_gtfs_file
from gtfs.domain.stop import Stop
from gtfs.domain.trip.stop_visit import StopVisit
from gtfs.domain.trip.trip import Trip
from gtfs.parsing.helpers.row_parsing_factory import RowParsingFactory
from gtfs.parsing.validation.attribute_validator import assert_nonnegative
from gtfs.parsing.validation.collection_validator import validate_stop_visits
from gtfs.parsing.validation.instance_validator import assert_not_greater_than
from gtfs.parsing.value_parsing.datetime_parser import parse_time
from gtfs.parsing.value_parsing.primitive_parser import parse_string, parse_integer


STOP_VISIT_REQUIRED_COLUMNS = [
    STOP_VISIT_TRIP_ID_COL_HEADER,
    STOP_VISIT_STOP_ID_COL_HEADER,
    STOP_VISIT_STOP_SEQUENCE_COL_HEADER,
    STOP_VISIT_ARRIVAL_TIME_COL_HEADER,
    STOP_VISIT_DEPARTURE_TIME_COL_HEADER
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

    validate_stop_visits(stop_visit_dict)

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
    parser = RowParsingFactory(
        file_name=STOP_VISITS_FILE_NAME,
        row=row,
        row_num=row_num
    )

    trip = parser.get_attribute_as_foreign_key(
        column_name=STOP_VISIT_TRIP_ID_COL_HEADER,
        referenced_objs=trips,
        referenced_file_name=TRIPS_FILE_NAME,
        parser=parse_string
    )

    arrival_time = parser.get_attribute(
        column_name=STOP_VISIT_ARRIVAL_TIME_COL_HEADER,
        parser=parse_time
    )

    departure_time = parser.get_attribute(
        column_name=STOP_VISIT_DEPARTURE_TIME_COL_HEADER,
        parser=parse_time
    )

    stop = parser.get_attribute_as_foreign_key(
        column_name=STOP_VISIT_STOP_ID_COL_HEADER,
        referenced_objs=stops,
        referenced_file_name=STOPS_FILE_NAME,
        parser=parse_string
    )

    sequence_order = parser.get_attribute(
        column_name=STOP_VISIT_STOP_SEQUENCE_COL_HEADER,
        parser=parse_integer,
        validator=assert_nonnegative
    )

    parser.assert_valid_instance(
        lambda: assert_not_greater_than(arrival_time, departure_time)
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