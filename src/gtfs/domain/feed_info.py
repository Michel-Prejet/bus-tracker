from datetime import date
from gtfs.domain.values.date_range import DateRange
from gtfs.domain.values.email import Email
from gtfs.domain.values.language import Language
from gtfs.domain.values.url import Url
from gtfs.gtfs_constants import UNBOUNDED_START_DATE, UNBOUNDED_END_DATE
from utilities.invariant_helper import require_not_none, require_non_empty_str


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
            language: Language,
            start_date: date | None,
            end_date: date | None,
            contact_email: Email | None
    ):
        self._publisher_name = publisher_name
        self._publisher_url = publisher_url
        self._language = language
        self._active_period = DateRange(
            start_date=start_date if start_date is not None else UNBOUNDED_START_DATE,
            end_date=end_date if end_date is not None else UNBOUNDED_END_DATE
        )
        self._contact_email = contact_email

        self._check_feed_info()

    @property
    def publisher_name(self) -> str:
        return self._publisher_name

    @property
    def publisher_url(self) -> Url:
        return self._publisher_url

    @property
    def language(self) -> Language:
        return self._language

    @property
    def active_period(self) -> DateRange:
        return self._active_period

    @property
    def contact_email(self) -> Email | None:
        return self._contact_email

    def _check_feed_info(self) -> None:
        require_not_none(
            feed_publisher_name=self._publisher_name,
            feed_publisher_url=self._publisher_url,
            feed_language=self._language,
            active_period=self._active_period
        )

        require_non_empty_str(feed_publisher_name=self._publisher_name)