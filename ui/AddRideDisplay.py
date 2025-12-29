from domain.Ride import Ride
from datetime import date, time
from ui.printing.RidePrinter import print_ride_compact

from domain.exceptions.EmptyBlockNumberError import EmptyBlockNumberError
from domain.exceptions.EmptyDestinationError import EmptyDestinationError
from domain.exceptions.EmptyRouteError import EmptyRouteError
from domain.exceptions.InvalidBlockNumberError import InvalidBlockNumberError
from domain.exceptions.TrackingNumberDigitError import TrackingNumberDigitError
from domain.exceptions.TrackingNumberLengthError import TrackingNumberLengthError
from utilities.PrintHelper import print_error, print_success

CURR_DATE_KEYWORD = "today"
SINGLE_DIGIT_HOUR_TIME_LENGTH = 4

def run_add_ride_regular(ride_list):
    """
    Creates a ride from user input and adds it to the given ride list. Prints error messages
    and prompts the user again if any input is invalid.

    :param ride_list: the ride list to add a ride to.
    """
    ride_date = _get_date_input()
    boarding_time = _get_time_input()
    route = _get_route_input()
    tracking_number = _get_tracking_number_input()
    destination = _get_destination_input()
    block_number = _get_block_number_input()
    notes = _get_notes_input()

    while True:
        try:
            ride = Ride.build(ride_date,
                              boarding_time,
                              route,
                              tracking_number,
                              destination,
                              block_number,
                              notes)

            _add_ride_and_print_messages(ride_list, ride, tracking_number)
            break
        except EmptyRouteError:
            print_error("Route cannot be empty.")
            route = _get_route_input()
        except TrackingNumberLengthError:
            print_error("Tracking number must contain exactly 3 characters.")
            tracking_number = _get_tracking_number_input()
        except TrackingNumberDigitError:
            print_error("Tracking number can only contain digits.")
            tracking_number = _get_tracking_number_input()
        except EmptyDestinationError:
            print_error("Destination cannot be empty.")
            destination = _get_destination_input()
        except EmptyBlockNumberError:
            print_error("Block number cannot be empty.")
            block_number = _get_block_number_input()
        except InvalidBlockNumberError:
            print_error("Block number can only contain digits and exactly one dash, which "
                        "cannot be the first or last character.")
            block_number = _get_block_number_input()

def run_add_ride_quick(ride_list):
    """
    Creates rides in succession from single-line CSV input and adds them to the
    given ride list until the user enters 'quit'. Prints error messages and
    prompts the user again if any input is invalid.

    :param ride_list: the ride list to add a ride to.
    """
    quit_keyword = "quit"
    num_tokens = 7

    print("*** Quick add mode ***\n" 
          "Enter rides in the form YYYY-MM-DD, HH:MM, route, destination, tracking number, block ID, notes\n"
          f"Enter '{CURR_DATE_KEYWORD}' instead of YYYY-MM-DD for today's date.\n"
          "Type 'quit' to exit quick add.")

    while True:
        try:
            ride_str = input("> ").strip()

            if ride_str.lower() == quit_keyword:
                break

            tokens = ride_str.split(",")
            if len(tokens) != num_tokens:
                print_error(f"There should be {num_tokens} tokens: YYYY-MM-DD, HH:MM, route, destination, "
                            f"tracking number, block ID, notes")
            else:
                if tokens[0].strip().lower() == CURR_DATE_KEYWORD:
                        ride_date = date.today()
                else:
                    ride_date = date.fromisoformat(tokens[0].strip())

                if len(tokens[1].strip()) == SINGLE_DIGIT_HOUR_TIME_LENGTH:
                    boarding_time = time.fromisoformat("0" + tokens[1].strip())
                else:
                    boarding_time = time.fromisoformat(tokens[1].strip())

                route = tokens[2].strip()
                destination = tokens[3].strip()
                tracking_number = tokens[4].strip()
                block_number = tokens[5].strip()
                notes = tokens[6].strip()

                ride = Ride.build(ride_date,
                                  boarding_time,
                                  route,
                                  tracking_number,
                                  destination,
                                  block_number,
                                  notes)

                _add_ride_and_print_messages(ride_list, ride, tracking_number)
        except ValueError:
            print_error("Date and time should be in YYYY-MM-DD and HH:MM format, respectively.")
        except EmptyRouteError:
            print_error("Route cannot be empty.")
        except TrackingNumberLengthError:
            print_error("Tracking number must contain exactly 3 characters.")
        except TrackingNumberDigitError:
            print_error("Tracking number can only contain digits.")
        except EmptyDestinationError:
            print_error("Destination cannot be empty.")
        except EmptyBlockNumberError:
            print_error("Block number cannot be empty.")
        except InvalidBlockNumberError:
            print_error("Block number can only contain digits and exactly one dash, which "
                        "cannot be the first or last character.")

def _get_date_input():
    """
    Gets a date in YYYY-MM-DD from the user and creates a date object, printing an error
    message and prompting the user again if their input is invalid.

    :return: the date object created from user input.
    """
    while True:
        try:
            date_str = input(f"Enter the date of the ride in YYYY-MM-DD format (or '{CURR_DATE_KEYWORD}'): ").strip()

            if date_str.lower() == CURR_DATE_KEYWORD:
                return date.today()

            return date.fromisoformat(date_str)
        except ValueError:
            print_error(f"Date should be in YYYY-MM-DD format (or '{CURR_DATE_KEYWORD}').")

def _get_time_input():
    """
    Gets a boarding time in HH:MM from the user and creates a time object, printing an error
    message and prompting the user again if their input is invalid.

    :return: the time object created from user input.
    """
    while True:
        try:
            time_str = input("Enter the boarding time in HH:MM format: ").strip()

            if len(time_str) == SINGLE_DIGIT_HOUR_TIME_LENGTH:
                time_str = "0" + time_str

            return time.fromisoformat(time_str)
        except ValueError:
            print_error("Time should be in HH:MM format.")

def _get_route_input():
    return input("Enter route (e.g. FX2): ")

def _get_tracking_number_input():
    return input("Enter the bus's 3-digit tracking number (e.g. 971): ")

def _get_destination_input():
    return input("Enter the route's destination (e.g. Markham Station): ")

def _get_block_number_input():
    return input("Enter the block ID (e.g. 171-7): ")

def _get_notes_input():
    return input("Enter any additional notes (can be blank): ")

def _add_ride_and_print_messages(ride_list, ride, tracking_number):
    """
    Adds the given ride to the given list, prints a success message,
    and prints all previous rides in `ride_list` on bus `tracking_number`.

    :param ride_list: the ride list to which to add `ride`.
    :param ride: the ride to add to `ride_list`.
    :param tracking_number: the tracking number of the bus
    for which to print previous rides.
    """
    print_success("Added ride.")
    _display_previous_rides(ride_list, tracking_number)
    ride_list.add_ride(ride)

def _display_previous_rides(ride_list, tracking_number):
    """
    Prints all rides in `ride_list` corresponding to `tracking_number`.

    :param ride_list: the ride list from which to print all rides on bus
    `tracking_number`.
    :param tracking_number: the tracking number of the bus for which to
    print all rides.
    """
    prev_rides = ride_list.get_rides_on_bus(tracking_number)

    if prev_rides:
        if len(prev_rides) == 1:
            print(f"\nYou have been on bus {tracking_number} one time:")
        else:
            print(f"\nYou have been on bus {tracking_number} {len(prev_rides)} times:")

        for curr in prev_rides:
            print_ride_compact(curr)






