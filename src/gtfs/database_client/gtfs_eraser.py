from abc import ABC, abstractmethod


class GTFSEraser(ABC):
    """
    Deletes GTFS domain objects.
    """

    @abstractmethod
    def clear_tables(self) -> None:
        """
        Deletes all persisted data.
        """
        pass