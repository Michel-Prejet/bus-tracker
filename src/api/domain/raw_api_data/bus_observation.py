from datetime import date, timedelta
from api.domain.raw_api_data.live_stop_visit import LiveStopVisit
from global_packages.utilities.invariant_helper import require_type, require_state, require_non_empty_str


class BusObservation:
    """
    Detailed information for a live stop visit scheduled for a specific bus,
    read from the Winnipeg Transit API.
    """

    def __init__(
        self,
        stop_visit: LiveStopVisit,
        service_date: date,
        bus_tracking_num: str,
        trip_key: str,
        route_id: str,
        cancelled: bool | None,
        bike_rack: bool | None,
        query_time: timedelta
    ):
        self._stop_visit = stop_visit
        self._service_date = service_date
        self._bus_tracking_num = bus_tracking_num
        self._trip_key = trip_key
        self._route_id = route_id
        self._cancelled = cancelled
        self._bike_rack = bike_rack
        self._query_time = query_time

        self._check_bus_observation()

    @property
    def stop_id(self) -> str:
        return self._stop_visit.stop_id

    @property
    def scheduled_departure(self) -> timedelta | None:
        return self._stop_visit.scheduled_departure

    @property
    def scheduled_arrival(self) -> timedelta | None:
        return self._stop_visit.scheduled_arrival

    @property
    def estimated_departure(self) -> timedelta | None:
        return self._stop_visit.estimated_departure

    @property
    def estimated_arrival(self) -> timedelta | None:
        return self._stop_visit.estimated_arrival

    @property
    def service_date(self) -> date:
        return self._service_date

    @property
    def bus_tracking_num(self) -> str:
        return self._bus_tracking_num

    @property
    def trip_key(self) -> str:
        return self._trip_key

    @property
    def route_id(self) -> str:
        return self._route_id

    @property
    def cancelled(self) -> bool | None:
        return self._cancelled

    @property
    def bike_rack(self) -> bool | None:
        return self._bike_rack

    @property
    def query_time(self) -> timedelta:
        return self._query_time

    def _check_bus_observation(self) -> None:
        require_type(LiveStopVisit, live_stop_visit=self._stop_visit)
        require_type(date, service_date=self._service_date)
        require_type(
            str,
            bus_tracking_number=self._bus_tracking_num,
            trip_key=self._trip_key,
            route_id=self._route_id
        )
        require_type(
            bool | None,
            cancelled_flag=self._cancelled,
            bike_rack_flag=self._bike_rack
        )
        require_type(timedelta, query_time=self._query_time)

        require_non_empty_str(
            bus_tracking_number=self._bus_tracking_num,
            trip_key=self._trip_key,
            route_id=self._route_id
        )

        require_state(
            self._query_time >= timedelta(0),
            "Query time should not be negative."
        )

