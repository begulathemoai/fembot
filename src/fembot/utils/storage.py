"""I Manage Storage (Manager)"""

import os

from . import globals

storage_path = os.getenv("XDG_DATA_HOME", None)
# storage path setup
if storage_path is None:
    storage_path = os.getenv("HOME", None)
    if storage_path is None:
        raise OSError("No way to get data home (neither XDG_DATA_HOME nor HOME is set)")
    else:
        storage_path = storage_path + "/.local/share"
storage_path += "/fembot"

if not os.path.exists(storage_path):
    os.mkdir(storage_path, 0o755)
# # #


def init() -> None:
    for i in globals.client.guilds:
        if not os.path.exists(storage_path + "/" + str(i.id)):
            os.mkdir(storage_path + "/" + str(i.id), 0o755)


def get_storage_path(guild_id: int) -> str:
    return storage_path + "/" + str(guild_id)
