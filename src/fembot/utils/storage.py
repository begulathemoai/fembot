"""I Manage Storage (Manager)"""

import os
import sqlite3  # i love SQL <3

from . import exceptions, globals

### i should maybe split up the folder management part from the db part but ehhhhh

# classic storage part

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


def get_storage_path(guild_id: int) -> str:
    return storage_path + "/" + str(guild_id)


# mixed part

db = None
cursor: sqlite3.Cursor = None


def init() -> None:
    for i in globals.client.guilds:
        if not os.path.exists(storage_path + "/" + str(i.id)):
            os.mkdir(storage_path + "/" + str(i.id), 0o755)

    global cursor, db
    db = sqlite3.connect(storage_path + "/" + "storage.db")
    cursor = db.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
uid INTEGER PRIMARY KEY AUTOINCREMENT,
guild_id INTEGER NOT NULL

);
""")
    db.commit()
    try:
        cursor.execute("""ALTER TABLE guilds ADD new_channel_category_id INT;""")
        db.commit()
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("""ALTER TABLE guilds ADD personal_channels_enabled INT;""")
        db.commit()
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("""ALTER TABLE guilds ADD no_ping_replies_enabled INT;""")
        db.commit()
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute(
            """ALTER TABLE guilds ADD unprompted_no_ping_replies_enabled INT;"""
        )
        db.commit()
    except sqlite3.OperationalError:
        pass
    global initialized
    initialized = True


# db storage part (scary)


def row_to_dict(row: sqlite3.Row):
    new_dict: dict = {}
    for i in row:
        new_dict[i] = row[i]
    return new_dict


def has_guild(guild_id: int):
    cursor.execute("""SELECT * FROM guilds WHERE guild_id == ?""", (guild_id,))
    return len(cursor.fetchall()) > 0


def add_guild(
    guild_id: int,
    new_channel_category_id: int = 0,
    personal_channels_enabled: bool = False,
    no_ping_replies_enabled: bool = False,
    unprompted_no_ping_replies_enabled: bool = False,
):
    if not initialized:
        raise exceptions.NotInitializedError(
            "The storage fembot lib was not initialized. Call storage.init() to initialize the lib."
        )
    cursor.execute(
        """INSERT INTO guilds (guild_id, new_channel_category_id, personal_channels_enabled, no_ping_replies_enabled, unprompted_no_ping_replies_enabled) VALUES (?, ?, ?, ?, ?)""",
        (
            guild_id,
            new_channel_category_id,
            int(personal_channels_enabled),
            int(no_ping_replies_enabled),
            int(unprompted_no_ping_replies_enabled),
        ),
    )
    db.commit()


def get_guild(guild_id: int) -> dict:
    cursor.execute("""SELECT * FROM guilds WHERE guild_id == ?""", (guild_id,))
    return row_to_dict(cursor.fetchall()[0])


def set_guild(guild_id: int, property: str, value) -> None:
    cursor.execute(
        """UPDATE guilds SET ? = ? WHERE guild_id == ?""",
        (
            property,
            value,
            guild_id,
        ),
    )
    db.commit()


def uid_to_guild_id(uid: int) -> int:
    if not initialized:
        raise exceptions.NotInitializedError(
            "The storage fembot lib was not initialized. Call storage.init() to initialize the lib."
        )
    cursor.execute("""SELECT guild_id FROM guilds WHERE uid == ?""", (uid,))
    return cursor.fetchall()[0][0]


def guild_id_to_uid(guild_id: int) -> int:
    if not initialized:
        raise exceptions.NotInitializedError(
            "The storage fembot lib was not initialized. Call storage.init() to initialize the lib."
        )
    cursor.execute("""SELECT uid FROM guilds WHERE guild_id == ?""", (guild_id,))
    return cursor.fetchall()[0][0]
