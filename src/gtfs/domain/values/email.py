import validators
from utilities.invariant_helper import require_not_none, require_state, require_non_empty_str


class Email:
    """
    Enforces validity on an email address read from the GTFS archive.
    """

    def __init__(self, email_address: str):
        self._email = email_address

        self._check_email()

    def __str__(self) -> str:
        return self._email

    def _check_email(self) -> None:
        require_not_none(
            email_username=self._email
        )
        require_non_empty_str(
            email_username=self._email
        )

        require_state(
            validators.email(self._email),
            f"Email address '{self._email}' is invalid."
        )

