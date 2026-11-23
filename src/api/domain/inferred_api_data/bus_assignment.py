from datetime import date
from api.domain.inferred_api_data.bus import Bus
from global_packages.utilities.invariant_helper import require_type
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class BusAssignment:
    """
    Represents an assignment of a bus to a block on a specific date.
    """
    def __init__(
        self,
        bus: Bus,
        block_id: WinnipegBlockID,
        service_date: date
    ):
        self._bus = bus
        self._block_id = block_id
        self._service_date = service_date

        self._check_bus_assignment()

    @property
    def bus(self) -> Bus:
        return self._bus

    @property
    def block_id(self) -> WinnipegBlockID:
        return self._block_id

    @property
    def service_date(self) -> date:
        return self._service_date

    def _check_bus_assignment(self) -> None:
        require_type(Bus, bus=self._bus)
        require_type(WinnipegBlockID, block_id=self._block_id)
        require_type(date, service_date=self._service_date)