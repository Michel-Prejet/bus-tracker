from datetime import date
from gtfs.domain.enums.day_of_week import DayOfWeek
from gtfs.domain.enums.service_pattern_override_type import ServicePatternOverrideType
from gtfs.domain.service_pattern.service_pattern_override import ServicePatternOverride
from gtfs.domain.values.date_range import DateRange
from gtfs.domain.values.gtfs_timestamp import GTFSTimestamp
from invariant_helper import require_non_empty_str, require_state, require_type


class ServicePattern:
    """
    Represents a service pattern followed by transit on a specific day of the
    week (defines the set of trips that will occur on that day).
    Stores the service pattern's unique ID, the days of the week it is active,
    and the date range for which it is valid. Takes into account any service
    pattern overrides (for example, on holidays) which can either add or remove
    this service pattern on a specific day.
    """

    def __init__(
            self,
            service_id: str,
            weekdays_active: set[DayOfWeek],
            active_period: DateRange
        ):
        self._service_id = service_id
        self._weekdays_active = weekdays_active
        self._active_period = active_period
        self._overrides: dict[date, ServicePatternOverride] = {}

        self._check_service_pattern()

    @property
    def service_id(self) -> str:
        return self._service_id

    @property
    def weekdays_active(self) -> set[DayOfWeek]:
        return self._weekdays_active

    @property
    def active_period(self) -> DateRange:
        return self._active_period

    @property
    def overrides(self) -> list[ServicePatternOverride]:
        """
        Returns a shallow copy of the list of service pattern overrides for
        this service pattern.
        """
        return list(self._overrides.values()).copy()

    def is_active(self, timestamp: GTFSTimestamp) -> bool:
        """
        Returns True if this service pattern is applicable during the
        given GTFS timestamp, taking into account any service pattern
        overrides.
        """
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

    def add_override(self, override: ServicePatternOverride) -> None:
        """
        Adds a given override/exception for this service pattern.
        Assumes that no override has already been assigned to the same date
        as that of the given service pattern override.
        """
        require_state(
            override.date not in self._overrides,
            "The same date cannot be associated twice with the same "
            "service pattern override."
        )

        self._overrides[override.date] = override

        self._check_service_pattern()

    def _check_service_pattern(self) -> None:
        require_type(str, service_id=self._service_id)
        require_type(set, active_weekday_set=self._weekdays_active)
        require_type(DateRange, active_date_range=self._active_period)
        require_type(
            dict,
            service_pattern_override_dictionary=self._overrides
        )

        for day in self._weekdays_active:
            require_type(DayOfWeek, day_in_active_weekday_set=day)

        for date_key, override in self._overrides.items():
            require_type(date, date_key_in_override_dict=date_key)
            require_type(ServicePatternOverride,
                         service_pattern_override_in_dict=override)

            require_state(
                date_key == override.date,
                "Date key should correspond to the date of the service pattern override."
            )

        require_non_empty_str(
            service_id=self._service_id
        )