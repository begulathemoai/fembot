class NoValueProvidedError(Exception):
    """Raised when a value was not provided (usually in an env var)."""


class NotInitializedError(Exception):
    """Raised when a component was not initialized."""


class NotConnectedError(Exception):
    """Raised when the PlaybackManager is not connected to any voice channel."""


class FileTooBigError(Exception):
    """The file was too big to be entirely downloaded."""
