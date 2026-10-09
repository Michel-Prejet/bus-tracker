from datetime import date, datetime, time, timezone, timedelta
from zoneinfo import ZoneInfo
from utilities.invariant_helper import require_not_none, require_state


AGENCY_TIMEZONE = ZoneInfo("America/Winnipeg") # TODO: import agency timezone

class GTFSTimestamp:
    """
    Abstracts GTFS Time logic. Stores a service date and an offset relative to
    12 hours before noon on that service date.

    Some rules about GTFS times:
    * The offset can take on any non-negative value, including those above
      24:00:00. As a consequence, one GTFS service day can extend into
      subsequent calendar dates.
    * The offset is calculated from 12 hours before noon on the service day.
      Usually this is just midnight (00:00:00), but because of DST we cannot
      make this assumption.
    """

    def __init__(self, service_date: date, timestamp: datetime):
        require_not_none(
            service_date=service_date,
            timestamp=timestamp
        )
        require_state(
            type(service_date) is date,
            "Service date should be a date object (not datetime)."
        )
        require_state(
            timestamp.tzinfo is not None and
            timestamp.utcoffset() is not None,
            "Timestamp should have a timezone."
        )

        self._service_date = service_date
        self._offset = self._timestamp_to_offset(service_date, timestamp)

        self._check_gtfs_timestamp()

    def __lt__(self, other: "GTFSTimestamp") -> bool:
        """
        Returns True if this GTFS timestamp occurs before the given instance
        (when converted to a regular datetime); returns False otherwise.
        """
        require_not_none(gtfs_timestamp_to_compare=other)

        return (self.as_datetime().astimezone(timezone.utc)
                < other.as_datetime().astimezone(timezone.utc))

    @property
    def service_date(self) -> date:
        return self._service_date

    @property
    def offset(self) -> timedelta:
        return self._offset

    def as_datetime(self) -> datetime:
        """
        Returns a datetime object representing the calendar date and time
        corresponding to this GTFS timestamp.
        """
        return self._offset_to_timestamp(
            self._service_date,
            self._offset
        )

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

    @staticmethod
    def _timestamp_to_offset(service_date: date, timestamp: datetime) -> timedelta:
        """
        Returns the offset as a timedelta object representing the amount of time
        elapsed since 12 hours before noon on the service date.

        * Note: 12 hours before noon is NOT always midnight due to DST; this is
        why we don't simply use midnight in this calculation.
        """
        service_day_start = GTFSTimestamp._get_service_day_start(service_date)

        return timestamp.astimezone(timezone.utc) - service_day_start

    @staticmethod
    def _offset_to_timestamp(service_date: date, offset: timedelta) -> datetime:
        """
        Returns a datetime object representing the calendar date and time
        corresponding to the given service date and offset.
        """
        service_day_start = GTFSTimestamp._get_service_day_start(service_date)

        return (service_day_start + offset).astimezone(AGENCY_TIMEZONE)

    @staticmethod
    def _get_service_day_start(service_date: date) -> datetime:
        """
        Returns a UTC datetime object corresponding to the start of the given
        service day as per GTFS rules.
        The start of a service day is defined as 12 hours before noon on that
        date, which does not always correspond to midnight due to DST.
        """
        service_day_noon = datetime.combine(
            service_date,
            time(hour=12),
            tzinfo=AGENCY_TIMEZONE
        )

        return service_day_noon.astimezone(timezone.utc) - timedelta(hours=12)