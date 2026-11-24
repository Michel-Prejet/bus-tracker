from abc import ABC, abstractmethod
from api.domain.inferred_api_data.bus import Bus


class APILoader(ABC):
    """
    Loads API domain objects from persistent storage.
    """

    @abstractmethod
    def get_bus_by_tracking_number(self, tracking_number: str) -> Bus | None:
        """
        Loads the non-retired bus with the given tracking number from persistent
        storage, or None if no such bus exists.
        """
        pass