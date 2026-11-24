from abc import ABC, abstractmethod
from api.domain.inferred_api_data.bus import Bus
from api.domain.inferred_api_data.bus_assignment import BusAssignment
from api.domain.inferred_api_data.live_bus_assignment import LiveBusAssignment


class APIWriter(ABC):
    """
    Persists API domain objects.
    """

    @abstractmethod
    def write_bus(self, bus: Bus) -> None:
        """
        Persists the given bus. If another non-retired bus exists with the
        same tracking number, its status is set to 'retired'.
        """
        pass

    @abstractmethod
    def write_bus_assignment(self, assignment: BusAssignment) -> None:
        """
        Persists the given bus assignment as a historical record. Updates the
        last service date of the associated bus.
        """

    @abstractmethod
    def write_live_bus_assignment(self, assignment: LiveBusAssignment) -> None:
        """
        Persists the given live bus assignment as a temporary reference.
        """