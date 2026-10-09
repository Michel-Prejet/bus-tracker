from gtfs.gtfs_constants import WPG_BLOCK_ID_TOKEN_DELIMITER, WPG_BLOCK_ID_NUM_TOKENS, WPG_BLOCK_ID_SERVICE_ID_TOKEN_INDEX, \
    WPG_BLOCK_ID_ROUTE_FAMILY_TOKEN_INDEX, WPG_BLOCK_ID_NUMBER_TOKEN_INDEX
from utilities.invariant_helper import require_not_none, require_state, require_non_empty_str


class WinnipegBlockID:
    """
    Represents a block ID with formatting specific to Winnipeg Transit. Consists
    of three tokens: a service ID, a route family, and a number identifying the
    block within its route family. When stored as a raw string, these tokens
    are delimited by a dash '-'. This object stores them separately and
    reconstructs the string in various formats.

    Note that in a general GTFS, a block ID can be any string (or None).
    """

    def __init__(self, block_id: str):
        require_not_none(block_id=block_id)

        tokens = block_id.split(WPG_BLOCK_ID_TOKEN_DELIMITER)
        require_state(
            len(tokens) == WPG_BLOCK_ID_NUM_TOKENS,
            f"Block ID should contain exactly {WPG_BLOCK_ID_NUM_TOKENS} "
            f"tokens delimited by '{WPG_BLOCK_ID_TOKEN_DELIMITER}'.",
        )

        self._service_id = tokens[WPG_BLOCK_ID_SERVICE_ID_TOKEN_INDEX]
        self._route_family = tokens[WPG_BLOCK_ID_ROUTE_FAMILY_TOKEN_INDEX]
        self._number = tokens[WPG_BLOCK_ID_NUMBER_TOKEN_INDEX]

        self._check_winnipeg_block_id()

    def __eq__(self, other) -> bool:
        """
        Returns True if the given object is an instance of WinnipegBlockID
        with the same service ID, route family, and number; returns False
        otherwise.
        """
        return (
            isinstance(other, WinnipegBlockID) and
            other._service_id == self._service_id and
            other._route_family == self._route_family and
            other._number == self._number
        )

    @property
    def service_id(self) -> str:
        return self._service_id

    def gtfs_format(self) -> str:
        """
        Returns the full block ID in the form
        [SERVICE ID]-[ROUTE FAMILY]-[NUMBER] as it is stored in the GTFS
        archive.
        This formatting is not generally used to identify runs day-to-day,
        but it is unique across the GTFS.
        """
        return (f"{self._service_id}{WPG_BLOCK_ID_TOKEN_DELIMITER}"
                f"{self._route_family}{WPG_BLOCK_ID_TOKEN_DELIMITER}"
                f"{self._number}")

    def standard_format(self) -> str:
        """
        Returns the shortened block ID in the form [ROUTE FAMILY]-[NUMBER],
        where the service ID is omitted.
        This formatting is most used in practice to identify runs day-to-day
        because the service ID is inferred from the date. However, it is not
        unique across the GTFS.
        """
        return (f"{self._route_family}{WPG_BLOCK_ID_TOKEN_DELIMITER}"
                f"{self._number}")

    def _check_winnipeg_block_id(self) -> None:
        require_not_none(
            service_id=self._service_id,
            route_family=self._route_family,
            block_id_number=self._number
        )
        require_non_empty_str(
            service_id=self._service_id,
            route_family=self._route_family,
            block_id_number=self._number
        )

        require_state(
            self._service_id.isdigit(),
            "Service ID should be an integer."
        )
        require_state(
            self._route_family.isdigit(),
            "Route family should be an integer."
        )
        require_state(
            self._number.isdigit(),
            "Block ID number should be an integer."
        )