from domain.Ride import Ride
from domain.RideList import RideList
from domain.validation.exceptions.RideError import (EmptyBlockNumberError, EmptyDestinationError, EmptyRouteError,
                                                    InvalidBlockNumberError, TrackingNumberDigitError,
                                                    TrackingNumberLengthError, RideError, InvalidDateError,
                                                    InvalidTimeError)
from ui.printing.RidePrinter import print_ride_compact
from utilities.InvariantHelper import require_state
from utilities.PrintHelper import print_error, print_success
from domain.validation.ValidateRide import CURR_DATE_KEYWORD, validate_date, validate_boarding_time, validate_route, \
    validate_tracking_number, validate_destination, validate_block_number

NUM_TOKENS_WITH_NOTES = 7
NUM_TOKENS_WITHOUT_NOTES = 6

def add_ride(ride_list: RideList) -> None:
    """
    Creates a ride from user input and adds it to the given ride list.
    Repeatedly prompts the user for each field until they enter a valid
    input.

    :param ride_list: the ride list to add the ride to.
    """

    ride_date = _prompter(f"Enter the date of the ride (YYYY-MM-DD or '{CURR_DATE_KEYWORD}'): ", validate_date)
    boarding_time = _prompter("Enter boarding time (HH:MM): ", validate_boarding_time)
    route = _prompter("Enter route (e.g. FX2): ", validate_route)
    tracking_number = _prompter("Enter the bus's 3-digit tracking number (e.g. 971): ", validate_tracking_number)
    destination = _prompter("Enter the route's destination (e.g. Markham Station): ", validate_destination)
    block_number = _prompter("Enter the block ID (e.g. 171-7): ", validate_block_number)
    notes = input("Enter any additional notes (can be blank): ")

    if ride_list.get_ride(ride_date, boarding_time):
        print_error("A ride with this date and boarding time already exists.")
    else:
        ride_list.add_ride(Ride(
            ride_date=ride_date,
            boarding_time=boarding_time,
            route=route,
            tracking_number=tracking_number,
            destination=destination,
            block_number=block_number,
            notes=notes
        ))
        print_success("Added ride.")
        _display_previous_rides(ride_list, tracking_number)

def add_rides_quick(ride_list: RideList) -> None:
    """
    Creates rides in succession from single-line CSV input and adds them
    to the given ride list until the user enters 'quit'. Prints error
    messages and prompts the user again if any inputs is invalid.

    :param ride_list: the ride list to add the ride to.
    """
    QUIT_KEYWORD = "quit"

    print("Enter ride information on one line as: YYYY-MM-DD, HH:MM, route, tracking number, destination, block ID, notes\n"
          f"Enter '{CURR_DATE_KEYWORD}' instead of YYYY-MM-DD for today's date.\n"
          f"Warning: duplicates (same date and boarding time) will be silently ignored.\n"
          f"Type '{QUIT_KEYWORD}' to end session.")

    while True:
        csv_raw = input("> ").strip()

        if csv_raw.lower() == QUIT_KEYWORD:
            break

        tokens: list[str] = csv_raw.split(",")

        if len(tokens) not in [NUM_TOKENS_WITH_NOTES, NUM_TOKENS_WITHOUT_NOTES]:
            print_error(f"There should be {NUM_TOKENS_WITHOUT_NOTES} or {NUM_TOKENS_WITH_NOTES} tokens: YYYY-MM-DD, HH:MM, "
                        f"route, tracking number, destination, block ID, notes")
        else:
            try:
                ride: Ride = _create_ride_from_tokens(tokens)
                ride_list.add_ride(ride)

                print_success("Added ride.")
                _display_previous_rides(ride_list, ride.tracking_number)
            except RideError as e:
                _print_error_message(e)

def _prompter(prompt: str, validator):
    """
    Prompts the user and validates their input with the given function.
    Continues prompting until the input is valid.

    :param prompt: the prompt to display to the user.
    :param validator: the function to validate user input.
    :return: valid user input, or an object created from it.
    """
    while True:
        try:
            raw: str = input(prompt)
            return validator(raw)
        except RideError as e:
            _print_error_message(e)

def _print_error_message(error: RideError) -> None:
    """
    Prints an error message corresponding to a given ride error.

    :param error: the ride error for which to print an error message.
    """
    if isinstance(error, InvalidDateError):
        print_error(f"Date should be in YYYY-MM-DD format (or '{CURR_DATE_KEYWORD}').")
    elif isinstance(error, InvalidTimeError):
        print_error("Time should be in HH:MM format.")
    elif isinstance(error, EmptyRouteError):
        print_error("Route cannot be empty.")
    elif isinstance(error, TrackingNumberDigitError):
        print_error("Tracking number can only contain digits.")
    elif isinstance(error, TrackingNumberLengthError):
        print_error("Tracking number must contain exactly 3 characters.")
    elif isinstance(error, EmptyDestinationError):
        print_error("Destination cannot be empty.")
    elif isinstance(error, EmptyBlockNumberError):
        print_error("Block number cannot be empty.")
    elif isinstance(error, InvalidBlockNumberError):
        print_error("Block number can only contain digits and exactly one dash, which "
                    "cannot be the first or last character.")
    else:
        raise error

def _create_ride_from_tokens(tokens: list) -> Ride:
    """
    Constructs and returns a ride based on a list of tokens. The
    list should be of the form [YYYY-MM-DD, HH:MM, route,
    tracking_number, destination, block_number, notes]. Raises
    any exceptions caused by any invalid inputs.

    :param tokens: a list containing the 7 tokens needed to construct
    a ride (not necessarily all valid).
    :return: the ride object constructed from `tokens`.
    """
    require_state(len(tokens) in [NUM_TOKENS_WITH_NOTES, NUM_TOKENS_WITHOUT_NOTES],
                  "There should be 6 or 7 tokens.")

    if len(tokens) == NUM_TOKENS_WITH_NOTES:
        return Ride(
            ride_date=validate_date(tokens[0]),
            boarding_time=validate_boarding_time(tokens[1]),
            route=validate_route(tokens[2]),
            tracking_number=validate_tracking_number(tokens[3]),
            destination=validate_destination(tokens[4]),
            block_number=validate_block_number(tokens[5]),
            notes=tokens[6]
        )
    elif len(tokens) == NUM_TOKENS_WITHOUT_NOTES:
        return Ride(
            ride_date=validate_date(tokens[0]),
            boarding_time=validate_boarding_time(tokens[1]),
            route=validate_route(tokens[2]),
            tracking_number=validate_tracking_number(tokens[3]),
            destination=validate_destination(tokens[4]),
            block_number=validate_block_number(tokens[5]),
            notes=""
        )

def _display_previous_rides(ride_list: RideList, tracking_number: str):
    """
    Prints all rides in `ride_list` corresponding to `tracking_number` if there
    are at least two such rides.

    :param ride_list: the ride list from which to print all rides on the bus
    with the given tracking number.
    :param tracking_number: the tracking number of the bus for which to
    print all rides.
    """
    prev_rides: list[Ride] = ride_list.get_rides_on_bus(tracking_number)

    if len(prev_rides) > 1:
        print(f"\nYou have been on bus {tracking_number} {len(prev_rides)} times:")

        for curr in prev_rides:
            print_ride_compact(curr)
