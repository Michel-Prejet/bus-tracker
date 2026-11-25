from datetime import timedelta
from typing import Protocol
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class BlockCandidateProvider(Protocol):
    def get_possible_block_ids(
        self,
        service_id: str,
        stop_id: str,
        scheduled_arrival: timedelta | None,
        scheduled_departure: timedelta | None
    ) -> list[WinnipegBlockID] | None:
        """
        Returns a list of all block IDs containing a stop visit matching the
        given service ID, stop ID, and scheduled arrival/departure times.
        """
        pass