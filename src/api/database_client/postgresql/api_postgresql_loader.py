from psycopg import Connection
from psycopg.rows import dict_row
from api.database_client.api_loader import APILoader
from api.domain.enums.bus_length import BusLength
from api.domain.enums.bus_propulsion_type import BusPropulsionType
from api.domain.enums.bus_status import BusStatus
from api.domain.inferred_api_data.bus import Bus


class APIPostgreSQLLoader(APILoader):
    """
    Opens a connection to the PostgreSQL database and loads API data
    into memory.
    """

    def __init__(self, db: Connection):
        self._db = db

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def get_bus_by_tracking_number(self, tracking_number: str) -> Bus | None:
        """
        Loads the bus from the database with the given tracking number whose
        status is not 'retired' and returns a Bus object, or None if no such
        bus was found.
        """
        with self._db.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, tracking_number, year_built, model, manufacturer, 
                    bus_length, propulsion_type, status, last_service_date
                FROM api.bus
                WHERE 
                    bus.tracking_number = %s AND
                    bus.status != 'retired'
                """,
                (tracking_number,)
            )

            result = cursor.fetchone()

            if result is None:
                return None

            bus = Bus(
                tracking_number=result["tracking_number"],
                year=result["year_built"],
                model=result["model"],
                manufacturer=result["manufacturer"],
                length=BusLength(result["bus_length"])
                    if result["bus_length"] is not None else None,
                propulsion=BusPropulsionType(result["propulsion_type"])
                    if result["propulsion_type"] is not None else None,
                status=BusStatus(result["status"]),
                last_service_date=result["last_service_date"]
            )

            bus.database_id = result["id"]

            return bus