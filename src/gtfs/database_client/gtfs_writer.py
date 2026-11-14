from abc import ABC, abstractmethod
from gtfs.domain.agency import Agency
from gtfs.domain.feed_info import FeedInfo
from gtfs.domain.route import Route
from gtfs.domain.service_pattern.service_pattern import ServicePattern
from gtfs.domain.shape.shape import Shape
from gtfs.domain.stop import Stop
from gtfs.domain.trip.trip import Trip


class GTFSWriter(ABC):
    """
    Persists GTFS domain objects.
    """

    @abstractmethod
    def write_agency(self, agency: Agency) -> None:
        """
        Persists the given agency.
        """
        pass

    @abstractmethod
    def write_feed_info(self, feed_info: FeedInfo) -> None:
        """
        Persists the given feed info.
        """
        pass

    @abstractmethod
    def write_route(self, route: Route) -> None:
        """
        Persists the given route.
        """
        pass

    @abstractmethod
    def write_stop(self, stop: Stop) -> None:
        """
        Persists the given stop.
        """
        pass

    @abstractmethod
    def write_service_pattern_and_overrides(
            self, service_pattern: ServicePattern
    ) -> None:
        """
        Persists the given service pattern and the service pattern overrides
        therein.
        """
        pass

    @abstractmethod
    def write_shape_and_points(self, shape: Shape) -> None:
        """
        Persists the given shape and the shape points therein.
        """
        pass

    @abstractmethod
    def write_trip_and_stop_visits(self, trip: Trip) -> None:
        """
        Persists the given trip and the stop visits therein.
        """
        pass
