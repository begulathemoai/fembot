"""Initializes fembot with the provided token

Raises:
    exceptions.NoProvidedValueError: No token was provided through DISCORD_BOT_TOKEN in .env or through env vars.
"""

import os

import dotenv

from . import commands, events, utils


def main() -> None:
    dotenv.load_dotenv()
    discord_bot_token: str = os.getenv("DISCORD_BOT_TOKEN", None)
    if discord_bot_token is None:
        raise utils.exceptions.NoProvidedValueError(
            "No token was provided through DISCORD_BOT_TOKEN."
        )
    utils.globals.client.run(discord_bot_token)
