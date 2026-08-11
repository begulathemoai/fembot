"""Initializes fembot with the provided token

slash commands are the most important user facing commands
garmin commands are the "fun" user commands and all of the admin ones that should not show up in bot autocomplete


Raises:
    exceptions.NoProvidedValueError: No token was provided through DISCORD_BOT_TOKEN in .env or through env vars.
"""

import os

import dotenv

from . import commands as commands
from . import events as events
from . import utils


def main() -> None:
    dotenv.load_dotenv()
    discord_bot_token: str = os.getenv("DISCORD_BOT_TOKEN", None)
    if discord_bot_token is None:
        raise utils.exceptions.NoValueProvidedError(
            "No token was provided through DISCORD_BOT_TOKEN."
        )
    utils.globals.client.run(discord_bot_token)
