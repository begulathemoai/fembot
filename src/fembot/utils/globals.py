import os
import re
from io import BufferedReader

import discord
import discord.app_commands

from . import guild_storage, logger

TRIPLE_DOG_DEATH_BARRAGE: BufferedReader = open(  # noqa: SIM115
    os.path.join(os.path.dirname(__file__), "../assets/tripledog.jpg"), "rb"
)  # no

TRACKING_YT_CHART: BufferedReader = open(  # noqa: SIM115
    os.path.join(os.path.dirname(__file__), "../assets/trackingyt.jpg"), "rb"
)  # no the second

# we define intents (these ones will do for now)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


client: discord.Client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


guilds: dict[int, guild_storage.GuildStorage] = {}


test_server_id: int = -1
try:
    test_server_id = int(os.getenv("TEST_SERVER_ID", "-1"))
except TypeError:
    test_server_id = -1


def is_test_server(guild_id: int) -> bool:
    if test_server_id == -1:
        return True
    return guild_id == test_server_id


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


NWORD_REGEX = re.compile(
    "[nոⁿₙNΝՆᴎℕꓠＮᴺŋɴꞃ][i1íïⁱᵢIⅠⅠⅼ丨ιℐℑ∣⍳Ⲓⵏꓲᴵ][gġɡցᶃǥǵᵍGℊ⅁ꓖＧᴳցǵǥ]{1,2}[e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲ][rгᴦʳRΓℛⲢꓣＲᴿɼʁꝛ]",
    re.IGNORECASE | re.MULTILINE,
)
NWORD_REGEX_BUT_FRENCH = re.compile(
    "[nոⁿₙNΝՆᴎℕꓠＮᴺŋɴꞃ][e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲ][gġɡցᶃǥǵᵍGℊ⅁ꓖＧᴳցǵǥ][rгᴦʳRΓℛⲢꓣＲᴿɼʁꝛ][e3еẹėéèₑᵉEΕЕᎬⴹꓰＥ𑢮ᴱɛɇꬲoоοօȯọỏơóòöᵒºOΟОՕ०ꓳ〇ⲞⲟＯᴼ]",
    re.IGNORECASE | re.MULTILINE,
)
YOUTUBE_TRACKING_REGEXES = list(
    map(
        re.compile,
        [
            r"https\:\/\/youtube\.com\/watch\?v=\w+\&si=[a-zA-Z0-9_\-]+",
            r"https\:\/\/youtu\.be\/\w+\?si=[a-zA-Z0-9_\-]+",
        ],
    )
)
