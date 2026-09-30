from datetime import date
from gtfs.domain.enums.day_of_week import DayOfWeek
from gtfs.domain.enums.service_pattern_override_type import ServicePatternOverrideType
from gtfs.domain.service_pattern_override import ServicePatternOverride
from gtfs.domain.values.date_range import DateRange
from gtfs.domain.values.gtfs_timestamp import GTFSTimestamp
from utilities.invariant_helper import require_not_none, require_non_empty_str, require_state


class ServicePattern:
    """
    Represents a service pattern followed by transit on a specific day of the
    week (defines the set of trips that will occur on that day).
    Stores the service pattern's unique ID, the days of the week it is active,
    and the date range for which it is valid. Takes into account any service
    pattern overrides (for example, on holidays) which can either add or remove
    this service pattern on a specific day.

    Important GTFS invariants for this object:
    * Each date can be associated with at most one service pattern override.
    """

    def __init__(
            self,
            service_id: str,
            weekdays_active: set[DayOfWeek],
            active_period: DateRange,
            overrides: dict[date, ServicePatternOverride]):
        self._service_id = service_id
        self._weekdays_active = weekdays_active
        self._active_period = active_period
        self._overrides = overrides

        self._check_service_pattern()

    @property
    def service_id(self) -> str:
        return self._service_id

    def is_active(self, timestamp: GTFSTimestamp) -> bool:
        """
        Returns True if this service pattern is applicable during the
        given GTFS timestamp, taking into account any service pattern
        overrides.
        """
        require_not_none(
            timestamp=timestamp
        )

        service_date = timestamp.service_date

        if service_date in self._overrides:
            match self._overrides[service_date].type:
                case ServicePatternOverrideType.ADD:
                    return True
                case ServicePatternOverrideType.REMOVE:
                    return False

        return (
            service_date in self._active_period and
            DayOfWeek.from_date(service_date) in self._weekdays_active
        )

    def _check_service_pattern(self) -> None:
        require_not_none(
            service_id=self._service_id,
            list_of_weekdays_active=self._weekdays_active,
            active_date_range=self._active_period,
            override_dict=self._overrides
        )

        for day in self._weekdays_active:
            require_not_none(
                weekday_in_list=day
            )

        for date_key, override in self._overrides.items():
            require_not_none(
                date_key_in_override_dict=date_key,
                service_pattern_override_in_dict=override
            )
            require_state(
                date_key == override.date,
                "Date key should correspond to the date of the service pattern override."
            )

        require_non_empty_str(
            service_id=self._service_id
        )