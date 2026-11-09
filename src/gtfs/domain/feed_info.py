from datetime import date
from gtfs.domain.values.date_range import DateRange
from gtfs.domain.values.url import Url
from gtfs.constants.gtfs_constants import UNBOUNDED_START_DATE, UNBOUNDED_END_DATE
from invariant_helper import require_non_empty_str, require_type


class FeedInfo:
    """
    Stores static information about the GTFS feed itself, such as the
    publisher's name and website URL, the language and start/end dates of the
    feed, and an email address for feed inquiries.

    Note: if the start and/or end dates are null, they will be replaced with
    default/sentinel values.
    """

    def __init__(
            self,
            publisher_name: str,
            publisher_url: Url,
            start_date: date | None,
            end_date: date | None
    ):
        self._publisher_name = publisher_name
        self._publisher_url = publisher_url
        self._active_period = DateRange(
            start_date=start_date if start_date is not None else UNBOUNDED_START_DATE,
            end_date=end_date if end_date is not None else UNBOUNDED_END_DATE
        )

        self._check_feed_info()

    @property
    def publisher_name(self) -> str:
        return self._publisher_name

    @property
    def publisher_url(self) -> Url:
        return self._publisher_url

    @property
    def active_period(self) -> DateRange:
        return self._active_period

    def _check_feed_info(self) -> None:
        require_type(str, feed_publisher_name=self._publisher_name)
        require_type(Url, feed_publisher_url=self._publisher_url)
        require_type(DateRange, feed_active_period=self._active_period)

        require_non_empty_str(feed_publisher_name=self._publisher_name)