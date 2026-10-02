from utilities.invariant_helper import require_not_none, require_state
from gtfs.gtfs_constants import HEX_COLOUR_LENGTH, HEX_COLOUR_BASE, HEX_COLOUR_RED_SLICE, HEX_COLOUR_GREEN_SLICE, \
    HEX_COLOUR_BLUE_SLICE, HEX_PRIMARY_COLOUR_LENGTH


class Colour:
    """
    Enforces validity on a colour read from the GTFS and provides getters for
    GTFS Hexadecimal, Hexadecimal, and RGB formats.
    """

    def __init__(self, colour: str):
        require_not_none(colour_string=colour)
        require_state(
            len(colour) == HEX_COLOUR_LENGTH,
            f"Colour string should have exactly {HEX_COLOUR_LENGTH} characters."
        )
        require_state(
            self._is_hex(colour),
            "Colour string should be a hexadecimal string."
        )

        self._hex_red = colour[HEX_COLOUR_RED_SLICE]
        self._hex_green = colour[HEX_COLOUR_GREEN_SLICE]
        self._hex_blue = colour[HEX_COLOUR_BLUE_SLICE]

        self._check_colour()

    @property
    def gtfs_hex(self) -> str:
        """
        Returns a hexadecimal string representation (of the form RRGGBB) for this
        colour.
        """
        return f"{self._hex_red}{self._hex_green}{self._hex_blue}"

    @property
    def hex(self) -> str:
        """
        Returns a hexadecimal string representation (of the form #RRGGBB) for this
        colour.
        """
        return f"#{self._hex_red}{self._hex_green}{self._hex_blue}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        Returns an RGB representation of this colour as an integer tuple of
        the form (RED, GREEN, BLUE).
        """

        return (
            int(self._hex_red, HEX_COLOUR_BASE),
            int(self._hex_green, HEX_COLOUR_BASE),
            int(self._hex_blue, HEX_COLOUR_BASE)
        )

    def _check_colour(self) -> None:
        require_not_none(
            red_hexadecimal_value=self._hex_red,
            green_hexadecimal_value=self._hex_green,
            blue_hexadecimal_value=self._hex_blue
        )
        require_state(
            len(self._hex_red) == HEX_PRIMARY_COLOUR_LENGTH,
            f"Red hexadecimal value should contain exactly {HEX_PRIMARY_COLOUR_LENGTH} characters."
        )
        require_state(
            self._is_hex(self._hex_red),
            f"Red hexadecimal string should only contain hexadecimal characters."
        )

        require_state(
            len(self._hex_green) == HEX_PRIMARY_COLOUR_LENGTH,
            f"Green hexadecimal value should contain exactly {HEX_PRIMARY_COLOUR_LENGTH} characters."
        )
        require_state(
            self._is_hex(self._hex_green),
            f"Green hexadecimal string should only contain hexadecimal characters."
        )

        require_state(
            len(self._hex_blue) == HEX_PRIMARY_COLOUR_LENGTH,
            f"Blue hexadecimal value should contain exactly {HEX_PRIMARY_COLOUR_LENGTH} characters."
        )
        require_state(
            self._is_hex(self._hex_blue),
            f"Blue hexadecimal string should only contain hexadecimal characters."
        )

    @staticmethod
    def _is_hex(colour: str) -> bool:
        """
        Returns True if the trimmed string only consists of hexadecimal characters,
        returns False otherwise.
        """
        try:
            int(colour, HEX_COLOUR_BASE)
            return True
        except ValueError:
            return False
