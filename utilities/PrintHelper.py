RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
ERROR_PREFIX = "[ERROR] "
SUCCESS_PREFIX = "[SUCCESS] "

def print_error(message):
    """
    Prints a given error message to the terminal in red, prefixed
    by [ERROR].

    :param message: the error message to print.
    """
    print_red(ERROR_PREFIX + message)

def print_success(message):
    """
    Prints a given success message to the terminal in green, prefixed
    by [SUCCESS].

    :param message: the success message to print.
    """
    print_green(SUCCESS_PREFIX + message)

def print_red(text):
    print(RED + text + RESET)

def print_green(text):
    print(GREEN + text + RESET)

