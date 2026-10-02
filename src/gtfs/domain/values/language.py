from language_tags import tags
from utilities.invariant_helper import require_not_none, require_non_empty_str, require_state


class Language:
    """
    Enforces validity on a BCP 47 language tag read from the GTFS archive.
    """

    def __init__(self, language_code: str):
        self._language_code = language_code

        self._check_language()

    def __str__(self) -> str:
        return self._language_code

    def _check_language(self) -> None:
        require_not_none(language_code=self._language_code)
        require_non_empty_str(language_code=self._language_code)
        require_state(
            tags.check(self._language_code),
            f"Language code '{self._language_code}' is not a valid BCP 47 language tag."
        )