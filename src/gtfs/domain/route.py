from gtfs.domain.enums.route_types import RouteType
from gtfs.domain.values.colour import Colour
from gtfs.domain.values.url import Url
from utilities.invariant_helper import require_not_none, require_state, require_non_empty_str


DEFAULT_ROUTE_BACKGROUND_COLOUR = Colour("FFFFFF")
DEFAULT_ROUTE_TEXT_COLOUR = Colour("000000")

class Route:
    """
    Represents a route read from the GTFS with an ID, a short and long name,
    a type, a URL, background and text colours, and a sort order.

    The official GTFS invariants for this object are as follows:
    * The ID cannot be None or empty.
    * The short and long names cannot both be None, and whichever names are
      present cannot be empty.
    * The route type cannot be None.
    * If the background colour is None, it is set to the default value of FFFFFF.
    * If the text colour is None, it is set to the default value of 000000.
    * If the sort order is not None, it must be non-negative.
    """

    def __init__(
            self,
            route_id: str,
            short_name: str | None,
            long_name: str | None,
            route_type: RouteType,
            route_url: Url | None,
            background_colour: Colour | None,
            text_colour: Colour | None,
            sort_order: int | None
    ):
        self._route_id = route_id
        self._short_name = short_name
        self._long_name = long_name
        self._route_type = route_type
        self._route_url = route_url
        self._background_colour = (
            background_colour
            if background_colour is not None
            else DEFAULT_ROUTE_BACKGROUND_COLOUR
        )
        self._text_colour = (
            text_colour
            if text_colour is not None
            else DEFAULT_ROUTE_TEXT_COLOUR
        )
        self._sort_order = sort_order

        self._check_route()

    @property
    def id(self) -> str:
        return self._route_id

    @property
    def short_name(self) -> str | None:
        return self._short_name

    @property
    def long_name(self) -> str | None:
        return self._long_name

    @property
    def type(self) -> RouteType:
        return self._route_type

    @property
    def url(self) -> Url | None:
        return self._route_url

    @property
    def background_colour(self) -> Colour:
        return self._background_colour

    @property
    def text_colour(self) -> Colour:
        return self._text_colour

    @property
    def sort_order(self) -> int | None:
        return self._sort_order

    def _check_route(self) -> None:
        require_not_none(
            route_id=self._route_id,
            route_type=self._route_type,
            route_background_colour=self._background_colour,
            route_text_colour=self._text_colour
        )

        require_non_empty_str(
            route_id=self._route_id
        )

        require_state(
            self._short_name is not None or self._long_name is not None,
            "Route must contain a short name and/or a long name."
        )
        if self._short_name is not None:
            require_non_empty_str(route_short_name=self._short_name)
        if self._long_name is not None:
            require_non_empty_str(route_long_name=self._long_name)

        if self._sort_order is not None:
            require_state(
                self._sort_order >= 0,
                "Route sort order should be a non-negative integer."
            )