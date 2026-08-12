import enum
from typing import Any


class SourceType(enum.Enum):
    """Specifies which downloader to use."""

    ATTACHMENT = enum.auto()
    """The source is a discord attachment, use `discord.py`'s built-in downloader."""
    URL = enum.auto()
    """The source is a remote url, use `yt-dlp`."""
    OTHER = enum.auto()
    """The source type is unknown, don't try to download."""


class PlaybackManagerSong:
    """A song managed by the `PlaybackManager`."""

    filename: str | None
    """The path to the song on disk. Replaced by `None` when it is removed from disk (for optimization purposes)."""
    pretty_name: str
    """The song's name as displayed by fembot."""
    source_type: SourceType
    """Specifies which downloader to use with this song."""
    source_reference: Any
    """A reference to the song, depends on the `SourceType`."""
    source_url: str
    """The url the song was downloaded from."""
    uid: str
    """The song's unique id."""
    rank: int
    """The song's rank in the playlist."""

    def __init__(
        self,
        filename: str,
        pretty_name: str,
        source_type: SourceType,
        source_reference: Any,
        source_url: str,
        uid: str,
        rank: int,
    ) -> None:
        self.filename = filename
        self.pretty_name = pretty_name if pretty_name != "" else filename
        self.source_type = source_type
        self.source_reference = source_reference
        self.source_url = source_url
        self.uid = uid
        self.rank = rank
