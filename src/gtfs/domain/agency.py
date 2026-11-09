from zoneinfo import ZoneInfo
from gtfs.domain.values.url import Url
from invariant_helper import require_not_none, require_non_empty_str, require_type


class Agency:
    """
    Stores static information about a transit agency, such as its name,
    URL, and timezone.
    """

    def __init__(
            self,
            agency_name: str,
            agency_url: Url,
            timezone: ZoneInfo,
    ):
        self._name = agency_name
        self._agency_url = agency_url
        self._timezone = timezone

        self._check_agency_info()

    @property
    def name(self) -> str:
        return self._name

    @property
    def agency_url(self) -> Url:
        return self._agency_url

    @property
    def timezone(self) -> ZoneInfo:
        return self._timezone

    def _check_agency_info(self) -> None:
        require_type(str, agency_name=self._name)
        require_type(Url, agency_url=self._agency_url)
        require_type(ZoneInfo, agency_timezone=self._timezone)

        require_non_empty_str(agency_name=self._name)