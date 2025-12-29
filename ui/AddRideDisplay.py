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

def run_add_ride(ride_list):
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

            print_success("Added ride.")
            _display_previous_rides(ride_list, tracking_number)

            ride_list.add_ride(ride)
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
            print_error("Block number can only contains digits and exactly one dash, which "
                        "cannot be the first or last character.")
            block_number = _get_block_number_input()

def _get_date_input():
    """
    Gets a date in YYYY-MM-DD from the user and creates a date object, printing an error
    message and prompting the user again if their input is invalid.

    :return: the date object created from user input.
    """
    while True:
        try:
            date_str = input("Enter the date of the ride in YYYY-MM-DD format (or 'today'): ").strip()

            if date_str.lower() == "today":
                return date.today()

            return date.fromisoformat(date_str)
        except ValueError:
            print_error("Date should be in YYYY-MM-DD format (or 'today').")

def _get_time_input():
    """
    Gets a boarding time in HH:MM from the user and creates a time object, printing an error
    message and prompting the user again if their input is invalid.

    :return: the time object created from user input.
    """
    while True:
        single_digit_hour_time_length = 4

        try:
            time_str = input("Enter the boarding time in HH:MM format: ").strip()

            if len(time_str) == single_digit_hour_time_length:
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






