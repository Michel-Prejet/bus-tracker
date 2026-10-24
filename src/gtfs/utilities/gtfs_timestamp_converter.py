from datetime import date, timedelta, datetime, timezone, time
from zoneinfo import ZoneInfo
from invariant_helper import require_not_none, require_state


"""
Functions used to convert between GTFS timestamps and standard datetime
objects. 

Some rules about GTFS times:
    * The offset can take on any non-negative value, including those above
      24:00:00. As a consequence, one GTFS service day can extend into
      subsequent calendar dates.
    * The offset is calculated from 12 hours before noon on the service day.
      Usually this is just midnight (00:00:00), but because of DST we cannot
      make this assumption.
"""

def std_timestamp_to_gtfs_offset(service_date: date, timestamp: datetime,
                                 agency_timezone: ZoneInfo) -> timedelta:
    """
    Returns the offset as a timedelta object representing the amount of time
    elapsed since 12 hours before noon on the service date.

    * Note: 12 hours before noon is NOT always midnight due to DST; this is
    why we don't simply use midnight in this calculation.
    """
    require_not_none(
        service_date=service_date,
        datetime_timestamp=timestamp,
        agency_timezone=agency_timezone
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

    service_day_start = _get_service_day_start(service_date, agency_timezone)

    return timestamp.astimezone(timezone.utc) - service_day_start

def gtfs_offset_to_std_timestamp(service_date: date, offset: timedelta,
                                 agency_timezone: ZoneInfo) -> datetime:
    """
    Returns a datetime object representing the calendar date and time
    corresponding to the given service date and offset.
    """
    require_not_none(
        service_date=service_date,
        offset=offset,
        agency_timezone=agency_timezone
    )
    require_state(
        type(service_date) is date,
        "Service date should be a date object (not datetime)."
    )
    require_state(
        offset >= timedelta(0),
        "Offset should not be negative."
    )

    service_day_start = _get_service_day_start(service_date, agency_timezone)

    return (service_day_start + offset).astimezone(agency_timezone)

def _get_service_day_start(service_date: date, agency_timezone: ZoneInfo) -> datetime:
    """
    Returns a UTC datetime object corresponding to the start of the given
    service day as per GTFS rules.
    The start of a service day is defined as 12 hours before noon on that
    date, which does not always correspond to midnight due to DST.
    """
    NOON=time(hour=12)
    HOURS_BEFORE_NOON = 12

    service_day_noon = datetime.combine(
        service_date,
        NOON,
        tzinfo=agency_timezone
    )

    return (service_day_noon.astimezone(timezone.utc)
            - timedelta(hours=HOURS_BEFORE_NOON))