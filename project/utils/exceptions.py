"""Module for custom exceptions."""


class EmptyDataSetImport(Exception):
    """Exception to raise on attemptying to import dataset with no rows."""

    pass


class HumanReadableError(Exception):
    """Custom exception to mark controlled errors for better user notification messages."""

    pass
