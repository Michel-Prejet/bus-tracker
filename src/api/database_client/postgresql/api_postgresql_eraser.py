from datetime import datetime
from psycopg import Connection
from api.database_client.api_eraser import APIEraser


class APIPostgreSQLEraser(APIEraser):
    """
    Opens a connection to the PostgreSQL database and deletes rows from API
    tables.
    """

    def __init__(self, db: Connection):
        self._db = db

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def delete_live_bus_assignments_older_than(self, timestamp: datetime) -> None:
        with self._db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM api.live_bus_assignment
                WHERE last_query_time < %s
                """,
                (timestamp,)
            )