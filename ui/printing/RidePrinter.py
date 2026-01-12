import textwrap

from domain.Ride import Ride

LINE_WIDTH = 72
INDENT_SPACES = 3
SUB_INDENT_SPACES = 6

def print_ride_compact(ride: Ride) -> None:
    """
    Prints a compact representation of a given ride. The tracking
    number, date/time, route, destination, and block number are printed
    on a single line.

    :param ride: the ride to print.
    """
    date_str = ride.ride_date.isoformat()
    time_str = ride.boarding_time.strftime("%H:%M")

    print(f"Bus {ride.tracking_number} | {date_str} {time_str} | Route {ride.route} -> {ride.destination} "
          f"| Block {ride.block_number}")

def print_ride_detailed(ride: Ride, curr_route: str, curr_stop: str) -> None:
    """
    Prints a detailed representation of a given ride. The date/time, route,
    destination, block ID, tracking number, and additional notes are printed
    on separate lines, as well as the specified current route/stop of the bus.

    :param ride: the ride to print.
    :param curr_route: the current route being served by the bus ridden in `ride`.
    :param curr_stop: the current stop being served by the bus ridden in `ride`.
    """
    indent = INDENT_SPACES * " "
    sub_indent = SUB_INDENT_SPACES * " "

    date_str = ride.ride_date.strftime("%B %d, %Y")
    time_str = ride.boarding_time.strftime("%I:%M %p")

    print(
    f"Ride on {date_str} at {time_str}\n"
    f"{indent}Route: {ride.route}\n"
    f"{indent}Destination: {ride.destination}\n"
    f"{indent}Block ID: {ride.block_number}\n"
    f"{indent}Bus: {ride.tracking_number}\n"
    f"{sub_indent}Current route: {curr_route}\n"
    f"{sub_indent}Current stop: {curr_stop}\n"
    f"{indent}Additional notes:"
    )

    _print_paragraph(ride.notes, SUB_INDENT_SPACES)

def _print_paragraph(text: str, indentation: int) -> None:
    """
    Prints a string in paragraph form. Adds a newline and a given number of
    spaces whenever the maximal line width (72) is reached.

    :param text: the string to print in paragraph form.
    :param indentation: the number of spaces with which to indent each line.
    """

    wrapper = textwrap.TextWrapper(
        width=LINE_WIDTH,
        initial_indent= " " * indentation,
        subsequent_indent= " " * indentation
    )

    print(wrapper.fill(text))