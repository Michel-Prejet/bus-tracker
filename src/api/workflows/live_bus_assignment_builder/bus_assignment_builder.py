from datetime import date, timedelta
from zoneinfo import ZoneInfo
from api.domain.inferred_api_data.live_bus_assignment import LiveBusAssignment
from api.domain.raw_api_data.bus_observation import BusObservation


def todo(
    observations_by_bus: dict[str, list[BusObservation]],
    service_id: str,
    service_date: date,
    current_time: timedelta,
    timezone: ZoneInfo
) -> LiveBusAssignment | None:
    pass


