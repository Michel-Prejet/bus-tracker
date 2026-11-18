from datetime import date
from zoneinfo import ZoneInfo
import requests
from typing import Any
from api.parsing.stop_schedule_parser import parse_api_stop_schedule
from global_packages.error_messages import get_err_msg


CRITICAL_STOPS = [
    10159,
    17007,
    40196,
    10803,
    10657,
    61253,
    37003,
    10562,
    10158,
    30893,
    11037,
    40195,
    60475,
    30789,
    10289,
    60672,
    20600,
    62015,
    10907,
    40800,
    60746,
    50617,
    61279,
    50616,
    40889,
    50311,
    50310,
    61278,
    10087,
    37005,
    20200,
    10881,
    20468,
    61277,
    10010,
    50210,
    40466,
    30366,
    40052,
    20456,
    10908,
    10627,
    61155,
    10090,
    10632,
    30078,
    40900,
    50192,
    10001,
    20019,
    60577,
    10131,
    10303,
    20227,
    30364,
    61159
]

def get_stop_schedule(stop_id: str, api_key: str) -> dict[str, Any]:
    url = f"https://api.winnipegtransit.com/v4/stops/{stop_id}/schedule.json"

    response = requests.get(
        url,
        params={"api-key": api_key},
        timeout=15
    )

    response.raise_for_status()

    return response.json()

all_observations = []
for stop_id in CRITICAL_STOPS:
    try:
        schedule = get_stop_schedule(str(stop_id), "")
        observations = parse_api_stop_schedule(
            schedule,
            date.fromisoformat("2026-11-16"),
            ZoneInfo("America/Winnipeg")
        )

        for obs in observations:
            all_observations.append(obs)
    except Exception as e:
        print(get_err_msg(e))

all_observations.sort(key=lambda o: o.bus_tracking_num)
for obs in all_observations:
    if "100" <= obs.bus_tracking_num <= "999":
        print(
            f"Bus {obs.bus_tracking_num}",
            f"\n\tRoute {obs.route_id}",
            f"\n\tStop {obs.stop_id}",
            f"\n\tTrip key {obs.trip_key}",
            f"\n\tDeparture:",
            f"\n\t\tScheduled: {obs.scheduled_departure.offset}",
            f"\n\t\tEstimated: {obs.estimated_departure.offset}",
            f"\n\tCancelled: {str(obs.cancelled)}",
            f"\n\tBike rack: {str(obs.bike_rack)}",
            f"\n\tQuery time: {obs.query_time.offset}"
        )
