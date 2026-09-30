from datetime import date
from gtfs.domain.enums.service_pattern_override_type import ServicePatternOverrideType
from utilities.invariant_helper import require_not_none


class ServicePatternOverride:
    """
    Represents instructions for a date with an exceptional service pattern.
    Stores a date and a type which indicates whether service should be added
    or remove from that date.
    """

    def __init__(self, override_date: date, override_type: ServicePatternOverrideType):
        self._date = override_date
        self._type = override_type

        self._check_service_pattern_override()

    @property
    def date(self) -> date:
        return self._date

    @property
    def type(self) -> ServicePatternOverrideType:
        return self._type

    def _check_service_pattern_override(self) -> None:
        require_not_none(
            service_pattern_override_date=self._date,
            service_pattern_override_type=self._type
        )