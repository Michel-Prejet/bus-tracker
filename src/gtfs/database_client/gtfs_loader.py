from abc import ABC, abstractmethod
from datetime import timedelta
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class GTFSLoader(ABC):
    """
    Loads GTFS domain objects from persistent storage.
    """

    @abstractmethod
    def get_possible_block_ids(
            self,
            service_id: str,
            stop_id: str,
            scheduled_arrival: timedelta | None,
            scheduled_departure: timedelta | None
    ) -> list[WinnipegBlockID]:
        """
        Returns the blocks in which a stop visit occurs matching the given
        stop ID, service pattern ID, and scheduled arrival/departure times.
        Null times are not considered.
        """
        pass