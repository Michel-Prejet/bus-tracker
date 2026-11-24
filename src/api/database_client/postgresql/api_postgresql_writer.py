from psycopg import Connection
from psycopg.rows import dict_row
from api.database_client.api_writer import APIWriter
from api.domain.enums.bus_status import BusStatus
from api.domain.inferred_api_data.bus import Bus
from api.domain.inferred_api_data.bus_assignment import BusAssignment
from api.domain.inferred_api_data.live_bus_assignment import LiveBusAssignment
from global_packages.utilities.invariant_helper import require_state


class APIPostgreSQLWriter(APIWriter):
    """
    Opens a connection to the PostgreSQL database and writes API objects.
    """

    def __init__(self, db: Connection):
        self._db = db

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def write_bus(self, bus: Bus) -> None:
        """
        Inserts the given bus into the database. If another non-retired bus
        exists with the same tracking number, its status is set to 'retired'.
        """
        with self._db.cursor(row_factory=dict_row) as cursor:
            if bus.status != BusStatus.RETIRED:
                cursor.execute(
                    """
                    UPDATE api.bus
                    SET status = 'retired'
                    WHERE
                        tracking_number = %s AND
                        status != 'retired'
                    """,
                    (bus.tracking_number,)
                )

            cursor.execute(
                """
                INSERT INTO api.bus
                (tracking_number, year_built, model, manufacturer,
                 bus_length, propulsion_type, status, last_service_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """,
                (bus.tracking_number, bus.year, bus.model, bus.manufacturer,
                 int(bus.length) if bus.length is not None else None,
                 str(bus.propulsion) if bus.propulsion is not None else None,
                 str(bus.status), bus.last_service_date)
            )

            bus.database_id = cursor.fetchone()["id"]

    def write_bus_assignment(self, assignment: BusAssignment) -> None:
        """
        Inserts the given bus assignment into the database as a historical
        record. Assumes that its bus already exists in the database. Updates
        the last service date of the bus.
        """
        require_state(
            assignment.bus.database_id is not None,
            "The assigned bus should have been inserted into the database."
        )

        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api.bus_assignment
                    (bus, block_id, service_date)
                VALUES (%s, %s, %s)
                """,
                (assignment.bus.database_id, assignment.block_id.gtfs_format(),
                 assignment.service_date)
            )

            cursor.execute(
                """
                UPDATE api.bus
                SET last_service_date = GREATEST(last_service_date, %s)
                WHERE id = %s
                """,
                (assignment.service_date, assignment.bus.database_id,)
            )

            assignment.bus.last_service_date = assignment.service_date

    def write_live_bus_assignment(self, assignment: LiveBusAssignment) -> None:
        """
        Inserts the given live bus assignment into the database as a temporary
        reference. Assumes that its bus already exists in the database.
        """
        require_state(
            assignment.bus.database_id is not None,
            "The assigned bus should have been inserted into the database."
        )

        with self._db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api.live_bus_assignment
                    (bus, block_id, service_date, status, bike_rack, 
                     last_query_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (bus, block_id, service_date)
                DO UPDATE
                SET status = EXCLUDED.status, bike_rack = EXCLUDED.bike_rack, 
                    last_query_time = EXCLUDED.last_query_time
                WHERE 
                    EXCLUDED.last_query_time >= api.live_bus_assignment.last_query_time
                """,
                (assignment.bus.database_id, assignment.block_id.gtfs_format(),
                 assignment.service_date, int(assignment.status),
                 assignment.bike_rack, assignment.last_query_time)
            )