"""Initializes fembot with the provided token

slash commands are the most important user facing commands
garmin commands are the "fun" user commands and all of the admin ones that should not show up in bot autocomplete


Raises:
    exceptions.NoProvidedValueError: No token was provided through DISCORD_BOT_TOKEN in .env or through env vars.
"""

import asyncio
import os

from . import commandline, utils
from . import commands as commands
from . import events as events


async def eventloop(discord_bot_token):
    await asyncio.gather(
        utils.globals.client.start(discord_bot_token),
        commandline.commandline.commandline(),  # zamn :sob:
    )


def main() -> None:
    utils.logger.log("fetching token...")
    discord_bot_token: str = os.getenv("FEM_BOT_TOKEN", None)
    if discord_bot_token is None:
        raise utils.exceptions.NoValueProvidedError(
            "No token was provided through FEM_BOT_TOKEN."
        )
    utils.logger.log("starting discord.py eventloop...")
    # asyncio.run(eventloop(discord_bot_token))
    utils.globals.client.run(discord_bot_token)
