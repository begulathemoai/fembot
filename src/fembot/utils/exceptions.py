class NoValueProvidedError(Exception):
    """Raised when a value was not provided (usually in an env var)."""


class NotInitializedError(Exception):
    """Raised when a component was not initialized."""
