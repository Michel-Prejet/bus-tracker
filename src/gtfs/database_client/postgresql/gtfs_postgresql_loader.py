from datetime import timedelta
from psycopg import Connection
from psycopg.rows import dict_row
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

    def get_blocks_from_observation(
        self,
        stop_id: str,
        service_id: str,
        scheduled_departure: timedelta
    ) -> list[WinnipegBlockID]:
        """
        Loads WinnipegBlockIDs from the database for which there exists a trip
        with the given service pattern ID associated with a stop visit matching
        the given stop ID and scheduled departure time.
        """
        with self._db.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT DISTINCT gtfs.trip.block_id
                FROM gtfs.trip
                JOIN gtfs.stop_visit ON gtfs.trip.id = gtfs.stop_visit.trip
                WHERE
                    gtfs.trip.service_pattern = %s AND
                    gtfs.stop_visit.stop = %s AND
                    gtfs.stop_visit.scheduled_departure = %s
                """,
                (service_id, stop_id, scheduled_departure)
            )

            return [
                WinnipegBlockID(result["block_id"])
                for result in cursor.fetchall()
            ]