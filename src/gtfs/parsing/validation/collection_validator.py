from gtfs.constants.csv_column_headers.agency_headers import AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER, \
    AGENCY_TIMEZONE_COL_HEADER
from gtfs.constants.csv_column_headers.feed_info_headers import PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER, \
    FEED_START_DATE_COL_HEADER, FEED_END_DATE_COL_HEADER
from gtfs.constants.csv_column_headers.route_headers import ROUTE_ID_COL_HEADER
from gtfs.constants.csv_column_headers.service_pattern_headers import SERVICE_ID_COL_HEADER
from gtfs.constants.csv_column_headers.service_pattern_override_headers import OVERRIDE_SERVICE_ID_COL_HEADER, \
    OVERRIDE_DATE_COL_HEADER
from gtfs.constants.csv_column_headers.shapes_headers import SHAPE_POINT_SEQUENCE_COL_HEADER
from gtfs.constants.csv_column_headers.stop_headers import STOP_ID_COL_HEADER
from gtfs.constants.csv_column_headers.stop_visit_headers import STOP_VISIT_STOP_SEQUENCE_COL_HEADER
from gtfs.constants.csv_column_headers.trips_headers import TRIP_ID_COL_HEADER
from gtfs.constants.gtfs_constants import STOPS_FILE_NAME, ROUTES_FILE_NAME, NUM_AGENCIES_SUPPORTED, AGENCY_FILE_NAME, \
    NUM_FEED_INFOS_ALLOWED, SERVICE_PATTERNS_FILE_NAME, SERVICE_PATTERN_OVERRIDES_FILE_NAME, FEED_INFO_FILE_NAME, \
    SHAPES_FILE_NAME, TRIPS_FILE_NAME, STOP_VISITS_FILE_NAME
from gtfs.domain.agency import Agency
from gtfs.domain.feed_info import FeedInfo
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.domain.shape.shape_point import ShapePoint
from gtfs.domain.stop import Stop
from gtfs.domain.trip.stop_visit import StopVisit
from gtfs.domain.trip.trip import Trip
from gtfs.exceptions.gtfs_collection_error import GTFSCollectionError


def validate_stops(stops: list[Stop]) -> None:
    """
    Throws an exception if the same stop ID appears more than once in the
    given list of stops.
    """
    _assert_unique(
        [stop.id for stop in stops],
        GTFSCollectionError(
            file_name=STOPS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[STOP_ID_COL_HEADER]
        )
    )

def validate_routes(routes: list[Route]) -> None:
    """
    Throws an exception if the same route ID appears more than once in the
    given list of routes.
    """
    _assert_unique(
        [route.id for route in routes],
        GTFSCollectionError(
            file_name=ROUTES_FILE_NAME,
            names_of_columns_with_violated_restrictions=[ROUTE_ID_COL_HEADER]
        )
    )

def validate_agencies(agencies: list[Agency]) -> None:
    """
    Throws an exception if there is not exactly one agency in the given list.
    """
    if len(agencies) != NUM_AGENCIES_SUPPORTED:
        raise GTFSCollectionError(
            file_name=AGENCY_FILE_NAME,
            names_of_columns_with_violated_restrictions=[
                AGENCY_NAME_COL_HEADER, AGENCY_URL_COL_HEADER,
                AGENCY_TIMEZONE_COL_HEADER,
            ]
        )

def validate_feed_infos(feed_infos: list[FeedInfo]) -> None:
    """
    Throws an exception if there is not exactly one feed info object in the
    given list.
    There must be exactly one feed info as per official GTFS requirements.
    """
    if len(feed_infos) != NUM_FEED_INFOS_ALLOWED:
        raise GTFSCollectionError(
            file_name=FEED_INFO_FILE_NAME,
            names_of_columns_with_violated_restrictions=[
                PUBLISHER_NAME_COL_HEADER, PUBLISHER_URL_COL_HEADER,
                FEED_START_DATE_COL_HEADER, FEED_END_DATE_COL_HEADER
            ]
        )

def validate_service_patterns(service_patterns: list[ServicePattern]) -> None:
    """
    Throws an exception if the same service ID appears more than once in the
    given list of service patterns.
    """
    _assert_unique(
        [pattern.service_id for pattern in service_patterns],
        GTFSCollectionError(
            file_name=SERVICE_PATTERNS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[SERVICE_ID_COL_HEADER]
        )
    )

def validate_service_pattern_overrides(
        override_assignments: list[tuple[ServicePattern, ServicePatternOverride]]
) -> None:
    """
    Throws an exception if the same (serviceID, overrideDate) tuple appears more
    than once in the given list.
    """
    _assert_unique(
        [(pattern.service_id, override.date) for pattern, override in override_assignments],
        GTFSCollectionError(
            SERVICE_PATTERN_OVERRIDES_FILE_NAME,
            [OVERRIDE_SERVICE_ID_COL_HEADER, OVERRIDE_DATE_COL_HEADER]
        )
    )

def validate_shape_points(
        shapes: dict[str, list[ShapePoint]]
) -> None:
    """
    Throws an exception if the same sequence order appears more than once in
    any of the lists of shape points in the given dictionary.
    """
    for shape, shape_points in shapes.items():
        _assert_unique(
            [point.sequence_order for point in shape_points],
            GTFSCollectionError(
                file_name=SHAPES_FILE_NAME,
                names_of_columns_with_violated_restrictions=[SHAPE_POINT_SEQUENCE_COL_HEADER]
            )
        )

def validate_trips(trips: list[Trip]) -> None:
    """
    Throws an exception if the same trip ID appears more than once in the
    given list of trips.
    """
    _assert_unique(
        [trip.id for trip in trips],
        GTFSCollectionError(
            file_name=TRIPS_FILE_NAME,
            names_of_columns_with_violated_restrictions=[TRIP_ID_COL_HEADER]
        )
    )

def validate_stop_visits(stop_visits: dict[Trip, list[StopVisit]]) -> None:
    """
    Throws an exception if the same sequence order appears more than once in
    any of the lists of stop visits in the given dictionary.
    """
    for trip, stop_visits in stop_visits.items():
        _assert_unique(
            [visit.sequence_order for visit in stop_visits],
            GTFSCollectionError(
                file_name=STOP_VISITS_FILE_NAME,
                names_of_columns_with_violated_restrictions=[STOP_VISIT_STOP_SEQUENCE_COL_HEADER]
            )
        )

def _assert_unique[T](
        items: list[T],
        exc: GTFSCollectionError
) -> None:
    """
    Throws the given exception if there are duplicate items in the given
    list.
    """
    seen: set[T] = set()

    for item in items:
        if item in seen:
            raise exc

        seen.add(item)