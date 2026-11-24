from datetime import date, timedelta
from api.domain.enums.assignment_status import AssignmentStatus
from api.domain.inferred_api_data.bus import Bus
from api.domain.inferred_api_data.bus_assignment import BusAssignment
from global_packages.utilities.invariant_helper import require_type, require_state
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


class LiveBusAssignment:
    """
    Represents an ongoing assignment of a bus to a block, with cancelled and
    bike rack flags.
    """

    def __init__(
        self,
        assignment: BusAssignment,
        status: AssignmentStatus,
        bike_rack: bool | None,
        last_query_time: timedelta,
    ):
        self._assignment = assignment
        self._status = status
        self._bike_rack = bike_rack
        self._last_query_time = last_query_time

        self._check_bus_assignment()

    @property
    def bus(self) -> Bus:
        return self._assignment.bus

    @property
    def block_id(self) -> WinnipegBlockID:
        return self._assignment.block_id

    @property
    def status(self) -> AssignmentStatus:
        return self._status

    @property
    def service_date(self) -> date:
        return self._assignment.service_date
    @property
    def bike_rack(self) -> bool | None:
        return self._bike_rack

    @property
    def last_query_time(self) -> timedelta:
        return self._last_query_time

    def _check_bus_assignment(self) -> None:
        require_type(BusAssignment, bus_assignment=self._assignment)
        require_type(AssignmentStatus, bus_assignment_status=self._status)
        require_type(bool | None, bike_rack_status=self._bike_rack)
        require_type(timedelta, last_query_time=self._last_query_time)

        require_state(
            self._last_query_time >= timedelta(0),
            "Last query time should not be negative."
        )