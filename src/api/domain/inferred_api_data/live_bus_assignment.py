from datetime import date
from api.domain.inferred_api_data.bus import Bus
from api.domain.inferred_api_data.bus_assignment import BusAssignment
from global_packages.utilities.invariant_helper import require_type
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class LiveBusAssignment:
    """
    Represents an ongoing assignment of a bus to a block, with cancelled and
    bike rack flags.
    """

    def __init__(
        self,
        assignment: BusAssignment,
        cancelled: bool | None,
        bike_rack: bool | None
    ):
        self._assignment = assignment
        self._cancelled = cancelled
        self._bike_rack = bike_rack

        self._check_bus_assignment()

    @property
    def bus(self) -> Bus:
        return self._assignment.bus

    @property
    def block_id(self) -> WinnipegBlockID:
        return self._assignment.block_id

    @property
    def service_date(self) -> date:
        return self._assignment.service_date

    @property
    def cancelled(self) -> bool | None:
        return self._cancelled

    @property
    def bike_rack(self) -> bool | None:
        return self._bike_rack

    def _check_bus_assignment(self) -> None:
        require_type(BusAssignment, bus_assignment=self._assignment)
        require_type(
            bool | None,
            cancelled_status=self._cancelled,
            bike_rack_status=self._bike_rack
        )