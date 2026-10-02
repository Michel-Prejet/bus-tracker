from zoneinfo import ZoneInfo
from gtfs.domain.values.email import Email
from gtfs.domain.values.language import Language
from gtfs.domain.values.url import Url
from utilities.invariant_helper import require_not_none, require_non_empty_str


class AgencyInfo:
    """
    Stores static information about a transit agency, such as its name,
    website and fare URL, timezone, language, and contact information.
    """

    def __init__(
            self,
            agency_id: str | None,
            name: str,
            agency_url: Url,
            fare_url: Url | None,
            timezone: ZoneInfo,
            language: Language | None,
            phone_num: str | None,
            email: Email | None
    ):
        self._agency_id = agency_id
        self._name = name
        self._agency_url = agency_url
        self._fare_url = fare_url
        self._timezone = timezone
        self._language = language
        self._phone_num = phone_num
        self._email = email

        self._check_agency_info()

    @property
    def id(self) -> str | None:
        return self._agency_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def agency_url(self) -> Url:
        return self._agency_url

    @property
    def fare_url(self) -> Url | None:
        return self._fare_url

    @property
    def timezone(self) -> ZoneInfo:
        return self._timezone

    @property
    def language(self) -> Language | None:
        return self._language

    @property
    def phone_num(self) -> str | None:
        return self._phone_num

    @property
    def email(self) -> Email | None:
        return self._email

    def _check_agency_info(self) -> None:
        require_not_none(
            agency_name=self._name,
            agency_url=self._agency_url,
            agency_timezone=self._timezone
        )

        if self._agency_id is not None:
            require_non_empty_str(agency_id=self._agency_id)

        require_non_empty_str(agency_name=self._name)

        if self._phone_num is not None:
            require_non_empty_str(agency_phone_number=self._phone_num)