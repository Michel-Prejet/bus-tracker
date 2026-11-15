from api.domain.bus import Bus
from gtfs.domain.stop import Stop
from gtfs.domain.values.gtfs_timestamp import GTFSTimestamp
from invariant_helper import require_type, require_non_empty_str, require_state


class BusObservation:
    """
    Represents an API observation recorded by the API parser from the
    live schedule.
    """

    def __init__(
        self,
        bus: Bus,
        stop: Stop,
        trip_key: str,
        query_time: GTFSTimestamp,
        scheduled_arrival: GTFSTimestamp | None,
        estimated_arrival: GTFSTimestamp | None,
        scheduled_departure: GTFSTimestamp | None,
        estimated_departure: GTFSTimestamp | None,
        cancelled: bool | None,
        bike_rack: bool | None
    ):
        self._bus = bus
        self._stop = stop
        self._trip_key = trip_key
        self._scheduled_arrival = scheduled_arrival
        self._estimated_arrival = estimated_arrival
        self._scheduled_departure = scheduled_departure
        self._estimated_departure = estimated_departure
        self._query_time = query_time
        self._cancelled = cancelled
        self._bike_rack = bike_rack

        self._check_bus_observation()

    @property
    def bus(self) -> Bus:
        return self._bus

    @property
    def stop(self) -> Stop:
        return self._stop

    @property
    def trip_key(self) -> str:
        return self._trip_key

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
        require_type(Bus, bus=self._bus)
        require_type(Stop, stop=self._stop)
        require_type(str, trip_key=self._trip_key)
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

        require_non_empty_str(trip_key=self._trip_key)

        require_state(
            self._scheduled_arrival is not None or self._scheduled_departure is not None,
            "The scheduled arrival and departure times for the bus "
            "observation cannot both be None."
        )
