from gtfs.domain.values.gtfs_timestamp import GTFSTimestamp
from global_packages.utilities.invariant_helper import require_type, require_non_empty_str, require_state


class BusObservation:
    """
    Represents an API observation recorded by the API parser from the
    live schedule.
    """

    def __init__(
        self,
        bus_tracking_num: str,
        stop_id: str,
        trip_key: str,
        route_id: str,
        query_time: GTFSTimestamp,
        scheduled_arrival: GTFSTimestamp | None,
        estimated_arrival: GTFSTimestamp | None,
        scheduled_departure: GTFSTimestamp | None,
        estimated_departure: GTFSTimestamp | None,
        cancelled: bool | None,
        bike_rack: bool | None
    ):
        self._bus_tracking_num = bus_tracking_num
        self._stop_id = stop_id
        self._trip_key = trip_key
        self._route_id = route_id
        self._scheduled_arrival = scheduled_arrival
        self._estimated_arrival = estimated_arrival
        self._scheduled_departure = scheduled_departure
        self._estimated_departure = estimated_departure
        self._query_time = query_time
        self._cancelled = cancelled
        self._bike_rack = bike_rack

        self._check_bus_observation()

    @property
    def bus_tracking_num(self) -> str:
        return self._bus_tracking_num

    @property
    def stop_id(self) -> str:
        return self._stop_id

    @property
    def trip_key(self) -> str:
        return self._trip_key

    @property
    def route_id(self) -> str:
        return self._route_id

    @property
    def query_time(self) -> GTFSTimestamp:
        return self._query_time

    @property
    def scheduled_arrival(self) -> GTFSTimestamp | None:
        return self._scheduled_arrival

    @property
    def estimated_arrival(self) -> GTFSTimestamp | None:
        return self._estimated_arrival

    @property
    def scheduled_departure(self) -> GTFSTimestamp | None:
        return self._scheduled_departure

    @property
    def estimated_departure(self) -> GTFSTimestamp | None:
        return self._estimated_departure

    @property
    def cancelled(self) -> bool | None:
        return self._cancelled

    @property
    def bike_rack(self) -> bool | None:
        return self._bike_rack

    def _check_bus_observation(self) -> None:
        require_type(
            str,
            bus_tracking_num=self._bus_tracking_num,
            stop_id=self._stop_id,
            trip_key=self._trip_key,
            route_id=self._route_id
        )
        require_type(GTFSTimestamp, query_time=self._query_time)
        require_type(
            GTFSTimestamp | None,
            scheduled_arrival=self._scheduled_arrival,
            estimated_arrival=self._estimated_arrival,
            scheduled_departure=self._scheduled_departure,
            estimated_departure=self._estimated_departure
        )
        require_type(
            bool | None,
            cancelled_status=self._cancelled,
            bike_rack_status=self._bike_rack
        )

        require_non_empty_str(
            bus_tracking_num=self._bus_tracking_num,
            stop_id=self._stop_id,
            trip_key=self._trip_key,
            route_id=self._route_id
        )

        require_state(
            self._scheduled_arrival is not None or self._scheduled_departure is not None,
            "The scheduled arrival and departure times for the bus "
            "observation cannot both be None."
        )