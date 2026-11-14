from database_connection import connection
from gtfs.database_client.gtfs_writer import GTFSWriter
from gtfs.domain.agency import Agency
from gtfs.domain.enums.day_of_week import DayOfWeek
from gtfs.domain.feed_info import FeedInfo
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.stop import Stop
from gtfs.domain.trip.trip import Trip


class GTFSPostgreSQLWriter(GTFSWriter):
    """
    Opens a connection to the PostgreSQL database and writes GTFS objects.
    """

    def __init__(self):
        self._db = connection()

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def write_agency(self, agency: Agency) -> None:
        """
        Inserts the given agency into the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.agency
                    (agency_name, agency_url, timezone)
                VALUES (%s, %s, %s)
                """,
                (agency.name, agency.agency_url.value, str(agency.timezone))
            )

    def write_feed_info(self, feed_info: FeedInfo) -> None:
        """
        Inserts the given feed info into the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.feed_info
                    (publisher_name, publisher_url, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                """,
                (feed_info.publisher_name, feed_info.publisher_url.value,
                 feed_info.active_period.start, feed_info.active_period.end)
            )

    def write_route(self, route: Route) -> None:
        """
        Inserts the given route into the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.route
                    (id, short_name, long_name, route_type, route_url, 
                     background_colour, text_colour, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (route.id, route.short_name, route.long_name, route.type.value,
                 route.url.value if route.url is not None else None,
                 route.background_colour.gtfs_hex, route.text_colour.gtfs_hex,
                 route.sort_order)
            )

    def write_stop(self, stop: Stop) -> None:
        """
        Inserts the given stop into the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.stop
                    (id, stop_code, stop_name, latitude, longitude, stop_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (stop.id, stop.code, stop.name, stop.coordinates.latitude,
                 stop.coordinates.longitude,
                 stop.url.value if stop.url is not None else None)
            )

    def write_service_pattern_and_overrides(
            self, service_pattern: ServicePattern
    ) -> None:
        """
        Inserts the given service pattern and its associated service pattern
        overrides into the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.service_pattern
                    (id, monday, tuesday, wednesday, thursday, friday, saturday, 
                    sunday, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (service_pattern.service_id,
                 DayOfWeek.MONDAY in service_pattern.weekdays_active,
                 DayOfWeek.TUESDAY in service_pattern.weekdays_active,
                 DayOfWeek.WEDNESDAY in service_pattern.weekdays_active,
                 DayOfWeek.THURSDAY in service_pattern.weekdays_active,
                 DayOfWeek.FRIDAY in service_pattern.weekdays_active,
                 DayOfWeek.SATURDAY in service_pattern.weekdays_active,
                 DayOfWeek.SUNDAY in service_pattern.weekdays_active,
                 service_pattern.active_period.start,
                 service_pattern.active_period.end)
            )

            for override in service_pattern.overrides:
                cursor.execute(
                    """
                    INSERT INTO gtfs.service_pattern_override
                        (service_id, override_date, override_type)
                    VALUES (%s, %s, %s)
                    """,
                    (service_pattern.service_id, override.date,
                     override.type.value)
                )

    def write_shape_and_points(self, shape: Shape) -> None:
        """
        Inserts the given shape and its associated shape points into the
        database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.shape(id)
                VALUES (%s)
                """,
                (shape.id,)
            )

            for point in shape.points:
                cursor.execute(
                    """
                    INSERT INTO gtfs.shape_point
                        (shape_id, latitude, longitude, sequence_order)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (shape.id, point.coordinates.latitude,
                     point.coordinates.longitude, point.sequence_order)
                )

    def write_trip_and_stop_visits(self, trip: Trip) -> None:
        """
        Inserts the given trip and its associated stop visits into the
        database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO gtfs.trip
                    (id, route, service_pattern, shape, block_id, headsign,
                    direction_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (trip.id, trip.route.id, trip.service_pattern.service_id,
                 trip.shape.id if trip.shape is not None else None,
                 trip.block.gtfs_format(), trip.headsign, trip.direction)
            )

            for visit in trip.stop_visits:
                cursor.execute(
                    """
                    INSERT INTO gtfs.stop_visit
                        (trip, stop, scheduled_arrival, scheduled_departure,
                        sequence_order)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (trip.id, visit.stop.id, visit.scheduled_arrival,
                     visit.scheduled_departure, visit.sequence_order)
                )
