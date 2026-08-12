import os
import re
from io import BufferedReader

import discord
import discord.app_commands
import dotenv

from . import guild_storage, logger

# we load all env vars from the .env file
dotenv.load_dotenv()

TRIPLE_DOG_DEATH_BARRAGE: BufferedReader = open(  # noqa: SIM115
    os.path.join(os.path.dirname(__file__), "../assets/tripledog.jpg"), "rb"
)  # no
"""A file stream to `/src/fembot/assets/tripledog.jpg`."""

TRACKING_YT_CHART: BufferedReader = open(  # noqa: SIM115
    os.path.join(os.path.dirname(__file__), "../assets/trackingyt.jpg"), "rb"
)  # no the second
"""A file stream to `/src/fembot/assets/trackingyt.jpg`."""

individual_song_size_limit: int = 10_000_000
"""The size limit that a single song should never cross"""
collective_song_size_limit: int = 500_000_000
"""The size limit that all songs combined should never cross (per-server)"""


# we define intents (these ones will do for now)
intents = discord.Intents.default()
"""This bot's discord intents."""
intents.members = True
intents.message_content = True


client: discord.Client = discord.Client(intents=intents)
"""The discord client running fembot."""
tree = discord.app_commands.CommandTree(client)


guilds: dict[int, guild_storage.GuildStorage] = {}
"""Links the ids of the guilds fembot is in to their `GuildStorage`s."""


test_server_id: int = -1
"""If anything other than -1, fembot will only operate in the guild that has this id. Defined in the `TEST_SERVER_ID` env var."""
try:
    test_server_id = int(os.getenv("TEST_SERVER_ID", "-1"))
except TypeError:
    test_server_id = -1


def is_test_server(guild_id: int) -> bool:
    """Whether the guild of id `guild_id` is the current test guild."""
    if test_server_id == -1:
        return True
    return guild_id == test_server_id


owner_id: int
"""The user id of this instance's owner. Defined in the `OWNER_ID` env var."""
# owner_id initialization
try:
    owner_id = int(os.getenv("OWNER_ID", "-1"))
except TypeError:
    owner_id = -1
    logger.log("The provided OWNER_ID was of an incorrect type.")
# # #

bot_banned_users: list[int] = []
"""A list of the ids of users banned from this instance of fembot. Defined in the `BOT_BANNED_USERS` env var with format `id1:id2:id3:...:idN`."""
# bot_banned_users init
bot_banned_users_env_var: str = os.getenv("BOT_BANNED_USERS", "")
if bot_banned_users_env_var != "":
    for i in bot_banned_users_env_var.split(":"):
        if i.isnumeric():
            bot_banned_users.append(int(i))
        else:
            logger.log(
                "Part of BOT_BANNED_USERS, "
                + str(i)
                + ", was not recognized as a valid integer."
            )
del bot_banned_users_env_var
# # #

ready: bool = False
"""Whether fembot is fully ready to process commands and messages."""

guild_whitelist: list[int] = []
"""Which guilds this instance of fembot is allowed to operate in. Defined in the `GUILD_WHITELIST` env var with format `id1:id2:id3:...:idN`.
    """
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


blacklist_mode: bool = False
"""Set this to True if the `guild_whitelist` should act as a blacklist.
    """


def is_guild_allowed(id: int):
    """Checks whether fembot is allowed to operate in the guild of id `id`."""
    if blacklist_mode:
        return id not in guild_whitelist
    elif len(guild_whitelist) == 0:
        return True
    else:
        return id in guild_whitelist


NWORD_REGEX = re.compile(
    "[nոⁿₙNΝՆᴎℕꓠＮᴺŋɴꞃ][i1íïⁱᵢIⅠⅠⅼ丨ιℐℑ∣⍳Ⲓⵏꓲᴵ][gġɡցᶃǥǵᵍGℊ⅁ꓖＧᴳցǵǥ]{2}[e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲ][rгᴦʳRΓℛⲢꓣＲᴿɼʁꝛ]",
    re.IGNORECASE | re.MULTILINE,
)
"""A regex matching more or less well the english n-word."""
NWORD_REGEX_BUT_FRENCH = re.compile(
    "[nոⁿₙNΝՆᴎℕꓠＮᴺŋɴꞃ][e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲ][gġɡցᶃǥǵᵍGℊ⅁ꓖＧᴳցǵǥ][rгᴦʳRΓℛⲢꓣＲᴿɼʁꝛ][e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲoоοօȯọỏơóòöᵒºOΟОՕ०ꓳ〇ⲞⲟＯᴼ]",
    re.IGNORECASE | re.MULTILINE,
)
"""A regex matching more or less well the french n-word. (also matches the spanish word "black" but you can't make an omelet without breaking a few eggs and we are making the mother of all omelettes here jack can't fret over every egg or whatever)"""

YOUTUBE_TRACKING_REGEXES = list(
    map(
        re.compile,
        [
            r"https\:\/\/youtube\.com\/watch\?v=\w+\&si=[a-zA-Z0-9_\-]+",
            r"https\:\/\/youtu\.be\/\w+\?si=[a-zA-Z0-9_\-]+",
        ],
    )
)
"""Regexes matching a few youtube urls with embedded tracking."""
