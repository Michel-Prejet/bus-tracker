from database_connection import connection
from gtfs.domain.agency import Agency
from gtfs.domain.feed_info import FeedInfo


class GTFSDatabaseWriter:
    """
    Opens a connection to the database and writes GTFS objects.
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
                INSERT INTO gtfs.agency(agency_name, agency_url, timezone)
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