from datetime import timedelta

from psycopg import Connection, sql
from psycopg.rows import dict_row
from api.domain.raw_api_data.bus_observation import BusObservation
from gtfs.database_client.gtfs_loader import GTFSLoader
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class GTFSPostgreSQLLoader(GTFSLoader):
    """
    Opens a connection to the PostgreSQL database and loads GTFS data
    into memory.
    """

    def __init__(self, db: Connection):
        self._db = db

    def __enter__(self):
        self._db.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._db.__exit__(exc_type, exc_value, traceback)

    def get_possible_block_ids(
            self,
            service_id: str,
            stop_id: str,
            scheduled_arrival: timedelta | None,
            scheduled_departure: timedelta | None
    ) -> list[WinnipegBlockID]:
        """
        Loads WinnipegBlockIDs from the database for which there exists a trip
        with the given service pattern ID associated with a stop visit matching
        the given stop ID and scheduled arrival/departure times. Null times
        are not considered.
        """
        if scheduled_arrival is None and scheduled_departure is None:
            return []

        with self._db.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT DISTINCT gtfs.trip.block_id
                FROM gtfs.trip
                JOIN gtfs.stop_visit ON gtfs.trip.id = gtfs.stop_visit.trip
                WHERE
                    gtfs.trip.service_pattern = %s AND
                    gtfs.stop_visit.stop = %s AND
                    (%s::INTERVAL IS NULL OR gtfs.stop_visit.scheduled_departure = %s) AND
                    (%s::INTERVAL IS NULL OR gtfs.stop_visit.scheduled_arrival = %s)
                """,
                (service_id, stop_id, scheduled_departure, scheduled_departure,
                 scheduled_arrival, scheduled_arrival)
            )

            return [
                WinnipegBlockID(raw["block_id"])
                for raw in cursor.fetchall()
            ]


