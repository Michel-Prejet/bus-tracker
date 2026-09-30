from gtfs.domain.values.date_range import DateRange
from gtfs.domain.values.url import Url
from utilities.invariant_helper import require_not_none, require_non_empty_str


class FeedInfo:
    """
    Stores static information about the GTFS feed itself, such as the
    publisher's name and website URL, the language and start/end dates of the
    feed, and an email address for feed inquiries.
    """

    def __init__(
            self,
            publisher_name: str,
            publisher_url: Url,
            language: str,
            active_period: DateRange | None,
            contact_email: str | None
    ):
        self._publisher_name = publisher_name
        self._publisher_url = publisher_url
        self._language = language
        self._active_period = active_period
        self._contact_email = contact_email

        self._check_feed_info()

    @property
    def publisher_name(self) -> str:
        return self._publisher_name

    @property
    def publisher_url(self) -> Url:
        return self._publisher_url

    @property
    def language(self) -> str:
        return self._language

    @property
    def active_period(self) -> DateRange | None:
        return self._active_period

    @property
    def contact_email(self) -> str | None:
        return self._contact_email

    def _check_feed_info(self) -> None:
        require_not_none(
            feed_publisher_name=self._publisher_name,
            feed_publisher_url=self._publisher_url,
            feed_language=self._language
        )

        require_non_empty_str(feed_publisher_name=self._publisher_name)

        require_non_empty_str(feed_language=self._language)

        if self._contact_email is not None:
            require_non_empty_str(feed_contact_email=self._contact_email)