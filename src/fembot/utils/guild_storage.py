import discord

from . import personal_channel_manager, playback, storage


class GuildStorage:
    # ...
    kirky_ass_messages: list[str]
    enable_the_kirk: bool = True

    # consent is good
    facilitate_setup: bool = True
    """If True, fembot will modify the server by itself to accomodate for some of its systems. Otherwise, affected commands will just error out and ask for manual intervention."""

    guild: discord.Guild
    stfu_timestamp: int = 0
    # TODO
    playback_manager: playback.playback_manager.PlaybackManager
    # TODO
    personal_channel_manager: personal_channel_manager.PersonalChannelManager
    no_ping_replies_enabled: bool = False
    unprompted_no_ping_replies_enabled: bool = False

    # does nothing but getting ready for impl
    personal_channels_enabled: bool = False
    new_personal_channel_category_id: int = 0

    aliases: dict[str, str]

    trusted_members: list[int]

    def __init__(self, guild: discord.Guild) -> None:
        self.kirky_ass_messages = [
            "\\*tel aviv impressed\\*",
            "me when i'm trying to tell bro that he's too racist for me and that i HAVE to put him down for his own good but he cuts me off and starts talking about the roblox ugc market so i lowkirkestrogenuinely have to slime him",
            "i can't stand it anymore",
            "RAWAWAWAWAWAWAWAWAWAWAWAWA",
            """Dude I'm so disappointed by the fart implementation in Tomodachi Life: Living The Dream. In the original, you'd just peek into their apartments to occasionally see them ripping wet ass and it was SO funny. They could be alone, or chilling with their friend. Didn't matter. It didn't discriminate who farted either. It could be Jesus, your grandma, your waifu, whatever. In this game though, you have to choose whether they fart or they don't, but the problem is, if you DO give them the quirk, all they fucking do is fart. It's not funny when they just saunter about letting them slip out 24/7. It was funny in the original because you were sleeping with one eye open-never knowing where or when it would happen next.""",
            "Hey, fascist. Catch! ↑ → ↓↓↓",
            "If you read this, you are gay.",
            "Bella Ciao.",
            "*Notices bulge* OwO what’s this?",
            "[...](https://www.youtube.com/watch?v=av2CT_ieb_Q)",
        ]

        self.guild = guild
        self.playback_manager = playback.playback_manager.PlaybackManager(guild)

        if not storage.has_guild(guild.id):
            storage.add_guild(guild.id)
        else:
            data = storage.get_guild(guild.id)
            if "new_channel_category_id" in data:
                self.new_personal_channel_category_id = data["new_channel_category_id"]
            if "personal_channels_enabled" in data:
                self.personal_channels_enabled = bool(data["personal_channels_enabled"])
            if "no_ping_replies_enabled" in data:
                self.no_ping_replies_enabled = bool(data["no_ping_replies_enabled"])
            if "unprompted_no_ping_replies_enabled" in data:
                self.unprompted_no_ping_replies_enabled = bool(
                    data["unprompted_no_ping_replies_enabled"]
                )
            if "enable_the_kirk" in data:
                self.enable_the_kirk = bool(data["enable_the_kirk"])

            self.aliases = storage.get_aliases(self.guild.id)
            self.trusted_members = storage.get_trusted(self.guild.id)

    async def create_pc_category(self) -> None:
        await self.guild.create_category(name="Personal Channels")

    def get_kirky_message(self) -> str | None:
        return storage.get_kirky_message(self.guild.id)

    def update_storage(self) -> None:
        storage.set_guild(
            self.guild.id,
            "new_channel_category_id",
            self.new_personal_channel_category_id,
        )
        storage.set_guild(
            self.guild.id,
            "personal_channels_enabled",
            int(self.personal_channels_enabled),
        )
        storage.set_guild(
            self.guild.id,
            "no_ping_replies_enabled",
            int(self.no_ping_replies_enabled),
        )
        storage.set_guild(
            self.guild.id,
            "unprompted_no_ping_replies_enabled",
            int(self.unprompted_no_ping_replies_enabled),
        )
        storage.set_guild(
            self.guild.id,
            "enable_the_kirk",
            int(self.enable_the_kirk),
        )

    def add_trusted(self, id: int) -> bool:
        if id in self.trusted_members:
            return False

        self.trusted_members.append(id)
        storage.add_trusted(self.guild.id, id)
        return True

    def remove_trusted(self, id: int) -> bool:
        if id not in self.trusted_members:
            return False

        self.trusted_members.remove(id)
        storage.remove_trusted(self.guild.id, id)
        return True

    def add_alias(self, name: str, content: str) -> bool:
        if name in self.aliases:
            return False

        self.aliases[name] = content
        storage.add_alias(name, content, self.guild.id)
        return True

    def remove_alias(self, name: str) -> bool:
        if name not in self.aliases:
            return False

        self.aliases.pop(name)
        storage.remove_alias(name, self.guild.id)
        return True
