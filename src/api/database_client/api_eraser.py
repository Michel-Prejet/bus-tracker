from abc import ABC, abstractmethod
from datetime import datetime


class APIEraser(ABC):
    """
    Deletes API domain objects.
    """

    @abstractmethod
    def delete_live_bus_assignments_older_than(self, timestamp: datetime) -> None:
        pass