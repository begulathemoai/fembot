import os

import discord
import discord.app_commands

from . import logger

# we define intents (these ones will do for now)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


client: discord.Client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


owner_id: int
# owner_id initialization
try:
    owner_id = int(os.getenv("OWNER_ID", "-1"))
except TypeError:
    owner_id = -1
    logger.log("The provided OWNER_ID was of an incorrect type.")
# # #

banned_users: list[int] = []

ready: bool = False

"""Fill this var using the `GUILD_WHITELIST` env var. If it is empty, all guilds are allowed.
    """
guild_whitelist: list[int] = []
# guild_whitelist initialization
guild_whitelist_env_var: str = os.getenv("GUILD_WHITELIST", "")
if guild_whitelist_env_var != "":
    for i in guild_whitelist_env_var.split(":"):
        if i.isnumeric():
            guild_whitelist.append(int(i))
        else:
            logger.log(
                "Part of GUILD_WHITELIST, "
                + str(i)
                + ", was not recognized as a valid integer."
            )
del guild_whitelist_env_var
# # #

"""Set this to True if the `guild_whitelist` should act as a blacklist.
    """
blacklist_mode: bool = False


def is_guild_allowed(id: int):
    if blacklist_mode:
        return id not in guild_whitelist
    elif len(guild_whitelist) == 0:
        return True
    else:
        return id in guild_whitelist
