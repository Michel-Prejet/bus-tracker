from datetime import timedelta, date
from invariant_helper import require_not_none, require_state


class GTFSTimestamp:
    """
    Represents a GTFS timestamp with a service date and an offset computed from
    12 hours before noon on that service date. Offsets can take on any
    non-negative value, including those beyond 24:00:00.
    """

    def __init__(self, service_date: date, offset: timedelta):
        self._service_date = service_date
        self._offset = offset

        self._check_gtfs_timestamp()

    @property
    def service_date(self) -> date:
        return self._service_date

    @property
    def offset(self) -> timedelta:
        return self._offset

    def _check_gtfs_timestamp(self) -> None:
        require_not_none(
            service_date=self._service_date,
            offset=self._offset
        )

        require_state(
            type(self._service_date) is date,
            "Service date should be a date object (not datetime)."
        )

        require_state(
            self._offset >= timedelta(0),
            "Offset should not be negative."
        )
