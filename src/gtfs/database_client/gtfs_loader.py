from abc import ABC, abstractmethod
from datetime import timedelta
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class GTFSLoader(ABC):
    """
    Loads GTFS domain objects from persistent storage.
    """

    @abstractmethod
    def get_blocks_from_observation(
            self,
            stop_id: str,
            service_id: str,
            scheduled_departure: timedelta
    ) -> list[WinnipegBlockID]:
        """
        Returns the blocks in which a stop visit occurs matching the given
        stop ID, service pattern ID, and scheduled departure time.
        """
        pass