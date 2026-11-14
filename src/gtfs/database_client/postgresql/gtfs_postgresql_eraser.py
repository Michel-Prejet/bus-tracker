from psycopg import Connection
from gtfs.database_client.gtfs_eraser import GTFSEraser


class GTFSPostgreSQLEraser(GTFSEraser):
    """
    Opens a connection to the PostgreSQL database and deletes rows from GTFS
    tables.
    """

    def __init__(self, db: Connection):
        self._db = db

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def clear_tables(self) -> None:
        """
        Deletes all rows from every table in the database.
        """
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE
                        gtfs.agency,
                        gtfs.feed_info,
                        gtfs.route,
                        gtfs.stop,
                        gtfs.service_pattern,
                        gtfs.shape,
                        gtfs.trip
                CASCADE
                """
            )