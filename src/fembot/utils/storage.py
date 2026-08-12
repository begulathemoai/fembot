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


def get_playback_storage_path(guild_id: int) -> str:
    return get_storage_path(guild_id) + "/playback"


# mixed part

db = None
cursor: sqlite3.Cursor = None


def init() -> None:
    for i in globals.client.guilds:
        if not os.path.exists(storage_path + "/" + str(i.id)):
            os.mkdir(storage_path + "/" + str(i.id), 0o755)
        if not os.path.exists(storage_path + "/" + str(i.id) + "/playback"):
            os.mkdir(storage_path + "/" + str(i.id) + "/playback", 0o755)

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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kirky_messages (
uid INTEGER PRIMARY KEY AUTOINCREMENT,
guild_id INTEGER NOT NULL,
message VARCHAR(255) NOT NULL
);
""")
    db.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aliases (
uid INTEGER PRIMARY KEY AUTOINCREMENT,
guild_id INTEGER NOT NULL,
name VARCHAR(255) NOT NULL,
content VARCHAR(255) NOT NULL
);
""")
    db.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trusted_members (
uid INTEGER PRIMARY KEY AUTOINCREMENT,
guild_id INTEGER NOT NULL,
user_id INTEGER NOT NULL
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
    try:
        cursor.execute("""ALTER TABLE guilds ADD enable_the_kirk INT;""")
        db.commit()
    except sqlite3.OperationalError:
        pass
    global initialized
    initialized = True


# db storage part (scary)


def row_to_dict(row: sqlite3.Row):
    new_dict: dict = {}
    for i in row.keys():  # noqa: SIM118 # kys ruff this time i'm right you can't just remove .keys()
        new_dict[i] = row[i]
    return new_dict


def has_guild(guild_id: int):
    cursor.execute("""SELECT * FROM guilds WHERE guild_id == ?""", (guild_id,))
    return len(cursor.fetchall()) > 0


def add_trusted(guild_id: int, user_id: int) -> None:
    cursor.execute(
        """INSERT INTO trusted_members (guild_id, user_id) VALUES (?, ?)""",
        (guild_id, user_id),
    )
    db.commit()


def remove_trusted(guild_id: int, user_id: int) -> None:
    cursor.execute(
        """DELETE FROM trusted_members WHERE guild_id == ? AND user_id == ?""",
        (guild_id, user_id),
    )
    db.commit()


def get_trusted(guild_id: int) -> list[int]:
    cursor.execute(
        """SELECT * FROM trusted_members WHERE guild_id == ?""",
        (guild_id,),
    )
    out: list[int] = []
    rows: list[sqlite3.Row] = cursor.fetchall()
    for i in rows:
        out.append(i["user_id"])
    return out


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
        f"""UPDATE guilds
         SET {property} == :value
         WHERE guild_id == :guild_id""",
        {
            "value": value,
            "guild_id": guild_id,
        },
    )
    db.commit()


def add_alias(name: str, content: str, guild_id: int) -> None:
    cursor.execute(
        """INSERT INTO aliases (guild_id, name, content) VALUES (?, ?, ?)""",
        (guild_id, name, content),
    )
    db.commit()


def remove_alias(name: str, guild_id: int) -> None:
    cursor.execute(
        """DELETE FROM aliases WHERE guild_id == ? AND name == ?""",
        (guild_id, name),
    )
    db.commit()


def get_aliases(guild_id: int) -> dict[str, str]:
    cursor.execute(
        """SELECT * FROM aliases WHERE guild_id == ?""",
        (guild_id,),
    )
    out: dict[str, str] = {}
    rows: list[sqlite3.Row] = cursor.fetchall()
    for i in rows:
        out[i["name"]] = i["content"]
    return out


def add_kirky_message(message: str, guild_id: int) -> None:
    cursor.execute(
        """INSERT INTO kirky_messages (guild_id, message) VALUES (?, ?)""",
        (guild_id, message),
    )
    db.commit()


def get_kirky_message(guild_id: int) -> str | None:
    cursor.execute(
        """SELECT message FROM kirky_messages WHERE guild_id == ? ORDER BY RANDOM() LIMIT 1;""",
        (guild_id,),
    )
    result = cursor.fetchone()
    if result == None:
        return None
    else:
        return result[0]


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
